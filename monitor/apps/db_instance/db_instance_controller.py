# coding: utf-8
import copy

import IPy

from monitor.apps.db_instance.api import db_instance_api
from monitor.common.controller import CollectionController, ItemController
from monitor.common.decorators import tenant_project_func, set_operate_user_func
from monitor.utils import utils


class DBNodesManageController(CollectionController):
    name = 'monitor.db_nodes'
    allow_methods = ('GET',)
    resource = db_instance_api.DBNodesManageApi

    @tenant_project_func(tenant_field="db_instance.tenant_id", project_field="db_instance.project_id")
    def _build_criteria(self, req, supported_filters=None):
        return super(DBNodesManageController, self)._build_criteria(req, supported_filters)

    def on_get(self, req, resp, **kwargs):
        self._validate_method(req)
        criteria = self._build_criteria(req)
        filters = criteria.get("filters")
        server_ip = filters.get("server_ip")
        if server_ip and isinstance(server_ip,dict):
            ip = server_ip.get('ilike')
            if ip and utils.ipv6_validator(ip):
                ip = str(IPy.IP(ip))
                filters["server_ip"].update({"ilike": ip})
        refs = self.list(req, copy.deepcopy(criteria), **kwargs)
        count = self.count(req, criteria, results=refs, **kwargs)
        resp.json = {'count': count, 'data': refs}


class DBNodesItemManageController(ItemController):
    name = 'monitor.db_nodes.item'
    allow_methods = ('GET', 'PATCH')
    resource = db_instance_api.DBNodesManageApi

    @set_operate_user_func()
    def get(self, req, **kwargs):
        return self.make_resource(req).get(**kwargs)

    @set_operate_user_func()
    def update(self, req, data, **kwargs):
        rid = kwargs.pop('rid')
        return self.make_resource(req).update(rid, data, operate_flag=True)
