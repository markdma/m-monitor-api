# coding: utf-8
import copy

from monitor.apps.monitor_env.api import module_api
from monitor.apps.monitor_env.dbresources.resource import EnvironmentManageResource
from monitor.apps.host_report.api import az_api
from monitor.common.controller import CollectionController, ItemController, ResourceInterface
from monitor.core.exceptions import ValidationError, NotFoundError
from monitor.lib.validation import check_params_with_model


class ModuleBase(object):

    @staticmethod
    def _arg_model_update_data():
        base_define = {
            "env": {"type": basestring, "notnull": True, "required": True, "format": {">": 0, "<": 37}}
        }
        return base_define

    def checked_env(self, env):
        if env:
            env_type_info = EnvironmentManageResource().get(env)
            if not env_type_info:
                raise ValidationError("环境类型不存在")


class ModuleManageController(CollectionController):
    name = 'monitor.module'
    allow_methods = ('GET',)
    resource = module_api.ModuleManageApi

    def on_get(self, req, resp, **kwargs):
        self._validate_method(req)
        criteria = self._build_criteria(req)
        refs = self.list(req, copy.deepcopy(criteria), **kwargs)
        count = self.count(req, criteria, results=refs, **kwargs)
        resp.json = {'count': count, 'data': refs}


class ModuleManageItemController(ItemController, ModuleBase):
    name = 'monitor.module.item'
    allow_methods = ('GET', 'PATCH')
    resource = module_api.ModuleManageApi

    def on_get(self, req, resp, **kwargs):
        module_id = kwargs.pop('rid')
        module_api = self.make_resource(req)
        module_info = module_api.get(module_id)
        if not module_info:
            raise NotFoundError("module id:%s不存在" % module_id)
        resp.json = module_info

    def on_patch(self, req, resp, **kwargs):
        module_id = kwargs.pop('rid')
        module_api = self.make_resource(req)
        module_info = module_api.get(module_id)
        if not module_info:
            raise NotFoundError("module id:%s不存在" % module_id)
        checked_data = check_params_with_model(req.json, self._arg_model_update_data(), keep_extra_key=False)
        if not checked_data:
            resp.json = module_info
        else:
            self.checked_env(checked_data.get("env", None))
            module_api.update(module_id, checked_data)
            resp.json = module_api.get(module_id)
