# coding: utf-8
from __future__ import absolute_import

from monitor.apps.host_report.dbresources import resource


class HostReportApi(resource.HostReportResource):

    def list(self, filters=None, orders=None, offset=None, limit=None, hooks=None):

        return super(HostReportApi, self).list(filters=filters, orders=orders, offset=offset, limit=limit, hooks=hooks)
