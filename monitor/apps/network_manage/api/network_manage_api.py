# coding: utf-8
from __future__ import absolute_import

from monitor.apps.network_manage.dbresources import resource


class NetworkSpecialLineApi(resource.NetworkSpecialLineResource):

    def list(self, filters=None, orders=None, offset=None, limit=None, hooks=None):

        return super(NetworkSpecialLineApi, self).list(filters=filters, orders=orders, offset=offset, limit=limit, hooks=hooks)


class NetworkDeviceApi(resource.NetworkDeviceResource):

    def list(self, filters=None, orders=None, offset=None, limit=None, hooks=None):

        return super(NetworkDeviceApi, self).list(filters=filters, orders=orders, offset=offset, limit=limit, hooks=hooks)


class NetPodsManageApi(resource.NetPodsManageResource):
    pass


class NetSubsManageApi(resource.NetSubsManageResource):
    pass


class NetworkRelsManageApi(resource.NetworkRelsManageResource):
    pass


class HardwareModelOidsApi(resource.HardwareModelOidsResource):

    @property
    def default_filter(self):
        return {'is_deleted': 0}
