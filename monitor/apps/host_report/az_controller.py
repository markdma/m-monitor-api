# coding: utf-8
import copy

from monitor.apps.monitor_env.dbresources.resource import EnvironmentManageResource
from monitor.apps.host_report.api import az_api
from monitor.common.controller import CollectionController, ItemController
from monitor.core.exceptions import ValidationError, NotFoundError
from monitor.lib.validation import check_params_with_model


class AvailableZoneBase(object):

    @staticmethod
    def _arg_model_sync_data():
        base_define = {
            "data": {"type": list, "notnull": False, "required": False},
            "model": {"type": basestring, "notnull": True, "required": True, "format": {"in": ["update", "insert", "auto", "batch_update"]}},
            "batch_dict": {"type": dict, "notnull": False, "required": False},
            "filters": {"type": dict, "notnull": False, "required": False}
        }
        return base_define

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


class AvailableZoneController(CollectionController):
    name = 'monitor.available_zone'
    allow_methods = ('GET',)
    resource = az_api.AvailableZoneApi

    def on_get(self, req, resp, **kwargs):
        self._validate_method(req)
        criteria = self._build_criteria(req)
        refs = self.list(req, copy.deepcopy(criteria), **kwargs)
        count = self.count(req, criteria, results=refs, **kwargs)
        resp.json = {'count': count, 'data': refs}


class AvailableZoneItemController(ItemController, AvailableZoneBase):
    name = 'monitor.available_zone.item'
    allow_methods = ('GET', 'PATCH')
    resource = az_api.AvailableZoneApi

    def on_get(self, req, resp, **kwargs):
        az_id = kwargs.pop('rid')
        az_api = self.make_resource(req)
        az_info = az_api.get(az_id)
        if not az_info:
            raise NotFoundError("az id:%s不存在" % az_id)
        resp.json = az_info

    def on_patch(self, req, resp, **kwargs):
        az_id = kwargs.pop('rid')
        az_api = self.make_resource(req)
        az_info = az_api.get(az_id)
        if not az_info:
            raise NotFoundError("az id:%s不存在" % az_id)
        checked_data = check_params_with_model(req.json, self._arg_model_update_data(), keep_extra_key=False)
        if not checked_data:
            resp.json = az_info
        else:
            self.checked_env(checked_data.get("env", None))
            az_api.update(az_id, checked_data)
            resp.json = az_api.get(az_id)


# class AvailableZoneBatchSyncController(ResourceInterface):
#     name = 'monitor.available_zone.batch_sync'
#     allow_methods = ('PATCH',)
#     resource = az_api.AvailableZoneApi

