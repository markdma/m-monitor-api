# encoding = utf-8
import datetime

from monitor.db import models
from monitor.db.crud import ResourceBase


class LoadBalanceRepo(ResourceBase):
    orm_meta = models.LoadBalance
    _primary_keys = 'id'

    def _before_create(self, resource, validate):
        resource["create_time"] = datetime.datetime.now()

    def _before_update(self, rid, resource, validate):
        resource["update_time"] = datetime.datetime.now()
