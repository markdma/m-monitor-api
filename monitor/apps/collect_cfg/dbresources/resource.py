# coding: utf-8
from __future__ import absolute_import

import datetime

from monitor.db import models
from monitor.db.crud import ResourceBase


class CollectLogManageResource(ResourceBase):
    orm_meta = models.LogCollectManage
    _default_order = ['-created']
    _primary_keys = 'id'

    def _before_create(self, resource, validate):
        resource['created'] = datetime.datetime.now()
        resource['last_updated'] = datetime.datetime.now()

    def _before_update(self, rid, resource, validate):
        resource['last_updated'] = datetime.datetime.now()



class CollectProcManageResource(ResourceBase):
    orm_meta = models.ProcCollectManage
    _default_order = ['-created']
    _primary_keys = 'id'

    def _before_create(self, resource, validate):
        resource['created'] = datetime.datetime.now()
        resource['last_updated'] = datetime.datetime.now()

    def _before_update(self, rid, resource, validate):
        resource['last_updated'] = datetime.datetime.now()



class CollectPortManageResource(ResourceBase):
    orm_meta = models.PortCollectManage
    _default_order = ['-created']
    _primary_keys = 'id'

    def _before_create(self, resource, validate):
        resource['created'] = datetime.datetime.now()
        resource['last_updated'] = datetime.datetime.now()

    def _before_update(self, rid, resource, validate):
        resource['last_updated'] = datetime.datetime.now()


