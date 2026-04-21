# coding: utf-8
from __future__ import absolute_import

from __future__ import absolute_import

from monitor.apps.monitor_env.dbresources import resource


class ModuleManageApi(resource.ModuleManageResource):

    def list(self, filters=None, orders=None, offset=None, limit=None, hooks=None):

        return super(ModuleManageApi, self).list(filters=filters, orders=orders, offset=offset, limit=limit, hooks=hooks)