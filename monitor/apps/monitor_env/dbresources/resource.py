# coding: utf-8
from __future__ import absolute_import

import functools
import datetime

from monitor.db import models
from monitor.db.crud import ResourceBase


class EnvironmentManageResource(ResourceBase):
    orm_meta = models.EnvironmentManage
    _default_order = ['-ctime']
    _primary_keys = 'id'

    def _before_create(self, resource, validate):
        resource["ctime"] = datetime.datetime.now()

    def _before_update(self, rid, resource, validate):
        resource["mtime"] = datetime.datetime.now()


class ModuleManageResource(ResourceBase):
    orm_meta = models.ModuleManage
    _default_order = ['-ctime']
    _primary_keys = 'id'

    def _before_create(self, resource, validate):
        resource["ctime"] = datetime.datetime.now()

    def _before_update(self, rid, resource, validate):
        resource["mtime"] = datetime.datetime.now()
