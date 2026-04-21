# coding: utf-8
from __future__ import absolute_import

from monitor.apps.host_manage.dbresources import resource


class HostManageApi(resource.HostManageResource):

    def list(self, filters=None, orders=None, offset=None, limit=None, hooks=None):
        return super(HostManageApi, self).list(filters=filters, orders=orders, offset=offset, limit=limit, hooks=hooks)


class SearchEndPointApi(resource.SearchEndPointResource):
    def list(self, filters=None, orders=None, offset=None, limit=None, hooks=None):
        return super(SearchEndPointApi, self).list(filters=filters, orders=orders, offset=offset, limit=limit,
                                                   hooks=hooks)
