# coding: utf-8
import copy

import falcon

from monitor.apps.monitor_env.dbresources.resource import EnvironmentManageResource
from monitor.apps.network_manage.api import network_manage_api
from monitor.apps.network_manage.dbresources.resource import HardwareModelOidsResource, HardwareModelResource
from monitor.common.controller import CollectionController, ItemController, ResourceInterface
from monitor.core.exceptions import NotFoundError, ValidationError
from monitor.lib.redis_lib import RedisForCommon
from monitor.lib.validation import check_params_with_model


class NetworkSpecialLineManageBase(object):

    def _arg_model_update_data(self):
        define = {
            "enabled": {"type": int, "notnull": True, "required": False, "format": {"in": [0, 1]}},
            "is_use_vpn": {"type": int, "notnull": True, "required": False, "format": {"in": [0, 1]}}
                           }
        return define

    def checked_env_type(self, env_type_id):
        if env_type_id:
            env_type_info = EnvironmentManageResource().get(env_type_id)
            if not env_type_info:
                raise ValidationError("env不存在")


class NetworkDeviceManageBase(object):

    def _arg_model_update_data(self):
        define = {
            "env": {"type": basestring, "notnull": False, "required": False, "format": {">": 0, "<": 37}},
            "community": {"type": basestring, "notnull": False, "required": False, "format": {">": 0, "<": 101}},
            "enabled": {"type": int, "notnull": True, "required": False, "format": {"in": [0, 1]}},
            "snmp_port": {"type": int, "notnull": False, "required": False, "format": {">": 0, "<": 65536}}
        }
        return define

    def checked_env_type(self, env_type_id):
        if env_type_id:
            env_type_info = EnvironmentManageResource().get(env_type_id)
            if not env_type_info:
                raise ValidationError("env不存在")


class HardwareModelOidsManageBase(object):

    def _arg_model_create_data(self):
        define = {
            "hardware_model_id": {"type": basestring, "notnull": True, "required": True, "format": {">": 0, "<": 12}},
            "metric": {"type": basestring, "notnull": True, "required": True, "format": {">": 0, "<": 51}},
            "oid": {"type": basestring, "notnull": True, "required": True, "format": {">": 0, "<": 256}},
            "oid_type": {"type": basestring, "notnull": True, "required": False, "format": {">": 0, "<": 256}},
            "metric_type": {"type": basestring, "notnull": True, "required": False, "format": {">": 0, "<": 256}},
            "description": {"type": basestring, "notnull": False, "required": False, "format": {">": 0, "<": 100}},
            "calculate_type": {"type": basestring, "notnull": False, "required": False, "format": {">=": 0, "<": 32}},
            "calculate_oid": {"type": basestring, "notnull": False, "required": False, "format": {">=": 0, "<": 256}},
        }
        return define

    def _arg_model_update_data(self):
        define = {
            "metric": {"type": basestring, "notnull": True, "required": False, "format": {">": 0, "<": 51}},
            "oid": {"type": basestring, "notnull": True, "required": False, "format": {">": 0, "<": 256}},
            "oid_type": {"type": basestring, "notnull": True, "required": False, "format": {">": 0, "<": 256}},
            "metric_type": {"type": basestring, "notnull": True, "required": False, "format": {">": 0, "<": 256}},
            "description": {"type": basestring, "notnull": False, "required": False, "format": {">": 0, "<": 100}},
            "calculate_type": {"type": basestring, "notnull": False, "required": False, "format": {">=": 0, "<": 32}},
            "calculate_oid": {"type": basestring, "notnull": False, "required": False, "format": {">=": 0, "<": 256}},
        }
        return define

    def check_hardware_model_id(self, hardware_model_id):
        if not hardware_model_id:
            raise ValidationError("hardware model id不能为空")
        hardware_model_info = HardwareModelResource().get(hardware_model_id)
        if not hardware_model_info:
            raise ValidationError("hardware model id: %s不存在" % hardware_model_id)
        model = hardware_model_info.get('name', None)
        if not model:
            raise ValidationError("hardware model id: %s, 没有录入model" % hardware_model_id)
        return model

    def check_network_device_metric(self, metric, model_id, self_oid_id=None):
        if self_oid_id:
            oid_list = HardwareModelOidsResource().list(
                filters={'metric': metric, 'model_id': model_id, 'is_deleted': 0, 'id': {'ne': self_oid_id}})
        else:
            oid_list = HardwareModelOidsResource().list(filters={'metric': metric, 'model': model_id, 'is_deleted': 0})
        if len(oid_list) > 0:
            raise ValidationError("该model与metric组合已存在")


class NetworkSpecialLineController(CollectionController, NetworkSpecialLineManageBase):
    name = 'monitor.network_special_line'
    allow_methods = ('GET',)
    resource = network_manage_api.NetworkSpecialLineApi

    redisclient = RedisForCommon.get_instance_for_common_1()

    Netline_status_key = 'netline.status'
    Netline_ping_key = 'netline.ping'
    Netline_in_octet_key = 'netline.in.octet'
    Netline_out_octet_key = 'netline.out.octet'

    def on_get(self, req, resp, **kwargs):
        def get_custom_order(field, orders, map):
            temp = {}
            for i in map.keys():
                if map.get(i):
                    temp[i] = float(map[i])
                else:
                    temp[i] = map.get(i)
            field_order = []
            sort_id = []
            if "-" + field in orders:
                orders.remove("-" + field)
                field_order = sorted(temp.items(), key=lambda x: (x[1]), reverse=True)
            if "+" + field in orders:
                orders.remove("+" + field)
                field_order = sorted(temp.items(), key=lambda x: (x[1]))
            empty_field = []
            for index, t in enumerate(field_order):
                if not temp.get(t[0]):
                    empty_field.append(t[0])
                else:
                    sort_id.append(t[0])
            for item in empty_field:
                sort_id.append(item)
            return sort_id

        def get_custom_field(field, dist_item, request, value):
            fields = request.get("fields")
            if not fields or field in fields:
                dist_item[field] = value

        self._validate_method(req)
        criteria = self._build_criteria(req)
        ping_map = self.redisclient.hgetall(self.Netline_ping_key)
        statusMap = self.redisclient.hgetall(self.Netline_status_key)
        inOctetMap = self.redisclient.hgetall(self.Netline_in_octet_key)
        outOctetMap = self.redisclient.hgetall(self.Netline_out_octet_key)
        filters = criteria.get("filters")
        search = filters.get("search")
        orders = criteria.get('orders')
        sort_id = []
        offset = None
        limit = None
        if orders:
            sort_id = get_custom_order("ping", orders, ping_map) if not sort_id else sort_id
            sort_id = get_custom_order("net_in_octet", orders, inOctetMap) if not sort_id else sort_id
            sort_id = get_custom_order("net_out_octet", orders, outOctetMap) if not sort_id else sort_id
        if sort_id and sort_id[0]:
            offset = criteria.pop("offset")
            limit = criteria.pop("limit")
        search_list = []

        if filters and isinstance(filters, dict):
            statusList = []
            searchStatus = filters.get("status")
            if searchStatus:
                if isinstance(searchStatus, list):
                    statusList = [item for item in searchStatus]
                else:
                    statusList.append(searchStatus)
                for key, value in statusMap.items():
                    if value in statusList:
                        search_list.append(key)
                filters.update({"id": {"in": search_list}})
        if search:
            filters["$or"] = [{"name": {"ilike": search}}, {"remote_address": {"ilike": search}},
                              {"sw_iprange.iprange": {"ilike": search}}]
        refs = self.list(req, copy.deepcopy(criteria), **kwargs)
        if sort_id and sort_id[0]:
            temp = {item.get("id"): item for item in refs}
            refs = []
            for wan_id in sort_id:
                if temp.get(wan_id):
                    refs.append(temp.get(wan_id))
            if limit is None or limit == 0:
                limit = len(refs) - 1
            refs = refs[offset:offset + limit]
        for item in refs:
            wan_id = item.get("id")
            get_custom_field("ping", item, criteria, ping_map.get(wan_id))
            get_custom_field("status", item, criteria, statusMap.get(wan_id, 0))
            get_custom_field("net_in_octet", item, criteria, inOctetMap.get(wan_id))
            get_custom_field("net_out_octet", item, criteria, outOctetMap.get(wan_id))

        count = self.count(req, criteria, results=refs, **kwargs)
        resp.json = {'count': count, 'data': refs}


class NetworkSpecialLineItemController(ItemController, NetworkSpecialLineManageBase):
    name = 'monitor.network_special_line.item'
    allow_methods = ('PATCH', 'GET')
    resource = network_manage_api.NetworkSpecialLineApi

    def on_patch(self, req, resp, **kwargs):
        network_line_id = kwargs.pop('rid')
        network_line_api = self.make_resource(req)
        network_line_info = network_line_api.get(network_line_id)
        if not network_line_info:
            raise NotFoundError("netline id:%s不存在" % network_line_id)
        checked_data = check_params_with_model(req.json, self._arg_model_update_data(), keep_extra_key=False)
        if not checked_data:
            resp.json = network_line_info
        else:
            network_line_api.update(network_line_id, checked_data)
            resp.json = network_line_api.get(network_line_id)

    def on_get(self, req, resp, **kwargs):
        network_line_id = kwargs.pop('rid')
        network_line_api = self.make_resource(req)
        network_line_info = network_line_api.get(network_line_id)
        if not network_line_info:
            raise NotFoundError("netline id:%s不存在" % network_line_id)
        resp.json = network_line_info


class NetworkDeviceController(CollectionController, NetworkDeviceManageBase):
    name = 'monitor.network_device'
    allow_methods = ('GET',)
    resource = network_manage_api.NetworkDeviceApi
    redisclient = RedisForCommon.get_instance_for_common_1()

    Network_status_key = 'network.status'
    Network_rtt_key = 'network.rtt'

    def on_get(self, req, resp, **kwargs):
        self._validate_method(req)
        criteria = self._build_criteria(req)
        filters = criteria.get("filters")
        search = filters.get("search")
        if search:
            filters["$or"] = [{"name": {"ilike": search}}, {"iprange": {"ilike": search}}]
        orders = criteria.get('orders')
        ping_map = self.redisclient.hgetall((filters.get("catalog") or "network") + ".rtt")
        statusMap = self.redisclient.hgetall((filters.get("catalog") or "network") + ".status")
        ping_order = []
        limit = None
        offset = None
        sort_serial_num = []
        if orders:
            temp = {}
            for i in ping_map.keys():
                if ping_map.get(i):
                    temp[i] = float(ping_map[i])
                else:
                    temp[i] = ping_map.get(i)
            if "-ping" in orders:
                orders.remove("-ping")
                ping_order = sorted(temp.items(), key=lambda x: x[1], reverse=True)
            if "+ping" in orders:
                orders.remove("+ping")
                ping_order = sorted(temp.items(), key=lambda x: x[1])
            empty_field = []
            for index, t in enumerate(ping_order):
                if not temp.get(t[0]):
                    empty_field.append(t[0])
                else:
                    sort_serial_num.append(t[0])
            for item in empty_field:
                sort_serial_num.append(item)
        if sort_serial_num and sort_serial_num[0]:
            offset = criteria.pop("offset")
            limit = criteria.pop("limit")
        search_list = []
        if filters and isinstance(filters, dict):
            statusList = []
            searchStatus = filters.get("status")
            if searchStatus:
                if isinstance(searchStatus, list):
                    statusList = [item for item in searchStatus]
                else:
                    statusList.append(searchStatus)
                for key, value in statusMap.items():
                    if value in statusList:
                        search_list.append(key)
                filters.update({"serial_num": {"in": search_list}})

        refs = self.list(req, copy.deepcopy(criteria), **kwargs)
        if sort_serial_num and sort_serial_num[0]:
            temp = {item.get("serial_num"): item for item in refs}
            refs = []
            for serial_num in sort_serial_num:
                if temp.get(serial_num):
                    refs.append(temp.get(serial_num))
            if limit is None or limit == 0:
                limit = len(refs) - 1
            refs = refs[offset:offset + limit]
        for item in refs:
            if not criteria.get("fields") or "ping" in criteria.get("fields"):
                item["ping"] = ping_map.get(item.get("serial_num"), 0)
            if not criteria.get("fields") or "status" in criteria.get("fields"):
                item["status"] = statusMap.get(item.get("serial_num"), 0)
        count = self.count(req, criteria, results=refs, **kwargs)
        resp.json = {'count': count, 'data': refs}


class NetworkDeviceItemController(ItemController, NetworkDeviceManageBase):
    name = 'monitor.network_device.item'
    allow_methods = ('PATCH', 'GET')
    resource = network_manage_api.NetworkDeviceApi
    redisclient = RedisForCommon.get_instance_for_common_1()
    Network_status_key = 'network.status'
    Network_rtt_key = 'network.rtt'

    def on_patch(self, req, resp, **kwargs):
        network_device_id = kwargs.pop('rid')
        network_device_api = self.make_resource(req)
        network_device_info = network_device_api.get(network_device_id)
        if not network_device_info:
            raise NotFoundError("network device id:%s不存在" % network_device_id)
        checked_data = check_params_with_model(req.json, self._arg_model_update_data(), keep_extra_key=True)
        if not checked_data:
            resp.json = network_device_info
        else:
            self.checked_env_type(checked_data.get("env", None))
            network_device_api.update(network_device_id, checked_data)
            resp.json = network_device_api.get(network_device_id)

    def on_get(self, req, resp, **kwargs):
        criteria = self._build_criteria(req)
        network_device_id = kwargs.pop('rid')
        filters = criteria.get("filters", {})
        ping_map = self.redisclient.hgetall((filters.get("catalog") or "network") + ".rtt")
        statusMap = self.redisclient.hgetall((filters.get("catalog") or "network") + ".status")
        network_device_api = self.make_resource(req)
        network_device_info = network_device_api.get(network_device_id)
        if not network_device_info:
            raise NotFoundError("network device id:%s不存在" % network_device_id)
        if not criteria.get("fields") or "ping" in criteria.get("fields"):
            network_device_info["ping"] = ping_map.get(network_device_info.get("serial_num"), 0)
        if not criteria.get("fields") or "status" in criteria.get("fields"):
            network_device_info["status"] = statusMap.get(network_device_info.get("serial_num"), 0)
        resp.json = network_device_info


class HardwareModelOidsController(CollectionController, HardwareModelOidsManageBase):
    name = 'monitor.hardware_model.oids'
    allow_methods = ('GET', 'POST')
    resource = network_manage_api.HardwareModelOidsApi

    def on_get(self, req, resp, **kwargs):
        self._validate_method(req)
        criteria = self._build_criteria(req)
        refs = self.list(req, copy.deepcopy(criteria), **kwargs)
        count = self.count(req, criteria, results=refs, **kwargs)
        resp.json = {'count': count, 'data': refs}

    def on_post(self, req, resp, **kwargs):
        self._validate_method(req)
        checked_data = check_params_with_model(req.json, self._arg_model_create_data(), keep_extra_key=False)
        hardware_model_id =  checked_data.pop('hardware_model_id', None)
        model = self.check_hardware_model_id(hardware_model_id)
        checked_data.update({'model': model,"model_id": int(hardware_model_id)})
        self.check_network_device_metric(checked_data['metric'], hardware_model_id)
        network_device_oid_api = self.make_resource(req)
        resp.status = falcon.HTTP_201
        resp.json = network_device_oid_api.create(checked_data)


class HardwareModelOidsItemController(ItemController, HardwareModelOidsManageBase):
    name = 'monitor.hardware_model.oids.item'
    allow_methods = ('PATCH', 'GET', 'DELETE')
    resource = network_manage_api.HardwareModelOidsApi

    def on_patch(self, req, resp, **kwargs):
        network_device_oid_id = kwargs.pop('rid')
        network_device_oid_api = self.make_resource(req)
        network_device_oid_info = network_device_oid_api.get(network_device_oid_id)
        if not network_device_oid_info:
            raise NotFoundError("network device oid id:%s不存在" % network_device_oid_id)
        checked_data = check_params_with_model(req.json, self._arg_model_update_data(), keep_extra_key=False)
        if not checked_data:
            resp.json = network_device_oid_info
        else:
            if checked_data.get('metric', None):
                self.check_network_device_metric(checked_data['metric'], network_device_oid_info['model_id'],
                                                 self_oid_id=network_device_oid_id)
            network_device_oid_api.update(network_device_oid_id, checked_data)
            resp.json = network_device_oid_api.get(network_device_oid_id)

    def on_get(self, req, resp, **kwargs):
        network_device_oid_id = kwargs.pop('rid')
        network_device_oid_api = self.make_resource(req)
        network_device_oid_info = network_device_oid_api.get(network_device_oid_id)
        if not network_device_oid_info or network_device_oid_info['is_deleted'] == 1:
            raise NotFoundError("network device oid id:%s不存在" % network_device_oid_id)
        resp.json = network_device_oid_info

    def on_delete(self, req, resp, **kwargs):
        network_device_oid_id = kwargs.pop('rid')
        network_device_oid_api = self.make_resource(req)
        network_device_oid_info = network_device_oid_api.get(network_device_oid_id)
        if not network_device_oid_info:
            raise NotFoundError("network device oid id:%s不存在" % network_device_oid_id)
        ref, details = network_device_oid_api.delete(network_device_oid_id)
        resp.json = {'count': ref, 'data': details}


class NetPodsManageController(CollectionController):
    name = 'monitor.net_pods'
    allow_methods = ('GET',)
    resource = network_manage_api.NetPodsManageApi

    def on_get(self, req, resp, **kwargs):
        self._validate_method(req)
        criteria = self._build_criteria(req)
        refs = self.list(req, copy.deepcopy(criteria), **kwargs)
        count = self.count(req, criteria, results=refs, **kwargs)
        resp.json = {'count': count, 'data': refs}


class NetPodsBatchSyncController(ResourceInterface):
    name = 'monitor.net_pods.batch_sync'
    allow_methods = ('PATCH',)
    resource = network_manage_api.NetPodsManageApi


class NetSubsManageController(CollectionController):
    name = 'monitor.net_subs'
    allow_methods = ('GET',)
    resource = network_manage_api.NetSubsManageApi

    def on_get(self, req, resp, **kwargs):
        self._validate_method(req)
        criteria = self._build_criteria(req)
        refs = self.list(req, copy.deepcopy(criteria), **kwargs)
        count = self.count(req, criteria, results=refs, **kwargs)
        resp.json = {'count': count, 'data': refs}


class NetSubsBatchSyncController(ResourceInterface):
    name = 'monitor.net_subs.batch_sync'
    allow_methods = ('PATCH',)
    resource = network_manage_api.NetSubsManageApi


class NetworkRelsManageController(CollectionController):
    name = 'monitor.network_rels'
    allow_methods = ('GET',)
    resource = network_manage_api.NetworkRelsManageApi

    def on_get(self, req, resp, **kwargs):
        self._validate_method(req)
        criteria = self._build_criteria(req)
        refs = self.list(req, copy.deepcopy(criteria), **kwargs)
        count = self.count(req, criteria, results=refs, **kwargs)
        resp.json = {'count': count, 'data': refs}


class NetworkRelsBatchSyncController(ResourceInterface):
    name = 'monitor.network_rels.batch_sync'
    allow_methods = ('PATCH',)
    resource = network_manage_api.NetworkRelsManageApi
