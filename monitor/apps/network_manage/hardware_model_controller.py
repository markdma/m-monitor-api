# coding: utf-8
import copy

from monitor.apps.network_manage.api import hardware_model_api
from monitor.apps.network_manage.dbresources.resource import HardwareModelOidsResource
from monitor.common.controller import CollectionController, ItemController, ResourceInterface
from monitor.core.exceptions import NotFoundError


class HardwareModelBase(object):

    def get_oid_list(self, hardware_model_id):
        oid_list = HardwareModelOidsResource().list(filters={'is_deleted': 0, 'model_id': hardware_model_id})
        return oid_list

    def get_all_oid_dict(self):
        all_oid_dict = {}
        oid_list = HardwareModelOidsResource().list(filters={'is_deleted': 0})
        for oid in oid_list:
            if oid['model_id'] not in all_oid_dict.keys():
                all_oid_dict[oid['model_id']] = []
            all_oid_dict[oid['model_id']].append(oid)
        return all_oid_dict


class HardwareModelManageController(CollectionController, HardwareModelBase):
    name = 'monitor.hardware_model'
    allow_methods = ('GET',)
    resource = hardware_model_api.HardwareModelApi

    def on_get(self, req, resp, **kwargs):
        self._validate_method(req)
        criteria = self._build_criteria(req)
        if 'fields' in criteria and req.params.get('sw_oids', None) and isinstance(criteria['fields'],list):
            criteria['fields'].append('id')
            criteria['fields'] = list(set(criteria['fields']))
        refs = self.list(req, copy.deepcopy(criteria), **kwargs)
        count = self.count(req, criteria, results=refs, **kwargs)
        if req.params.get('sw_oids', None):
            all_oid_dict = self.get_all_oid_dict()
            for hardware_model in refs:
                hardware_model['sw_oids'] = all_oid_dict.get(hardware_model['id'], [])
        resp.json = {'count': count, 'data': refs}


class HardwareModelItemManageController(ItemController, HardwareModelBase):
    name = 'monitor.hardware_model.item'
    allow_methods = ('GET',)
    resource = hardware_model_api.HardwareModelApi

    def on_get(self, req, resp, **kwargs):
        hardware_model_id = kwargs.pop('rid')
        hardware_model_api = self.make_resource(req)
        hardware_model_info = hardware_model_api.get(hardware_model_id)
        if not hardware_model_info:
            raise NotFoundError("netline id:%s不存在" % hardware_model_id)
        hardware_model_info['sw_oids'] = self.get_oid_list(hardware_model_info['id'])
        resp.json = hardware_model_info


class HardwareModelBatchSyncController(ResourceInterface):
    name = 'monitor.hardware_model.batch_sync'
    allow_methods = ('PATCH',)
    resource = hardware_model_api.HardwareModelApi
