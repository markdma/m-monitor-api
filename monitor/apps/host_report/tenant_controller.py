# coding: utf-8

import copy
from monitor.apps.host_report.api import tenant_api, project_api
from monitor.common.controller import CollectionController, ResourceInterface


class TenantController(CollectionController):
    name = 'monitor.tenant'
    allow_methods = ('GET',)
    resource = tenant_api.TenantApi

    def on_get(self, req, resp, **kwargs):
        self._validate_method(req)
        criteria = self._build_criteria(req)
        filters = criteria["filters"] if criteria.get("filters") else None
        refs = self.list(req, copy.deepcopy(criteria), **kwargs)
        count = self.count(req, copy.deepcopy(criteria), results=refs, **kwargs)
        if filters:
            if filters.get("name") is not None:
                if filters["name"]["ilike"] == "*":
                    refs = [{"name": "*", "desc": "产品模板", "state": True}]
                    count = len(refs)
        resp.json = {'count': count, 'data': refs}


class TenantBatchSyncController(ResourceInterface):
    name = 'monitor.tenant.batch_sync'
    allow_methods = ('PATCH',)
    resource = tenant_api.TenantApi


class TenantProjectController(CollectionController):
    name = 'monitor.tenant_projects'
    allow_methods = ('GET',)
    resource = tenant_api.TenantApi

    def on_get(self, req, resp, **kwargs):
        self._validate_method(req)
        api_tenant = tenant_api.TenantApi()
        api_project = project_api.ProjectApi()
        tenant_list = api_tenant.list()
        tenant_dict = {info["uuid"]: info for info in tenant_list}
        # project_list = api_project.list(filters={'tenant_id': {'ilike': 'tenant-'}})
        project_list = api_project.list()
        for project_info in project_list:
            if project_info and isinstance(project_info, dict):
                project_info.pop("tenant", None)
            tenant_id = project_info["tenant_id"]
            if tenant_id and tenant_id in tenant_dict and isinstance(tenant_dict[tenant_id], dict):
                if tenant_dict[tenant_id].has_key("projects") and isinstance(tenant_dict[tenant_id]["projects"], list):
                    tenant_dict[tenant_id]["projects"].append(project_info)
                else:
                    tenant_dict[tenant_id]["projects"] = [project_info]
        resp.json = {'count': len(tenant_dict), 'data': tenant_dict.values()}
