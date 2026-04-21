# coding: utf-8
from __future__ import absolute_import

from monitor.apps.host_report.dbresources import resource


class ProjectApi(resource.ProjectResource):

    @property
    def default_filter(self):
        return {'is_deleted': 0}