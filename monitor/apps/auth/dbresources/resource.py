# coding: utf-8
from __future__ import absolute_import

import datetime

from monitor.db import models, pool
from monitor.db.crud import ResourceBase


class UserManageResource(ResourceBase):
    orm_meta = models.UserManage
    orm_pool = pool.POOLS.uic
    _default_order = ['-created']
    _primary_keys = 'id'

    def _before_create(self, resource, validate):
        resource["created"] = datetime.datetime.now()


class UserPolicyManageResource(ResourceBase):
    orm_meta = models.IamPolicyManage
    _default_order = ['-create_time']
    _primary_keys = 'id'
    _soft_del_flag = {'is_deleted': 1, 'update_time': datetime.datetime.now()}
    _soft_delete = True

    def _before_create(self, resource, validate):
        resource['create_time'] = datetime.datetime.now()

    def _before_update(self, rid, resource, validate):
        resource['update_time'] = datetime.datetime.now()