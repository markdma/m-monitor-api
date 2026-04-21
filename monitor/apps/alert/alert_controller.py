# -*- coding:utf-8 -*-
import copy
import datetime
import logging
import re

import IPy
import falcon
import ipaddress

from monitor.apps.alert.api import alert_api
from monitor.apps.alert.dbresources.resource import AlarmScheManageResource, EventCasesResource, AlarmNoteResource, \
    EventsManageResource, TPLManageResource, StrategyManageResource, GRPManageResource, \
    ActionManageResource, HostResource, GRPHostManageResource, UserManageResource, RelActionUserManageResource, \
    GRPTplManageResource, StrategyCallbackManageResource, ProjectResource, CustomManageResource, \
    AlarmAssetResource, TPLHostManageResource, CustomStrategyManageResource, AssetTPLResource, CounterManageResource, \
    AlarmCountResource
from monitor.apps.database_server.dbresources.resource import HostManageResource, AvailableZoneResource
from monitor.apps.network_manage.api import network_manage_api
from monitor.common import const_define, time_util
from monitor.common.controller import ItemController, CollectionController
from monitor.common.decorators import tenant_project_func, set_operate_user_func
from monitor.common.ipv6_filer import IPv6FilerConvert
from monitor.core import config
from monitor.core.exceptions import ValidationError, NotFoundError
from monitor.core.falcon_api_service import FalconApiService
from monitor.core.utils import ensure_unicode
from monitor.db import converter
from monitor.db.crud import ResourceBase
from monitor.lib.validation import check_params_with_model

LOG = logging.getLogger(__name__)

CONF = config.CONF


class AlarmScheBase(object):

    @staticmethod
    def _arg_model_data():
        define = {
            "group_type": {"type": basestring, "notnull": True, "required": True,
                           "format": {"in": ["host", "group", "oper", "net", "storage", "openstack", "vdb", "watch",
                                             "apigateway", "container", "datacenter", "office"]}},
            "start_date": {"type": basestring, "notnull": True, "required": True, "format": {">": 0, "<": 256}},
            "end_date": {"type": basestring, "notnull": True, "required": True, "format": {">": 0, "<": 256}},
            "empno_m": {"type": basestring, "notnull": True, "required": True, "format": {">": 0, "<": 256}},
            "empno_b": {"type": basestring, "notnull": True, "required": True, "format": {">": 0, "<": 256}},
            "updater": {"type": basestring, "notnull": True, "required": True, "format": {">": 0, "<": 256}}
        }
        return define

    @staticmethod
    def _arg_batch_model_data():
        define = {
            "group_type": {"type": basestring, "notnull": True, "required": True,
                           "format": {"in": ["host", "group", "oper", "net", "storage", "openstack", "vdb", "watch",
                                             "apigateway", "container", "datacenter", "office"]}},
            "start_date": {"type": basestring, "notnull": True, "required": True, "format": {">": 0, "<": 256}},
            "end_date": {"type": basestring, "notnull": True, "required": True, "format": {">": 0, "<": 256}},
            "data_list": {"type": list, "notnull": True, "required": True}
        }
        return define

    @staticmethod
    def _arg_update_model_data():
        define = {
            "start_date": {"type": basestring, "notnull": True, "required": False, "format": {">": 0, "<": 256}},
            "end_date": {"type": basestring, "notnull": True, "required": False, "format": {">": 0, "<": 256}},
            "empno_m": {"type": basestring, "notnull": True, "required": False, "format": {">": 0, "<": 256}},
            "empno_b": {"type": basestring, "notnull": True, "required": False, "format": {">": 0, "<": 256}},
            "updater": {"type": basestring, "notnull": False, "required": False, "format": {">": 0, "<": 256}}
        }
        return define

    @staticmethod
    def check_plan_time(start_time, end_time, group_type, self_flag=False, self_id=None):
        time_util.get_timestamp(start_time)
        time_util.get_timestamp(end_time)
        filters = {"group_type": group_type,
                   "$or": [{"start_date": {"lte": end_time, "gte": start_time}},
                           {"start_date": {"lte": start_time}, "end_date": {"gte": start_time}},
                           {"end_date": {"gte": end_time, "lte": start_time}}],
                   "isenable": 0
                   }
        if self_flag and self_id:
            filters.update({"id": {"ne": self_id}})
        data = AlarmScheManageResource().list(filters=filters)
        if len(data) > 0:
            time_str = "%s/%s" % (data[0]["start_date"], data[0]["end_date"])
            raise ValidationError("与已有时间段:%s, 冲突" % time_str)


class SendSmsBase(object):
    @staticmethod
    def _arg_model_data():
        define = {
            "phones": {"type": list, "notnull": True, "required": True, "format": {">": 0}},
            "content": {"type": basestring, "notnull": True, "required": True, "format": {">": 0}}
        }
        return define


# TODO 主机组base
class AlarmGroupBase(object):
    @staticmethod
    def _arg_model_data():
        define = {
            "grp_name": {"type": basestring, "notnull": True, "required": True, "format": {">=": 2, "<=": 64}},
            "tenant_id": {"type": basestring, "notnull": True, "required": True, "format": {">": 0, "<=": 32}},
            "project_id": {"type": basestring, "notnull": True, "required": True, "format": {">": 0, "<=": 32}},
            "create_user": {"type": basestring, "notnull": True, "required": True, "format": {">": 0, "<=": 32}}
        }
        return define


# TODO 主机base
class AlarmHostBase(object):
    @staticmethod
    def _arg_model_data():
        define = {
            "groupId": {"type": int, "notnull": True, "required": True, "format": {">": 0, "<=": 10}},
            "hosts": {"type": basestring, "notnull": True, "required": True, "format": {">": 0, "<=": 1024}}
        }

        return define


class EventCaseBase(object):

    @staticmethod
    def _arg_model_data():
        define = {
            "endpoint": {"type": list, "notnull": True, "required": True},
            "endpoint_type": {"type": basestring, "notnull": True, "required": False,
                              "format": {"in": const_define.EndpointType.ALL_TYPE}}
        }
        return define

    def split_cond(self, cond):
        set_value, alert_value = (None, None)
        if cond:
            cond = str(cond)
            regex = re.compile('[><!=]+')
            cond_list = regex.split(cond)
            if len(cond_list) == 2:
                alert_value = cond_list[0].strip()
                set_value = cond.replace(alert_value, '').strip()
        return set_value, alert_value


class EventCaseController(CollectionController, EventCaseBase):
    name = 'alert.event_cases'
    allow_methods = ('POST',)
    resource = alert_api.AlertCaseManageApi

    def on_post(self, req, resp, **kwargs):
        self._validate_method(req)
        checked_data = check_params_with_model(req.json, self._arg_model_data(), keep_extra_key=False)
        endpoint = checked_data['endpoint']
        if not endpoint:
            raise ValidationError("endpoint data not allow empty")
        if endpoint and len(endpoint) > 100:
            raise ValidationError("endpoint data not allow more than 100 item, now item is:%s" % len(endpoint))
        endpoint_type = checked_data.get('endpoint_type', const_define.EndpointType.HOST)
        api = self.make_resource(req)
        refs = api.list(filters={'endpoint': endpoint, 'status': 'PROBLEM'})
        from collections import defaultdict
        endpoint_alert_data = defaultdict(list)
        for info in refs:
            alert_value = info['cond']
            set_value, alert_value = self.split_cond(alert_value)
            new_data = {'Metric': info['metric'], 'Level': info['priority'], 'Timestamp': info['timestamp'],
                        'SetValue': set_value, 'AlertValue': alert_value, 'EndpointType': endpoint_type}
            endpoint_alert_data[info['endpoint']].append(new_data)
        resp.json = {'count': len(endpoint_alert_data), 'data': endpoint_alert_data}


class ShieldListController(CollectionController):
    name = 'alert.shield_list'
    allow_methods = ('GET',)
    resource = alert_api.ShieldListManageApi

    def on_get(self, req, resp, **kwargs):
        self._validate_method(req)
        criteria = self._build_criteria(req)
        try:
            filter_tmp = self.get_maintain_time(copy.deepcopy(criteria["filters"]))
        except Exception as e:
            raise ValidationError(e.message)
        criteria["filters"].update(filter_tmp)
        refs = self.list(req, copy.deepcopy(criteria), **kwargs)
        count = self.count(req, criteria, results=refs, **kwargs)
        if len(refs) > 0:
            user_list = UserManageResource().list()
            user_dict = {user["uid"]: user for user in user_list}
            for ref in refs:
                maintain_begin = ref.get("host", {}).get("maintain_begin", None)
                maintain_end = ref.get("host", {}).get("maintain_end", None)
                owner = ref.get("host", {}).get("maintain_owner", None)
                ref["maintain_owner"] = None
                if maintain_begin is not None:
                    ref["host"]["maintain_begin"] = time_util.timestamp_to_date_str(maintain_begin)
                if maintain_end is not None:
                    ref["host"]["maintain_end"] = time_util.timestamp_to_date_str(maintain_end)
                if owner:
                    ref["maintain_owner"] = user_dict.get(owner) or None
        resp.json = {'count': count, 'data': refs}

    def get_maintain_time(self, filters):
        import time
        time_now = int(time.time())
        start = -1
        maintain_end = {"gte": time_now}
        if isinstance(filters, dict) and filters.has_key('host.maintain_begin'):
            time_begin = time_util.get_timestamp(filters["host.maintain_begin"])
            start = time_begin
        if isinstance(filters, dict) and filters.has_key('host.maintain_end'):
            time_end = time_util.get_timestamp(filters["host.maintain_end"])
            end = time_end if time_end > time_now else time_now
            maintain_end.update({"lte": end})

        filter_tmp = {'host.maintain_begin': {"gte": start},
                      'host.maintain_end': maintain_end}
        return filter_tmp


class AlarmScheController(CollectionController, AlarmScheBase):
    name = 'alert.alarm_sche'
    allow_methods = ('GET', 'POST',)
    resource = alert_api.AlarmScheManageApi

    def on_get(self, req, resp, **kwargs):
        self._validate_method(req)
        criteria = self._build_criteria(req)
        refs = self.list(req, copy.deepcopy(criteria), **kwargs)
        count = self.count(req, criteria, results=refs, **kwargs)
        resp.json = {'count': count, 'data': refs}

    def on_post(self, req, resp, **kwargs):
        self._validate_method(req)
        check_data = req.json
        alarm_sche_api = self.resource()
        data_new = []
        resp_data = []
        # 兼容批量创建逻辑
        if check_data.get("data_list"):
            check_data = check_params_with_model(check_data, self._arg_batch_model_data(), keep_extra_key=False)
            group_type = check_data["group_type"]
            self.check_plan_time(check_data["start_date"], check_data["end_date"], group_type)
            for info in check_data["data_list"]:
                info["group_type"] = group_type
                info_new = check_params_with_model(info, self._arg_model_data(), keep_extra_key=False)
                data_new.append(info_new)

        else:
            info_new = check_params_with_model(check_data, self._arg_model_data(), keep_extra_key=False)
            self.check_plan_time(info_new["start_date"], info_new["end_date"], info_new["group_type"])
            data_new.append(info_new)
        for info_new in data_new:
            resp_info = alarm_sche_api.create(info_new)
            resp_data.append(resp_info)
        resp.json = {'count': len(data_new), 'data': resp_data}


class AlarmScheItemController(ItemController, AlarmScheBase):
    name = 'alert.alarm_sche.item'
    allow_methods = ('GET', 'PATCH', 'DELETE',)
    resource = alert_api.AlarmScheManageApi

    def on_patch(self, req, resp, **kwargs):
        self._validate_method(req)
        alarm_sche_id = kwargs.pop('rid')
        alarm_sche_api = self.make_resource(req)
        alarm_sche_info = alarm_sche_api.get(alarm_sche_id)
        if not alarm_sche_info:
            raise NotFoundError("alarm_sche_id: %s, 不存在" % alarm_sche_id)
        json_data = req.json
        checked_data = check_params_with_model(json_data, self._arg_update_model_data(), keep_extra_key=False)
        group_type = alarm_sche_info["group_type"]
        start_date = checked_data.get("start_date") or alarm_sche_info["start_date"]
        end_date = checked_data.get("end_date") or alarm_sche_info["end_date"]
        if not checked_data:
            resp.json = alarm_sche_info
        else:
            if group_type and start_date and end_date:
                self.check_plan_time(start_date, end_date, group_type, self_flag=True, self_id=alarm_sche_id)
            before, after = alarm_sche_api.update(alarm_sche_id, checked_data)
            resp.json = after

    def on_delete(self, req, resp, **kwargs):
        self._validate_method(req)
        alarm_sche_id = kwargs.pop('rid')
        alarm_sche_api = self.make_resource(req)
        alarm_sche_info = alarm_sche_api.get(alarm_sche_id)
        if not alarm_sche_info:
            raise NotFoundError("alarm_sche_id: %s, 不存在" % alarm_sche_id)
        count, info = alarm_sche_api.delete(alarm_sche_id)
        resp.json = {"count": count, "data": info}


class AlarmListController(CollectionController):
    name = 'alarm.alarm_list'
    allow_methods = ('GET', 'POST')  # 该POST是删除告警
    resource = EventCasesResource

    @tenant_project_func()
    def _build_criteria(self, req, supported_filters=None):
        return super(AlarmListController, self)._build_criteria(req, supported_filters)

    def on_get(self, req, resp, **kwargs):
        """
        处理GET请求

        :param req: 请求对象
        :type req: Request
        :param resp: 相应对象
        :type resp: Response
        """
        self._validate_method(req)
        criteria = self._build_criteria(req)
        filters = criteria.get('filters', {})
        if not req.params.get('project_id'):  # filters.get('project_id'):
            filters.pop('project_id', None)
        status = filters.get('status')
        if status == '0':
            filters['status'] = 'PROBLEM'
        # elif status == '1':
        #     filters['status'] = 'OK'
        # elif status == '2':
        #     filters['status'] = 'DEL'
        else:
            filters['status'] = {'ne': 'PROBLEM'}
        # 默认只显示2类 有新品类时在这里添加
        if not filters.get('source_type'):
            filters['source_type'] = {'in': ['host', 'database','drtask','bakstra']}
        elif filters.get('source_type') == "netline" and filters.get("endpoint"):
            netline_resource = network_manage_api.NetworkSpecialLineApi()
            netline = netline_resource.get(rid=filters['endpoint'])
            filters['source_type'] = "netdev"
            filters['endpoint'] = netline.get("hardware_serial_num")
            filters["$or"] = [{"metric": {"ilike": netline.get("remote_address")}},
                              {"metric": {"ilike": netline.get("local_hardware_interface_name")}}]
        if filters.get('source_type') == "netdev":
            if "project_id" in filters: filters.pop("project_id")
            if "tenant_id" in filters: filters.pop("tenant_id")
        refs = self.list(req, copy.deepcopy(criteria), **kwargs)  #
        count = self.count(req, copy.deepcopy(criteria), results=refs, **kwargs)
        resp.json = {'count': count, 'data': refs}

    def create(self, req, data, **kwargs):
        """
        删除告警 修改告警状态 显示到告警历史列表中
        :param req: 请求对象
        :type req: Request
        :param data: 资源的内容
        :type data: dict
        :returns: 创建后的资源信息
        :rtype: dict
        """
        create_user = req.headers.get("X-AUTH-UID")
        data.update({"create_user": create_user})
        return self.make_resource(req).delete_alarm(data)


class AlarmCountController(CollectionController):
    name = 'alarm.alarm_count'
    allow_methods = ('GET',)
    resource = AlarmCountResource

    def on_get(self, req, resp, **kwargs):
        self._validate_method(req)
        criteria = self._build_criteria(req)
        refs = self.list(req, copy.deepcopy(criteria), **kwargs)
        resp.json = refs

    def list(self, req, criteria, **kwargs):
        criteria = copy.deepcopy(criteria)
        criteria.pop('fields', None)
        refs = self.make_resource(req).list(**criteria)
        return refs


# 资源绑定模板
class AssetTPLController(CollectionController):
    name = 'alarm.alarm_asset_tpl'
    allow_methods = ('GET', 'POST')
    resource = AssetTPLResource

    @tenant_project_func()
    def _build_criteria(self, req, supported_filters=None):
        return super(AssetTPLController, self)._build_criteria(req, supported_filters)

    def on_get(self, req, resp, **kwargs):
        self._validate_method(req)
        criteria = self._build_criteria(req)
        criteria.pop("fields", None)
        resp.json = self.make_resource(req).relation_list(**criteria)

    @set_operate_user_func()
    def create(self, req, data, **kwargs):
        return self.make_resource(req).create(data, operate_flag=True)


# 模板
class AlarmTemplateController(CollectionController):
    name = 'alarm.alarm_tpl'
    allow_methods = ('GET', 'POST')
    resource = TPLManageResource

    @tenant_project_func()
    def _build_criteria(self, req, supported_filters=None):
        return super(AlarmTemplateController, self)._build_criteria(req, supported_filters)

    def on_get(self, req, resp, **kwargs):
        self._validate_method(req)
        criteria = self._build_criteria(req)
        filters = criteria.get('filters', {})
        tpl_type = filters.pop('tpl_type', None)
        search = filters.pop("search", None)
        offset = criteria.get("offset", None)
        limit = criteria.get("limit", None)
        if search:
            filters["tpl_name"] = {"ilike": search}
        # 普通用户查询*
        if (filters.get("admin") == "0" and not filters.get("tenant_admin")) and (
                filters.get("project_id") == "*" or filters.get("tenant_id") == "*"):
            count, refs = 0, []
        # 租户管理员查询*
        elif filters.get("tenant_admin") and (
                filters.get("tenant_id") == "*" or filters.get("project_id") == "*"):
            count, refs = self.resource().get_tenant_tpl(filters, offset, limit)
        # 超管查询*
        elif filters.get("admin") == "1" and (filters.get("tenant_id") == "*" or filters.get("project_id") == "*"):
            count, refs = self.resource().get_produce_tpl(filters, offset, limit)
        else:
            if tpl_type == "parent":
                count, refs = self.resource().get_quick_list()
            else:
                refs = self.list(req, copy.deepcopy(criteria), **kwargs)
                count = self.count(req, copy.deepcopy(criteria), results=refs, **kwargs)
                for ref in refs:
                    if ref["tenant_id"] == ref["project_id"]:
                        ref["project"] = {}
                        ref["project"]["name"] = "*"
                        ref["project"]["desc"] = "租户下所有项目"
                    if ref["tenant_id"] == "*":
                        ref["tenant"] = {}
                        ref["tenant"]["name"] = "*"
                        ref["tenant"]["desc"] = "所有租户"

        resp.json = {'count': count, 'data': refs}

    @set_operate_user_func()
    def create(self, req, data, **kwargs):
        return self.make_resource(req).create(data, operate_flag=True)


# 模板
class AlarmTemplateItemController(ItemController):
    name = 'alarm.alarm_tpl.item'
    allow_methods = ('PATCH', 'DELETE')
    resource = TPLManageResource

    @set_operate_user_func()
    def update(self, req, data, **kwargs):
        rid = kwargs.pop('rid')
        return self.make_resource(req).update(rid, data, operate_flag=True)

    @set_operate_user_func()
    def delete(self, req, **kwargs):
        return self.make_resource(req).delete(**kwargs)


# 模板克隆
class AlarmTemplateCloneController(CollectionController):
    name = 'alarm.alarm_tpl_clone'
    allow_methods = ('POST',)
    resource = TPLManageResource

    @set_operate_user_func()
    def create(self, req, data, **kwargs):
        return self.make_resource(req).clone_tpl(data, operate_flag=True)


# 告警Action
class AlarmTplActionController(CollectionController):
    name = 'alarm.alarm_tpl_action'
    allow_methods = ('POST',)
    resource = ActionManageResource

    @set_operate_user_func()
    def create(self, req, data, **kwargs):
        return self.make_resource(req).create(data, operate_flag=True)


class HostSearchController(CollectionController):
    name = 'alarm.host_search'
    allow_methods = ('GET',)
    resource = HostResource


# 搜索search
class StrategySearchController(CollectionController):
    name = 'alarm.alarm_strategy_search'
    allow_methods = ('GET',)

    def on_get(self, req, resp, **kwargs):
        self._validate_method(req)
        criteria = self._build_criteria(req)
        refs = self.list(req, copy.deepcopy(criteria), **kwargs)
        resp.json = refs

    def list(self, req, criteria, **kwargs):
        filters = criteria.get("filters")
        search = filters.pop("search", None)
        search_type = filters.pop("type", None)
        resp_data = []
        if not search or not search_type:
            return resp_data
        criteria["offset"] = 0
        criteria["limit"] = 20
        if search_type == "host":
            filters["$or"] = [{"exthostname": {"ilike": search}}, {"ip": {"ilike": search}}]
            criteria["fields"] = ["id", "exthostname", "ip"]
            host_list = HostSearchController().list(req, criteria)
            for host in host_list:
                exthostname = host.get("exthostname")
                ip = host.get("ip")
                if not exthostname or not ip:
                    continue
                host_item = {
                    "Id": host.get("id"),
                    "Name": "%s:%s" % (exthostname, ip)
                }
                resp_data.append(host_item)
        elif search_type == "tpl":
            filters["tpl_name"] = {"ilike": search}
            criteria["fields"] = ["id", "tpl_name"]
            tpl_list = AlarmTemplateController().list(req, criteria)
            for tpl in tpl_list:
                tpl_item = {
                    "Id": tpl.get("id"),
                    "Name": tpl.get("tpl_name") or ""
                }
                resp_data.append(tpl_item)
        else:
            return resp_data
        return resp_data


class CounterController(CollectionController):
    name = 'alarm.counter'
    allow_methods = ('GET',)
    resource = CounterManageResource

    def on_get(self, req, resp, **kwargs):
        self._validate_method(req)
        criteria = self._build_criteria(req)
        filters = criteria.get("filters")
        if filters and "asset_id" in filters:
            filters["asset_id"] = {"like": filters["asset_id"]}
        refs = self.list(req, copy.deepcopy(criteria), **kwargs)
        resp.json = refs


# 策略
class AlarmStrategyController(CollectionController, ResourceBase):
    name = 'alarm.alarm_strategy'
    allow_methods = ('GET', 'POST')
    resource_tpl = TPLManageResource
    resource_tpl_host = TPLHostManageResource
    resource = StrategyManageResource
    resource_action = ActionManageResource
    resource_rel_act_user = RelActionUserManageResource
    resource_user = UserManageResource
    resource_strategy_callback = StrategyCallbackManageResource

    @tenant_project_func()
    def _build_criteria(self, req, supported_filters=None):
        return super(AlarmStrategyController, self)._build_criteria(req, supported_filters)

    # 根据tpl_id返回策略
    def _get_strategy_by_tpl_id(self, req, tpl_id, tpl, tenant_id, project_id, callback_url=None, sms_alarm=None,
                                envsMap=None):
        if envsMap is None:
            envsMap = {}
        action_id = tpl.get('action_id', None)
        name = tpl.get('tpl_name', None)
        create_user = tpl.get('create_user', None)
        user_info = self.resource_user().list(filters={'uid': create_user})
        if len(user_info) >= 1:
            user_cnname = user_info[0].get("cnname")
        else:
            user_cnname = ""
        action = self.resource_action().get(action_id)
        callback_url_from = None
        if action:
            if action.get('callback', 0):
                callback_url = action.get('url', None)
                callback_url_from = name
            else:
                callback_url, callback_url_from = self.resource_action().get_parent_action_url_by_tpl(tpl_id)
            sms_alarm = action.get('sms_alarm', None)
            action_id = action.get('id', None)

        rel_action_users = self.resource_rel_act_user().list(filters={'action_id': action_id})
        uic_ids = [action_user['uic_id'] for action_user in rel_action_users]

        user_datas = self.resource_user().list(filters={'uid': {"in": uic_ids}})
        user_list = [{'id': user['id'], 'name': "%s(%s)" % (user['name'], user['cnname']),
                      'cnname': user['cnname'], 'uid': user['uid']} for user in user_datas]
        strategy_filters = {"tpl_id": tpl_id}
        tpl = self.resource_tpl().get(tpl_id)
        if not tpl:
            raise ValidationError("模板ID(%s)不存在" % tpl_id)
        parent_tpl_id = tpl["parent_id"]
        parent_categories = self.make_resource(req).cover_strategy(parent_tpl_id)
        sub_categories = self.make_resource(req).list(filters=strategy_filters)
        datas = self.make_resource(req).count_strategy(parent_categories, sub_categories)
        for data in datas:
            tplInfo = self.resource_tpl().get(data["tpl_id"])
            if tplInfo:
                actionid = tplInfo["action_id"]
                create_user = tplInfo["create_user"]
                tpl_name = tplInfo["tpl_name"]
            else:
                actionid = action_id
                tpl_name = name
            data.pop('tenant')
            data.pop('project')
            data.pop('tenant_id')
            data.pop('project_id')
            data['ActionId'] = actionid
            data['CreateUser'] = create_user
            old_func = data.pop('func')
            func_list = old_func.split("(#")
            data['Fun'] = func_list[0]
            if func_list[0] == "lookup":  # lookup(#2,3)
                tmp_func = func_list[1]
                data['num'] = tmp_func.split(',')[0]
                data['Func'] = tmp_func.split(',')[1][:-1]
            else:
                data['Func'] = func_list[1][:-1]
                data['num'] = ""
            data['Id'] = data.pop('id')
            data['MaxStep'] = data.pop('max_step')
            data['Metric'] = data.pop('metric')
            data['Note'] = data.pop('note')
            data['Op'] = data.pop('op')
            data['Priority'] = data.pop('priority')
            data['RightValue'] = data.pop('right_value')
            data['RunBegin'] = data.pop('run_begin')
            data['RunEnd'] = data.pop('run_end')
            data['Tags'] = data.pop('tags')
            data['tplId'] = data.pop('tpl_id')
            data['Url'] = callback_url
            data['Source'] = data.pop('source')
            data['TplName'] = tpl_name
            envs = data.pop('envs')
            envList = envs.split(',') if envs is not None and envs != "" else []
            data["Envs"] = []
            for env_code in envList:
                if envsMap.get(env_code):
                    data["Envs"].append(envsMap.get(env_code))
        return {
            'CallBackURL': callback_url,
            'CreateUser': user_cnname,
            'Data': datas,
            'Edit': 1,
            'tplId': tpl_id,
            'SmsAlarm': sms_alarm,
            'TplName': name,
            'Uic': user_list,
            'Tenant_id': tenant_id,
            'Project_id': project_id,
            'CallBackURLFrom': callback_url_from
        }

    def on_get(self, req, resp, **kwargs):
        self._validate_method(req)
        criteria = self._build_criteria(req)
        offset = criteria.get("offset")
        limit = criteria.get("limit")
        criteria_filters = criteria.get("filters")
        tenant_filters = criteria_filters.get("tenant_id")
        project_filters = criteria_filters.get("project_id")
        super_admin = False
        if criteria_filters.get("admin") == "1":
            super_admin = True
        admin_flag = False  # 用户门户 忽略header中的项目
        if criteria_filters.get("admin_flag") is False:
            admin_flag = True
        tpl_id = req.params.get('tplId', None)
        host_id = req.params.get('hostId', None)
        hostname = req.params.get('hostname', None)
        # 设备视图 序列号
        if hostname:
            host_info = HostResource().list(filters={"hostname": hostname})
            if len(host_info) >= 1 and not host_id:
                host_id = host_info[0].get("id")
            if not host_id:
                resp.json = []
                return
        if not tpl_id and not host_id:
            raise ValidationError("模板ID或主机ID，必传一个")
        if tpl_id and host_id:
            raise ValidationError("模板ID或主机ID，只传一个")
        res = FalconApiService().get_falcon_api_common("/cloud/v1/envs")
        envs_result = res.get('data', [])
        envs_map = {item.get('code'): item for item in envs_result}
        callback_url = None
        sms_alarm = None
        if tpl_id:
            # 判断是否分页
            page_flag = False
            if isinstance(offset, int) and isinstance(limit, int):
                page_flag = True
            resp_dict = {
                "count": 0,
                "tpl_id": int(tpl_id),
                "data": [],
                "uic": []
            }
            tpl = self.resource_tpl().get(tpl_id)
            if not tpl:
                if page_flag:
                    resp.json = resp_dict
                else:
                    resp.json = []
                return
            tenant_id = tpl.get('tenant_id')
            project_id = tpl.get('project_id')
            # 数据隔离 超管需单独处理
            if not super_admin:
                if admin_flag:  # 云管
                    if tenant_id not in tenant_filters or project_id not in project_filters:
                        if page_flag:
                            resp.json = resp_dict
                        else:
                            resp.json = []
                        return
                else:  # 用户
                    if tenant_id not in tenant_filters:
                        if page_flag:
                            resp.json = resp_dict
                        else:
                            resp.json = []
                        return
            tpl_dict = self._get_strategy_by_tpl_id(req, tpl_id, tpl, tenant_id, project_id, envsMap=envs_map)
            action_id = tpl.get("action_id")
            rel_action_users = self.resource_rel_act_user().list(filters={'action_id': action_id})
            uic_ids = [action_user['uic_id'] for action_user in rel_action_users]
            user_datas = self.resource_user().list(filters={'uid': {"in": uic_ids}})
            user_list = [{'id': user['id'], 'name': "%s(%s)" % (user['name'], user['cnname']),
                          'cnname': user['cnname'], 'uid': user['uid']} for user in user_datas]
            resp_dict["uic"] = user_list

            # 判断是否分页
            if page_flag:
                tmp_strategy_datas = tpl_dict.get("Data")
                strategy_count = len(tmp_strategy_datas)
                resp_dict["count"] = strategy_count
                if strategy_count > 0:
                    # 过滤来源或者优先级
                    source = criteria_filters.get("source")
                    priority = criteria_filters.get("priority")
                    metric = criteria_filters.get("metric")
                    strategy_datas = []
                    if metric or priority or source:
                        for i in tmp_strategy_datas:
                            if source and str(i["tplId"]) != source:
                                continue
                            if priority and str(i["Priority"]) != priority:
                                continue
                            if metric and metric not in str(i["Metric"]):
                                continue
                            strategy_datas.append(i)
                    else:
                        strategy_datas = tmp_strategy_datas
                    if not strategy_datas:
                        resp_dict["count"] = 0
                    else:
                        # 按照策略id降序
                        strategy_datas = sorted(strategy_datas,
                                                key=lambda item: (item["tplId"], item["Id"]),
                                                reverse=True)
                        start_index = offset
                        end_index = offset + limit
                        resp_dict["data"] = strategy_datas[start_index:end_index]
                        resp_dict["count"] = len(strategy_datas)
                resp.json = resp_dict
            else:
                resp.json = [tpl_dict]
        elif host_id:
            all_tpls = []
            host_tpls = self.resource_tpl_host().list(filters={'host_id': host_id})
            for host_tpl in host_tpls:
                tpl_id = host_tpl.get('tpl_id')
                tpl_info = self.resource_tpl().get(tpl_id)
                if not tpl_info:
                    continue
                # 数据隔离
                tenant_id = tpl_info.get("tenant_id")
                project_id = tpl_info.get("project_id")
                if not super_admin:
                    if tenant_id not in tenant_filters or tpl_info.get("project_id") not in project_filters:
                        continue
                action_id = tpl_info['action_id']
                name = tpl_info['tpl_name']
                create_user = tpl_info['create_user']
                user_info = self.resource_user().list(filters={'uid': create_user})
                if len(user_info) >= 1:
                    user_cnname = user_info[0].get("cnname") or ""
                else:
                    user_cnname = ""

                strategy_filters = {"tpl_id": tpl_id}
                parent_tpl_id = tpl_info["parent_id"]
                parent_categories = self.make_resource(req).cover_strategy(parent_tpl_id)
                sub_categories = self.make_resource(req).list(filters=strategy_filters)
                datas = self.make_resource(req).count_strategy(parent_categories, sub_categories)
                for data in datas:
                    tplInfo = self.resource_tpl().get(data["tpl_id"])
                    if tplInfo:
                        actionid = tplInfo["action_id"]
                        create_user = tplInfo["create_user"]
                        tpl_name = tplInfo["tpl_name"]
                    else:
                        actionid = action_id
                        tpl_name = name
                    data.pop('tenant')
                    data.pop('project')
                    data.pop('tenant_id')
                    data.pop('project_id')
                    data['ActionId'] = actionid
                    data['CreateUser'] = create_user
                    old_func = data.pop('func', None)
                    if not old_func:
                        data['num'] = ""
                        data['Func'] = ""
                    else:
                        func_list = old_func.split("(#")
                        data['Fun'] = func_list[0]
                        if func_list[0] == "lookup":  # lookup(#2,3)
                            tmp_func = func_list[1]
                            data['num'] = tmp_func.split(',')[0]
                            data['Func'] = tmp_func.split(',')[1][:-1]
                        else:
                            data['Func'] = func_list[1][:-1]
                            data['num'] = ""
                    data['Id'] = data.pop('id')
                    data['MaxStep'] = data.pop('max_step')
                    data['Metric'] = data.pop('metric')
                    data['Note'] = data.pop('note')
                    data['Op'] = data.pop('op')
                    data['Priority'] = data.pop('priority')
                    data['RightValue'] = data.pop('right_value')
                    data['RunBegin'] = data.pop('run_begin')
                    data['RunEnd'] = data.pop('run_end')
                    data['Tags'] = data.pop('tags')
                    envs = data.pop('envs')
                    envList = envs.split(',') if envs is not None and envs != "" else []
                    data["Envs"] = []
                    for env_code in envList:
                        if envs_map.get(env_code):
                            data["Envs"].append(envs_map.get(env_code))
                    data['tplId'] = data.pop('tpl_id')
                    data['TplName'] = tpl_name
                    data['Url'] = callback_url
                    data['Source'] = data.pop('source')
                action = self.resource_action().get(action_id)
                callback_url_from = ''
                if action:
                    if action.get('callback', 0):
                        callback_url = action.get('url', None)
                        callback_url_from = name
                    else:
                        callback_url, callback_url_from = self.resource_action().get_parent_action_url_by_tpl(tpl_id)
                    sms_alarm = action.get('sms_alarm', None)
                    action_id = action.get('id', None)

                rel_action_users = self.resource_rel_act_user().list(filters={'action_id': action_id})
                uic_ids = [action_user['uic_id'] for action_user in rel_action_users]

                user_datas = self.resource_user().list(filters={'uid': {"in": uic_ids}})
                user_list = [{'id': user['id'], 'name': "%s(%s)" % (user['name'], user['cnname']),
                              'cnname': user['cnname'], 'uid': user['uid']} for user in user_datas]
                each_host_tpl = {
                    'CallBackURL': callback_url,
                    'CreateUser': user_cnname,
                    'Data': datas,
                    'Edit': 1,
                    'tplId': tpl_id,
                    'SmsAlarm': sms_alarm,
                    'TplName': name,
                    'Uic': user_list,
                    'Tenant_id': tenant_id,
                    'Project_id': project_id,
                    'CallBackURLFrom': callback_url_from
                }
                all_tpls.append(each_host_tpl)

            resp.json = all_tpls

    @set_operate_user_func()
    def create(self, req, data, **kwargs):
        return self.make_resource(req).create(data, operate_flag=True)

    def on_post(self, req, resp, **kwargs):
        self._validate_method(req)
        self._validate_data(req)
        check_data = req.json
        occur_num = check_data.pop('func', "")
        func_type = check_data.pop('fun', "")
        if int(occur_num) >= 100:
            if func_type == "lookup":
                raise ValidationError("【采样数量】需要小于100,当前数量为:%s," % occur_num)
            else:
                raise ValidationError("【发生数量】需要小于100,当前数量为:%s," % occur_num)
        show_callback = check_data.pop('showCallback', None)
        if func_type == "lookup":
            tmp_num = check_data.pop('num', "")
            self.make_resource(req).check_lookup(tmp_num, occur_num)
            check_data['func'] = "{}(#{},{})".format(func_type, tmp_num, occur_num)
        else:
            check_data['func'] = func_type + "(#" + str(occur_num) + ")"
        env_enable = check_data.pop('env_enable', None) or 0
        callback = check_data.pop('callbackId', "")
        callback_name = check_data.pop('callbackName', "")
        envs = check_data.pop('envs', [])
        check_data["envs"] = ",".join(envs) if envs and envs[0] else ""
        resp_data = self.create(req, check_data, operate_flag=True)
        new_resp = resp_data
        new_resp['maxStep'] = resp_data.pop('max_step')
        new_resp['TplId'] = resp_data.pop('tpl_id')
        new_resp['runBegin'] = resp_data.pop('run_begin')
        new_resp['rightValue'] = resp_data.pop('right_value')
        new_resp['runEnd'] = resp_data.pop('run_end')
        stg_id = resp_data.get("id")
        callbackId = callbackName = None
        if show_callback:
            try:
                strategy_callback_resource = self.resource_strategy_callback()
                callBackId = callback.split("^")
                callback_id = callback_type = ""
                if len(callBackId) == 2:
                    callback_id = callBackId[0]
                    callback_type = callBackId[1]
                if callback_id and callback_type and stg_id:
                    is_exist = strategy_callback_resource.get(stg_id)
                    if is_exist:
                        strategy_callback_resource.delete(stg_id)
                    callback_data = {
                        "strategy_id": stg_id,
                        "callback_id": callback_id,
                        "callback_name": callback_name,
                        "callback_type": callback_type,
                        "update_at": datetime.datetime.now(),
                        "last_active_time": "2000-01-01 00:00:00",
                        "active_count": 0,
                        "success_count": 0,
                        "env_enable": env_enable
                    }
                    update_user = req.headers.get("X-AUTH-UID")
                    if update_user:
                        callback_data["update_user"] = update_user
                    strategy_callback = strategy_callback_resource.create(callback_data)
                    callbackId = strategy_callback.get('callback_id')
                    callbackName = strategy_callback.get('callback_name')

            except Exception as e:
                LOG.error("insert callback strategy failed(%s)" % e)

        new_resp['callbackId'] = callbackId
        new_resp['callbackName'] = callbackName

        resp.json = new_resp
        resp.status = falcon.HTTP_201


# 策略
class AlarmStrategyItemController(ItemController):
    name = 'alarm.alarm_strategy.item'
    allow_methods = ('PATCH', 'DELETE')
    resource = StrategyManageResource
    resource_stg_callback = StrategyCallbackManageResource

    def on_patch(self, req, resp, **kwargs):
        self._validate_data(req)
        self._validate_method(req)
        stg_id = kwargs.get('rid')
        func_type = req.json.pop('fun', None) or ""
        occur_num = req.json.pop('func', None)
        if int(occur_num) >= 100:
            if func_type == "lookup":
                raise ValidationError("【采样数量】需要小于100,当前数量为:%s," % occur_num)
            else:
                raise ValidationError("【发生数量】需要小于100,当前数量为:%s," % occur_num)
        if func_type == "lookup":
            tmp_num = req.json.pop('num', "")
            self.make_resource(req).check_lookup(tmp_num, occur_num)
            req.json['func'] = "{}(#{},{})".format(func_type, tmp_num, occur_num)
        else:
            req.json['func'] = func_type + "(#" + str(occur_num) + ")"
        update_user = req.headers.get("X-AUTH-UID") or ""
        envs = req.json.pop('envs', []) or []
        req.json['envs'] = ",".join(envs) if envs and envs[0] else ''
        ref_before, ref_after = self.update(req, req.json, **kwargs)
        if ref_after is not None:
            resp.json = ref_after
        else:
            raise NotFoundError(resource=self.resource.__name__)

        # 更新回调工具
        callback_name = req.json.pop('callbackName', None) or ""
        callBackId = req.json.pop('callbackId', None) or ""
        callback_id = callback_type = ""
        callBackId = callBackId.split("^")
        try:
            strategy_callback_resource = self.resource_stg_callback()
            if len(callBackId) == 2:
                callback_id = callBackId[0]
                callback_type = callBackId[1]
            if callback_id and callback_type:
                is_exist = strategy_callback_resource.get(stg_id)
                if is_exist:
                    strategy_callback_resource.delete(stg_id)
                new_stg_callback = {
                    "strategy_id": stg_id,
                    "callback_id": callback_id,
                    "callback_name": callback_name,
                    "callback_type": callback_type,
                    "update_at": datetime.datetime.now(),
                    "update_user": update_user,
                    "last_active_time": "2000-01-01 00:00:00",
                    "active_count": 0,
                    "success_count": 0,
                    "env_enable": req.json.pop('env_enable', 0)
                }
                strategy_callback_resource.create(new_stg_callback)

        except Exception as e:
            LOG.error("update callback strategy failed(%s)" % e)

    @set_operate_user_func()
    def update(self, req, data, **kwargs):
        rid = kwargs.pop('rid')
        return self.make_resource(req).update(rid, data, operate_flag=True)

    @set_operate_user_func()
    def delete(self, req, **kwargs):
        return self.make_resource(req).delete(**kwargs)


'''
class AlarmCustomStrategyController():
    resource_stra = StrategyManageResource
    resource_tpl = TPLManageResource

    def on_post(self, req, resp, **kwargs):
        tenant_id=req.headers['X-AUTH-TENANT']
        project_id=req.headers['X-AUTH-PROJECT']
        custom__ = '__custom_strategy__'
        self.resource_tpl.list(filters={
            'tenant_id':tenant_id,
            'project_id':project_id,
            'tpl_name': custom__
        },limit=1)
        sql_select="select * from tpl where tenant_id=%s and project_id=%s and tpl_name=%s"
        with self.get_session() as session:
            tpl_id=0
            item = session.execute(sql_select,(tenant_id,project_id,custom__,)).fetchone()
            if not item :
                tpl_create = self.resource_tpl.create(
                    resource={'tenant_id': tenant_id, 'project_id': project_id, 'tpl_name': custom__})
                tpl_id=tpl_create['id']
            else:
                tpl_id=item    ['id']
            req_json = req.json()
            req_json['tpl_id']=tpl_id
            AlarmStrategyController().on_post(req,copy.deepcopy(resp))/
            self.resource_stra.create(resource=req_json)
            sql_select_host_id='select h.id from custom c join host h on c.uuid=h.hostname where tenant_id=%s and project_id=%s'
            ids=session.execute(sql_select_host_id,(tenant_id,project_id,)).fetchall()
            sql_insert_tpl_host="insert ignore into tpl_host(tpl_id,host_id) values"+("(%s,%s),"*len(ids)).strip(',')
            session.execute(sql_insert_tpl_host,[tpl_id]*len(ids),[i[0] for i in ids])

'''


# TODO 主机组
class AlarmGroupController(CollectionController, AlarmGroupBase):
    name = 'alarm.alarm_grp'
    allow_methods = ('GET', 'POST')
    resource = GRPManageResource
    resource_user = UserManageResource

    def on_get(self, req, resp, **kwargs):
        self._validate_method(req)
        criteria = self._build_criteria(req)
        filters = criteria.get('filters')
        search_kws = filters.pop('search', None)
        if search_kws:
            filters['grp_name'] = {'ilike': search_kws}

        refs = self.list(req, copy.deepcopy(criteria), **kwargs)
        for ref in refs:
            ref['create_user_id'] = ref['create_user']
            ref['update_user_id'] = ref['update_user']
            c_user = self.resource_user().list(filters={"uid": ref.get("create_user")})
            if c_user:
                ref['create_user'] = c_user[0]
            else:
                ref['create_user'] = None

            u_user = self.resource_user().list(filters={"uid": ref.get("update_user")})
            if u_user:
                ref['update_user'] = u_user[0]
            else:
                ref['update_user'] = None

        count = self.count(req, copy.deepcopy(criteria), results=refs, **kwargs)
        resp.json = {'count': count, 'data': refs}

    def on_post(self, req, resp, **kwargs):
        self._validate_method(req)
        self._validate_data(req)
        check_data = check_params_with_model(req.json, self._arg_model_data(), keep_extra_key=False)
        grp_name = check_data.get('grp_name')
        tenant_id = check_data.get('tenant_id')
        grps = self.resource().list(filters={'grp_name': grp_name, 'tenant_id': tenant_id})
        if len(grps) != 0:
            raise ValidationError("当前主机组名称、租户已存在，请修改名称或重新选择租户")

        resp_data = self.resource().create(check_data)
        resp.json = resp_data
        resp.status = falcon.HTTP_201


# TODO 主机组 ITEM
class AlarmGroupItemController(CollectionController, ItemController):
    name = 'alarm.alarm_grp.item'
    allow_methods = ('GET', 'PATCH', 'DELETE')
    resource = GRPManageResource
    resource_grp_tpl = GRPTplManageResource
    resource_grp_host = GRPHostManageResource

    def on_patch(self, req, resp, **kwargs):
        self._validate_method(req)
        self._validate_data(req)
        grp_name = req.json.get('grp_name')
        update_user = req.json.get('update_user')
        if not grp_name:
            raise ValidationError('模板名称不能为空')
        if not len(grp_name) <= 64 and len(grp_name) >= 2:
            raise ValidationError('模板名称长度需要大于等于2，小于等于64')
        if not update_user:
            raise ValidationError('缺少更新人id')
        ref_before, ref_after = self.update(req, req.json, **kwargs)
        if ref_after is not None:
            resp.json = ref_after
        else:
            raise NotFoundError(resource=self.resource.__name__)

    def on_delete(self, req, resp, **kwargs):
        self._validate_method(req)
        grp_id = kwargs.pop('rid')

        self.resource_grp_host().delete_all(filters={'grp_id': grp_id})
        ref, details = self.resource().delete(grp_id)
        if ref:
            resp.json = {"count": ref, "data": details}
        else:
            raise NotFoundError(resource=self.resource.__name__)


# 资源
class AlarmAssetItemController(CollectionController, ItemController, ResourceBase):
    name = 'alarm.alarm_asset.item'
    allow_methods = ('GET', 'POST', 'DELETE')
    resource = AlarmAssetResource

    @tenant_project_func()
    def _build_criteria(self, req, supported_filters=None):
        return super(AlarmAssetItemController, self)._build_criteria(req, supported_filters)

    def on_get(self, req, resp, **kwargs):
        self._validate_method(req)
        criteria = self._build_criteria(req)
        refs, count = self.resource().asset_result(criteria)
        resp.json = {'count': count, 'data': refs}

    @staticmethod
    def ipv6_validator(ip):
        """
        校验ip是否正确
        :param ip:
        :return:
        """
        try:
            ipaddress.IPv6Address(ensure_unicode(str(ip)))
            return True
        except Exception as e:
            return False

    @staticmethod
    def valid_host_ips(host_ip):
        valid_host_ip_regex = "^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$"
        if not re.match(valid_host_ip_regex, host_ip) and not AlarmAssetItemController.ipv6_validator(host_ip):
            raise ValidationError(message=("非法格式的ip: %s" % host_ip))

    def on_post(self, req, resp, **kwargs):
        self._validate_method(req)
        self._validate_data(req)
        host_ips = req.json.get("hosts")
        tpl_id = req.json.get('tplId')
        # 参数校验
        if not tpl_id:
            raise NotFoundError("tplId为空,请选定至少一个模板")
        old_host_ips_list = re.split('[n,/;_\n\r]+', host_ips)

        ips_list = []
        for input_ip in old_host_ips_list:
            ip = input_ip.replace(' ', '').replace('\n', '').replace('\r', '')
            self.valid_host_ips(ip)
            ips_list.append(str(IPy.IP(ip)))
        if len(ips_list) <= 0:
            raise ValidationError(message=("非法格式的ip: %s" % ips_list))

        uid = req.headers.get("X-AUTH-UID") or ""
        msg = self.resource().add_assets(tpl_id, ips_list, uid, True)
        resp.json = {"code": 0, "msg": msg}

    def on_delete(self, req, resp, **kwargs):
        self._validate_method(req)
        tpl_id = req.params.get('tplId')
        host_ids = req.params.get('hostIds')
        if tpl_id:
            uid = req.headers.get("X-AUTH-UID") or ""
            count, ref = self.resource().delete_assets(tpl_id, host_ids, uid, True)
            resp.json = {"count": count, "data": ref}
        else:
            raise NotFoundError("请选定至少一个模板")


# TODO 项目拉取
class ProjectListController(CollectionController):
    name = 'alarm.project'
    allow_methods = ('GET',)
    resource = ProjectResource

    def on_get(self, req, resp, **kwargs):
        self._validate_method(req)
        criteria = self._build_criteria(req)
        filters = criteria["filters"] if criteria.get("filters") else None
        refs = self.list(req, copy.deepcopy(criteria), **kwargs)
        count = self.count(req, copy.deepcopy(criteria), results=refs, **kwargs)
        if filters:
            if filters.get("name") is not None:
                if filters["name"]["ilike"] == "*":
                    refs = [{"name": "*", "desc": "租户模板", "state": True}]
                    count = len(refs)
        resp.json = {'count': count, 'data': refs}


# 自定义上报
class CustomController(CollectionController, ResourceBase):
    name = 'alarm.custom'
    allow_methods = ('GET', 'POST')
    resource = CustomManageResource
    cmdbHost = HostManageResource
    az = AvailableZoneResource

    @tenant_project_func()
    def _build_criteria(self, req, supported_filters=None):
        return super(CustomController, self)._build_criteria(req, supported_filters)

    def on_get(self, req, resp, **kwargs):
        self._validate_method(req)
        criteria = self._build_criteria(req)
        filters = criteria.get('filters', {})
        exthostname = filters.pop("name", None)
        IPv6FilerConvert.ipv6_filter_convert('ip', filters)
        ip = filters.pop("ip", None)
        env_typ = filters.pop("env", None)
        if exthostname:
            filters["host_info.exthostname"] = exthostname
        if ip:
            filters["host_info.ip"] = converter.IPv6AddressConverter().convert(ip)
        if env_typ:
            filters["env_type"] = env_typ
        filters["host_info.type"] = "custom"  # 防止host表与custom表数据不一致
        refs = self.list(req, copy.deepcopy(criteria), **kwargs)
        count = self.count(req, copy.deepcopy(criteria), results=refs, **kwargs)
        resp.json = {'count': count, 'data': refs}

    @set_operate_user_func()
    def create(self, req, data, **kwargs):
        if not data.get('ip'):
            raise ValidationError(message="ip不能为空")
        hosts = self.cmdbHost().list(filters={'$or': [{"ip": data.get('ip')}, {"ipv6": data.get('ip')}]}, limit=1)
        host = hosts[0] if hosts else None
        if not (host):
            raise ValidationError(message="ip对应主机不存在")
        if not data.get('tenant_id'):
            data['tenant_id'] = host.get('tenant_id') or req.headers.get('X-AUTH-TENANT')
        if not data.get('project_id'):
            data['project_id'] = host.get('project_id') or req.headers.get('X-AUTH-PROJECT')
        if not data.get('region_id'):
            data['region_id'] = host.get('region_id')
        if not data.get('az_id'):
            data['az_id'] = host.get('az_id')
        if not data.get('env_type'):
            data['env_type'] = host.get('env_type')
        if "counter_type" not in data:
            data["counter_type"] = []
        if "counters" not in data:
            data["counters"] = []
        if data.get('az_id'):
            az_list = self.az().list(filters={"id": data['az_id']})
            env_de_az = az_list[0].get('env') if len(az_list) > 0 else None
            if env_de_az:
                data['env_type'] = env_de_az
        if not data.get('env') and not data.get('env_type'):
            raise ValidationError(message="无法获取此可用区的环境")
        return self.make_resource(req).create(data, operate_flag=True)


# 自定义上报
class CustomItemController(ItemController, ResourceBase):
    name = 'alarm.custom.item'
    allow_methods = ('PATCH', 'DELETE')
    resource = CustomManageResource
    cmdbHost = HostManageResource
    az = AvailableZoneResource

    @set_operate_user_func()
    def update(self, req, data, **kwargs):
        rid = kwargs.pop('rid')
        if not rid:
            raise ValidationError(message="rid不能为空")
        if "counter_type" not in data:
            data["counter_type"] = []
        if "counters" not in data:
            data["counters"] = []
        if data.get('az_id'):
            az_list = self.az().list(filters={"id": data['az_id']})
            env_de_az = (az_list[0] or {}).get('env') if len(az_list) > 0 else None
            if env_de_az:
                data['env_type'] = env_de_az
        if not data.get('env') and not data.get('env_type'):
            raise ValidationError(message="无法获取此可用区的环境")
        return self.make_resource(req).update(rid, data, operate_flag=True)

    @set_operate_user_func()
    def delete(self, req, **kwargs):
        return self.make_resource(req).delete(**kwargs)


# 自定义上报告警策略编辑
class CustomActionController(ItemController):
    name = 'alarm.custom.action'
    allow_methods = ('PATCH',)
    resource = CustomStrategyManageResource

    @set_operate_user_func()
    def update(self, req, data, **kwargs):
        rid = kwargs.pop('rid')
        return self.make_resource(req).update(rid, data, operate_flag=True)


class AlarmHistoryListController(CollectionController):
    name = 'alarm.alarm_historylist'
    allow_methods = ('GET',)
    resource = EventsManageResource

    @tenant_project_func(True, "event_cases.tenant_id", "event_cases.project_id")
    def _build_criteria(self, req, supported_filters=None):
        return super(AlarmHistoryListController, self)._build_criteria(req, supported_filters)

    def on_get(self, req, resp, **kwargs):
        """
        处理GET请求

        :param req: 请求对象
        :type req: Request
        :param resp: 相应对象
        :type resp: Response
        """
        self._validate_method(req)
        criteria = self._build_criteria(req)
        filters = criteria.get('filters', {})
        params = {}
        # 替换默认租户和项目过滤参数
        if "tenant_id" in filters:
            filters["event_cases.tenant_id"] = filters.pop("tenant_id")
            # filters.pop("tenant_id")
        if "project_id" in filters:
            filters["event_cases.project_id"] = filters.pop("project_id")
        if not req.params.get("project_id"):
            filters.pop("event_cases.project_id", None)
            # filters.pop("project_id")
        filters['status'] = {'ne': 0}
        if not filters.get('event_cases.source_type'):
            filters['event_cases.source_type'] = {'in': ['host', 'database']}
        elif filters.get('event_cases.source_type') == "netline" and filters.get("event_cases.endpoint"):
            netline_resource = network_manage_api.NetworkSpecialLineApi()
            netline = netline_resource.get(rid=filters['event_cases.endpoint'])
            filters['event_cases.source_type'] = "netdev"
            filters['event_cases.endpoint'] = netline.get("hardware_serial_num")
            filters["$or"] = [{"event_cases.metric": {"ilike": [netline.get("remote_address")]}},
                              {"event_cases.metric": {"ilike": netline.get("local_hardware_interface_name")}}]
        if filters.get('event_cases.source_type') == "netdev":
            if "event_cases.project_id" in filters: filters.pop("event_cases.project_id")
            if "event_cases.tenant_id" in filters: filters.pop("event_cases.tenant_id")
        filters.pop('admin', '')
        filters.pop('admin_flag', '')
        if filters.get('event_cases.endpoint', None):
            start_time = filters.pop('start_time', '')
            end_time = filters.pop('end_time', '')
            filters['single'] = True
            host_ip = filters.pop('host_info.ip', '')
            if start_time and end_time:
                filters["timestamp"] = {
                    "gte": start_time,
                    "lte": end_time,
                }

            if host_ip:
                filters['host.ip'] = {'like': host_ip}
        refs = self.list(req, copy.deepcopy(criteria), **kwargs)
        count = self.count(req, copy.deepcopy(criteria), results=refs, **kwargs)
        resp.json = {'count': count, 'data': refs}


class AlarmNoteController(CollectionController):
    name = 'alarm.alarm_note'
    allow_methods = ('GET', 'POST')
    resource = AlarmNoteResource

    def on_get(self, req, resp, **kwargs):
        """
        处理GET请求

        :param req: 请求对象
        :type req: Request
        :param resp: 相应对象
        :type resp: Response
        """
        self._validate_method(req)
        criteria = self._build_criteria(req)
        filters = criteria.get('filters', {})
        status = filters.get('status')
        timestamp = filters.pop('timestamp', None)
        if (status == '0' or status == 'PROBLEM') and timestamp:
            # 告警列表 PROBLEM
            filters['timestamp'] = {'gt': timestamp}
        uid = req.headers.get("X-AUTH-UID") or ""
        criteria.update({"uid_flag": uid})
        refs = self.list(req, copy.deepcopy(criteria), **kwargs)
        count = len(refs)  # 认领记录不会分页可以这么写
        resp.json = {'count': count, 'data': refs}

    def create(self, req, data, **kwargs):
        """
        告警认领 备注信息
        :param req: 请求对象
        :type req: Request
        :param data: 资源的内容
        :type data: dict
        :returns: 创建后的资源信息
        :rtype: dict
        """
        create_user = req.headers.get("X-AUTH-UID")
        data.update({"creator": create_user})
        return self.make_resource(req).create(data)


# 自定义模板
class TplController(CollectionController):
    name = 'alarm.tpl'
    allow_methods = ('GET', 'POST')
    resource = TPLManageResource
    resource_tpl_host = TPLHostManageResource

    @set_operate_user_func()
    def create(self, req, data, **kwargs):
        host_id = data.get("host_id")
        host_info = self.make_resource(req).get_host_data(host_id)
        data["exthostname"] = host_info[0]
        data["tenant_id"] = host_info[1]
        data["project_id"] = host_info[2]
        tpl_item = self.make_resource(req).create(data, operate_flag=True)
        tpl_id = tpl_item["id"]
        # tpl_host表中增加一条模板记录
        tpl_host = {"tpl_id": tpl_id, "host_id": host_id}
        self.resource_tpl_host().create(tpl_host)
        return tpl_item


class TplItemController(ItemController):
    name = 'alarm.tpl.item'
    allow_methods = ('DELETE',)
    resource = TPLManageResource

    @set_operate_user_func()
    def delete(self, req, **kwargs):
        return self.make_resource(req).delete(**kwargs)
