# coding: utf-8
from __future__ import absolute_import

from monitor.apps.host_report.dbresources import resource


class AvailableZoneApi(resource.AvailableZoneResource):

    @property
    def default_filter(self):
        # return {'is_deleted': [0, None, 'null']}
        # return {'is_deleted': {'ne': 1}}
        return {'$or': [{'is_deleted': {'eq': None}}, {'is_deleted': {'eq': 0}}]}

