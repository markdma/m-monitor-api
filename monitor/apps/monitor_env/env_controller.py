# coding: utf-8
import copy

from monitor.apps.host_manage.dbresources.resource import EnvironmentManageResource
from monitor.apps.monitor_env.api import env_api
from monitor.common.controller import CollectionController, ItemController
from monitor.core.exceptions import ValidationError, NotFoundError, ConflictError
from monitor.lib.validation import check_params_with_model


class EnvironmentBase(object):

    @staticmethod
    def _arg_model_data():
        base_define = {
            "id": {"type": basestring, "notnull": True, "required": True, "format": {">": 0, "<": 37}},
            "enabled": {"type": int, "notnull": False, "required": False, "format": {"in": [0, 1]}},
            "name": {"type": basestring, "notnull": True, "required": True, "format": {">": 0, "<": 255}},
            "gateway": {"type": basestring, "notnull": False, "required": False, "format": {">=": 0, "<": 256}},
            "graph": {"type": basestring, "notnull": False, "required": False, "format": {">=": 0, "<": 256}},
            "dashboard": {"type": basestring, "notnull": False, "required": False, "format": {">=": 0, "<": 256}},
            "tsdb": {"type": basestring, "notnull": False, "required": False, "format": {">=": 0, "<": 256}},
        }
        return base_define

    @staticmethod
    def _arg_model_update_data():
        base_define = {
            "enabled": {"type": int, "notnull": False, "required": False, "format": {"in": [0, 1]}},
            "name": {"type": basestring, "notnull": True, "required": False, "format": {">=": 0, "<": 256}},
            "gateway": {"type": basestring, "notnull": False, "required": False, "format": {">=": 0, "<": 256}},
            "graph": {"type": basestring, "notnull": False, "required": False, "format": {">=": 0, "<": 256}},
            "dashboard": {"type": basestring, "notnull": False, "required": False, "format": {">=": 0, "<": 256}},
            "tsdb": {"type": basestring, "notnull": False, "required": False, "format": {">=": 0, "<": 256}},
        }
        return base_define
    
    def check_existed_env(self, env_id):
        existed = False
        if env_id:
            env_type_info = EnvironmentManageResource().get(env_id)
            if env_type_info:
                existed = True
        return existed


class EnvironmentManageController(CollectionController, EnvironmentBase):
    name = 'monitor.environment'
    allow_methods = ('GET', 'POST')
    resource = env_api.EnvironmentManageApi

    def on_get(self, req, resp, **kwargs):
        self._validate_method(req)
        criteria = self._build_criteria(req)
        refs = self.list(req, copy.deepcopy(criteria), **kwargs)
        count = self.count(req, criteria, results=refs, **kwargs)
        resp.json = {'count': count, 'data': refs}

    def create(self, req, data, **kwargs):
        data = check_params_with_model(req.json, self._arg_model_data(), keep_extra_key=False)
        existed = self.check_existed_env(data['id'])
        if existed:
            raise ConflictError("该id已存在: %s" % data['id'])
        return self.make_resource(req).create(data)


class EnvironmentManageItemController(ItemController, EnvironmentBase):
    name = 'monitor.environment.item'
    allow_methods = ('GET', 'PATCH', 'DELETE')
    resource = env_api.EnvironmentManageApi

    def on_get(self, req, resp, **kwargs):
        env_id = kwargs.pop('rid')
        env_api = self.make_resource(req)
        env_info = env_api.get(env_id)
        if not env_info:
            raise NotFoundError("environment id:%s不存在" % env_id)
        resp.json = env_info

    def on_patch(self, req, resp, **kwargs):
        env_id = kwargs.pop('rid')
        env_api = self.make_resource(req)
        env_info = env_api.get(env_id)
        if not env_info:
            raise NotFoundError("environment id:%s不存在" % env_id)
        checked_data = check_params_with_model(req.json, self._arg_model_update_data(), keep_extra_key=False)
        if not checked_data:
            resp.json = env_info
        else:
            if isinstance(checked_data, dict):
                if checked_data.has_key("gateway") and checked_data["gateway"] is None:
                    checked_data["gateway"] = ""
                if checked_data.has_key("graph") and checked_data["graph"] is None:
                    checked_data["graph"] = ""
                if checked_data.has_key("dashboard") and checked_data["dashboard"] is None:
                    checked_data["dashboard"] = ""
                if checked_data.has_key("tsdb") and checked_data["tsdb"] is None:
                    checked_data["tsdb"] = ""
            env_api.update(env_id, checked_data)
            resp.json = env_api.get(env_id)

    def on_delete(self, req, resp, **kwargs):
        env_id = kwargs.pop('rid')
        env_api = self.make_resource(req)
        env_info = env_api.get(env_id)
        if not env_info:
            raise NotFoundError("environment id:%s不存在" % env_id)
        count, data = env_api.delete(env_id)
        resp.json = {'count': count, 'data': data}