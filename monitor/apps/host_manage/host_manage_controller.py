# coding: utf-8
import copy

import IPy

from monitor.apps.host_manage.api import host_manage_api
from monitor.apps.monitor_env.dbresources.resource import EnvironmentManageResource
from monitor.common.controller import CollectionController, ItemController
from monitor.common.decorators import tenant_project_func, set_operate_user_func
from monitor.core.exceptions import ValidationError
from monitor.utils import utils


class HostManageBase(object):

    @staticmethod
    def checked_env_type(env_type_id):
        if env_type_id:
            env_type_info = EnvironmentManageResource().get(env_type_id)
            if not env_type_info:
                raise ValidationError("env_type不存在")


class HostManageController(CollectionController, HostManageBase):
    name = 'monitor.host_manage'
    allow_methods = ('GET',)
    resource = host_manage_api.HostManageApi

    @tenant_project_func()
    def _build_criteria(self, req, supported_filters=None):
        return super(HostManageController, self)._build_criteria(req, supported_filters)

    def on_get(self, req, resp, **kwargs):
        self._validate_method(req)
        criteria = self._build_criteria(req)
        filters = criteria.get("filters")
        search = filters.get("search")
        if search:
            if utils.ipv6_validator(search):
                search = str(IPy.IP(search))
            filters["$or"] = [{"hostname": {"ilike": search}}, {"ip": {"ilike": search}}, {"ipv6": {"ilike": search}}]
        refs = self.list(req, copy.deepcopy(criteria), **kwargs)
        count = self.count(req, criteria, results=refs, **kwargs)
        resp.json = {'count': count, 'data': refs}


class HostManageItemController(ItemController, HostManageBase):
    name = 'monitor.host_manage.item'
    allow_methods = ('PATCH', 'GET')
    resource = host_manage_api.HostManageApi

    @set_operate_user_func()
    def update(self, req, data, **kwargs):
        rid = kwargs.pop('rid')
        service_name = req.get_header('X-Service-Name', default=None)
        operate_flag = False if service_name == 'falcon_api' else True
        return self.make_resource(req).update(rid, data, operate_flag=operate_flag)

    @set_operate_user_func()
    def get(self, req, **kwargs):
        return self.make_resource(req).get(**kwargs)


class SearchEndPointController(CollectionController):
    allow_methods = ('GET')
    resource = host_manage_api.SearchEndPointApi

    @tenant_project_func()
    def _build_criteria(self, req, supported_filters=None):
        return super(SearchEndPointController, self)._build_criteria(req, supported_filters)

    def on_get(self, req, resp, **kwargs):
        self._validate_method(req)
        criteria = self._build_criteria(req)
        filters = criteria.get("filters")
        refs = self.list(req, copy.deepcopy(criteria), **kwargs)
        count = self.count(req, criteria, results=refs, **kwargs)
        resp.json = {'count': count, 'data': refs}
