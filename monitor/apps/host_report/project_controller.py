# coding: utf-8
import copy

from monitor.apps.host_report.api import project_api
from monitor.common.controller import CollectionController, ResourceInterface


class ProjectController(CollectionController):
    name = 'monitor.project'
    allow_methods = ('GET',)
    resource = project_api.ProjectApi

    def on_get(self, req, resp, **kwargs):
        self._validate_method(req)
        criteria = self._build_criteria(req)
        # criteria['filters'].update({'is_deleted': 0})
        refs = self.list(req, copy.deepcopy(criteria), **kwargs)
        count = self.count(req, criteria, results=refs, **kwargs)
        resp.json = {'count': count, 'data': refs}


class ProjectBatchSyncController(ResourceInterface):
    name = 'monitor.project.batch_sync'
    allow_methods = ('PATCH',)
    resource = project_api.ProjectApi
