from monitor.db import models
from monitor.db.crud import ResourceBase


class CephClusterResource(ResourceBase):
    orm_meta = models.CephCluster
    _primary_keys = 'id'


class CephClusterHostResource(ResourceBase):
    orm_meta = models.CephClusterHost
    _primary_keys = 'id'


class CephClusterRgwResource(ResourceBase):
    orm_meta = models.CephClusterRgw
    _primary_keys = 'id'
