# coding=utf-8
import logging
import time
import traceback

from monitor.apps.ceph_cluster.api.ceph_cluster_api import CephClusterHostApi, CephClusterRgwApi
from monitor.apps.database_server.api.alrams_api import EventCasesManageResourceApi
from monitor.apps.host_manage.dbresources.resource import HostManageResource
from monitor.common.controller import CollectionController, ItemController
from monitor.core.exceptions import NotFoundError, CriticalError
from monitor.core.falcon_api_service import FalconApiService
LOG = logging.getLogger(__name__)


class CephClusterHostsAlarmStatus(CollectionController):
    name = 'monitor.ceph_cluster_alarm.item'
    allow_methods = ('POST',)
    resource = CephClusterHostApi

    def on_post(self, req, resp, **kwargs):

        def alarm_type_convert(alarm_type, status):
            alarm_param = {
                "status": "PROBLEM",
            }
            if alarm_type == "1":
                alarm_param["$or"] = [{"metric": {"ilike": "cpu"}}]
            elif alarm_type == "2":
                alarm_param["$or"] = [{"metric": {"ilike": "mem"}}]
            elif alarm_type == "3":
                alarm_param["$or"] = [{"metric": {"ilike": "net."}}]

            if status and status < 3:
                alarm_param["priority"] = status
            return alarm_param

        self._validate_method(req)
        try:
            host_uuid_list = req.json.get("host_uuids")

            alarm = req.json.get("alarm_type")
            search_status = req.json.get("status")
            param = alarm_type_convert(alarm, search_status)
            # 查询告警
            event_endpoint_map = {}
            if isinstance(host_uuid_list, list) and len(host_uuid_list) > 0:
                param["endpoint"] = {"in": host_uuid_list}
                event_endpoint_map = self._get_host_event_map(param)
            result = {}
            for endpoint in host_uuid_list:
                status_list = self._get_host_alarms_status(endpoint, event_endpoint_map)
                if alarm and alarm > 0:
                    status_list = [status_list[int(alarm) - 1]]
                if search_status:
                    ignore = True
                    for status in status_list:
                        if int(search_status) == status.get("value"):
                            ignore = False
                    if ignore:
                        continue
                result[endpoint] = status_list
            resp.json = {"data": result}
        except Exception as e:
            LOG.error("CephClusterHostsAlarmStatus get err %s", e)
            LOG.error(traceback.format_exc())
            raise CriticalError("数据异常，获取主机状态失败")

    def _get_host_alarms_status(self, endpoint, event_endpoint_map):
        """
            获取主机告警状态
        """
        event_temp_list = event_endpoint_map.get(endpoint)
        # 3正常  0-2 依次为高中低
        cpu_status = 3
        mem_status = 3
        net_status = 3
        if event_temp_list:
            for event in event_temp_list:
                if cpu_status + mem_status + net_status == 0:
                    break
                if event.get("metric", '').startswith("cpu") and cpu_status != 0:
                    cpu_status = event.get("priority") if event.get("priority") < cpu_status else cpu_status
                elif event.get("metric", '').startswith("mem") and mem_status != 0:
                    mem_status = event.get("priority") if event.get("priority") < mem_status else mem_status
                elif event.get("metric", '').startswith("net.") and net_status != 0:
                    net_status = event.get("priority") if event.get("priority") < net_status else net_status
        status_list = [{"alarm_type": "1", "value": cpu_status}, {"alarm_type": "2", "value": mem_status},
                       {"alarm_type": "3", "value": net_status}]
        return status_list

    def _get_host_event_map(self, param):
        """
            获取主机告警事件字典
        """
        event_list = EventCasesManageResourceApi().list(filters=param)
        event_endpoint_map = {}
        # 告警以endpoint维度分组
        for event in event_list:
            endpoint = event.get("endpoint")
            event_array = event_endpoint_map.get(endpoint)
            if event_array and isinstance(event_array, list):
                event_array.append(event)
            else:
                event_endpoint_map[endpoint] = [event]
        return event_endpoint_map


class CephClusterHostMetric(ItemController):
    name = 'monitor.ceph_cluster_host_metric'
    allow_methods = ('GET',)
    cpu_metric = "cpu.busy"
    mem_metric = "mem.memused.percent"
    net_in_metric = "net.if.in.bytes"
    net_out_metric = "net.if.out.bytes"

    def on_get(self, req, resp, **kwargs):
        host_uuid = kwargs.pop('rid')
        now = int(time.time())
        params = [{"endpoint": host_uuid, "counter": self.mem_metric},
                  {"endpoint": host_uuid, "counter": self.cpu_metric}]

        try:
            counter_list = FalconApiService().get_counter([host_uuid], "net.if.in.bytes")
            for counter in counter_list:
                params.append({
                    "endpoint": host_uuid,
                    "counter": self.net_in_metric + "/" + counter
                })
                params.append({
                    "endpoint": host_uuid,
                    "counter": self.net_out_metric + "/" + counter
                })
            graph_list = FalconApiService().get_last_point_by_graph(params)
        except Exception as e:
            LOG.error("FalconApiService() get result err %s", traceback.format_exc())
            raise CriticalError("系统错误")
        data = {}
        net_in_list = []
        net_out_list = []
        counter_map = {}
        for item in graph_list:
            # 判断获取的指标值 是否正常
            result = item.get("value", {})
            value = result.get("value", 0)
            timestamp = result.get("timestamp", 0)
            if now - timestamp > 300:
                value = 0
            counter_map[item["counter"]] = value
        data[self.cpu_metric] = counter_map.get(self.cpu_metric, 0)
        data[self.mem_metric] = counter_map.get(self.mem_metric, 0)
        for counter in counter_list:
            net_in_list.append({"iface": counter, "value": counter_map.get(self.net_in_metric + "/" + counter, 0)})
            net_out_list.append({"iface": counter, "value": counter_map.get(self.net_out_metric + "/" + counter, 0)})
        data[self.net_in_metric] = net_in_list
        data[self.net_out_metric] = net_out_list
        resp.json = {"timestamp": now, "data": data}


# 集群视图
class CephClusterView(CollectionController):
    name = 'monitor.ceph_cluster_host_metric'
    allow_methods = ('POST',)
    resource = CephClusterHostApi

    def on_post(self, req, resp, **kwargs):
        cluster_id = kwargs.pop("rid")
        mgr_list = req.json.get("mgr", [])
        mon_list = req.json.get("mon", [])
        rgw_list = req.json.get("rgw", [])
        params = []
        for mgr in mgr_list:
            params.append({"endpoint": cluster_id, "counter": "mgr.status/name=" + mgr})
        for mon in mon_list:
            params.append({"endpoint": cluster_id, "counter": "mon.status/name=" + mon})
        for rgw in rgw_list:
            params.append({"endpoint": cluster_id, "counter": "rgw.status/name=" + rgw})
        data = {}
        if len(params) == 0:
            resp.json = data
            return
        try:
            graph_list = FalconApiService().get_last_point_by_graph(params)
        except Exception as e:
            LOG.error("FalconApiService() get result err %s", traceback.format_exc())
            raise CriticalError("主机状态查询失败")
        graph_map = {}
        for item in graph_list:
            status = 'down'
            # 判断获取的指标值 是否正常
            result = item.get("value", {})
            value = result.get("value", 0)
            status = 'up' if value == 1 else status
            timestamp = result.get("timestamp", 0)
            if int(time.time()) - timestamp > 300:
                status = 'down'
            graph_map[item["counter"]] = status
        mgr_result = {}
        mon_result = {}
        rgw_result = {}
        for mgr in mgr_list:
            mgr_result[mgr] = graph_map.get("mgr.status/name=" + mgr, 'down')
        for mon in mon_list:
            mon_result[mon] = graph_map.get("mon.status/name=" + mon, 'down')
        for rgw in rgw_list:
            rgw_result[rgw] = graph_map.get("rgw.status/name=" + rgw, 'down')
        if mgr_result:
            data["mgr"] = mgr_result
        if mon_result:
            data["mon"] = mon_result
        if rgw_result:
            data["rgw"] = rgw_result
        LOG.info("return %s",data)
        resp.json = data
