# coding: utf-8
from __future__ import absolute_import

import datetime

from monitor.db import models
from monitor.db.crud import ResourceBase


class NetworkSpecialLineResource(ResourceBase):
    orm_meta = models.IFWanManage
    _default_order = ['-name']
    _primary_keys = 'id'

    def _before_create(self, resource, validate):
        resource["create_time"] = datetime.datetime.now()

    def _before_update(self, rid, resource, validate):
        resource["uptime"] = datetime.datetime.now()


class NetworkDeviceResource(ResourceBase):
    orm_meta = models.SWIprangeManage
    _default_order = ['-name']
    _primary_keys = 'serial_num'

    def _before_create(self, resource, validate):
        resource["create_time"] = datetime.datetime.now()

    def _before_update(self, rid, resource, validate):
        resource["uptime"] = datetime.datetime.now()


class HardwareModelOidsResource(ResourceBase):
    orm_meta = models.SWOidsManage
    _default_order = ['-model']
    _primary_keys = 'id'
    _soft_del_flag = {'is_deleted': 1, 'uptime': datetime.datetime.now()}
    _soft_delete = True

    def _before_create(self, resource, validate):
        resource["uptime"] = datetime.datetime.now()

    def _before_update(self, rid, resource, validate):
        resource["uptime"] = datetime.datetime.now()


class HardwareModelResource(ResourceBase):
    orm_meta = models.HardwareModelManage
    _default_order = ['-create_time']
    _primary_keys = 'id'

    # def _before_create(self, resource, validate):
    #     resource["create_time"] = datetime.datetime.now()

    def _before_update(self, rid, resource, validate):
        resource["update_time"] = datetime.datetime.now()


class NetPodsManageResource(ResourceBase):
    orm_meta = models.NetPodsManage
    _default_order = ['-name']
    _primary_keys = 'uuid'

    def _before_update(self, rid, resource, validate):
        resource["update_at"] = datetime.datetime.now()


class NetSubsManageResource(ResourceBase):
    orm_meta = models.NetSubsManage
    _default_order = ['-name']
    _primary_keys = 'uuid'

    def _before_update(self, rid, resource, validate):
        resource["update_at"] = datetime.datetime.now()


class NetworkRelsManageResource(ResourceBase):
    orm_meta = models.NetworkRelsManage
    _default_order = ['-src_device']
    _primary_keys = 'uuid'

    def _before_update(self, rid, resource, validate):
        resource["update_at"] = datetime.datetime.now()
