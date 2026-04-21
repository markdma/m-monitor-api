# coding: utf-8
from __future__ import absolute_import

import datetime

from monitor.core.exceptions import ValidationError
from monitor.db import models, validator
from monitor.db.crud import ResourceBase, ColumnValidator


class HostManageResource(ResourceBase):
    orm_meta = models.HostManage
    _default_order = ['-update_at']
    _primary_keys = 'uuid'
    _validate = [
        ColumnValidator(field='env_type',
                        rule='1,50',
                        rule_type='length',
                        validate_on=['update:O']),
        ColumnValidator(field='enabled',
                        rule_type='integer',
                        rule=validator.InValidator([0, 1]),
                        validate_on=['update:O']),
        ColumnValidator(field='audited',
                        rule_type='integer',
                        rule=validator.InValidator([0, 1]),
                        validate_on=['update:O'])
    ]

    def _before_create(self, resource, validate):
        resource["create_time"] = datetime.datetime.now()

    @staticmethod
    def checked_env_type(env_type_id):
        if env_type_id:
            env_type_info = EnvironmentManageResource().get(env_type_id)
            if not env_type_info:
                raise ValidationError("env_type不存在")

    def _before_update(self, rid, resource, validate):
        resource["update_time"] = datetime.datetime.now()
        self.checked_env_type(resource.get("env_type", None))


class EnvironmentManageResource(ResourceBase):
    orm_meta = models.EnvironmentManage
    _default_order = ['-ctime']
    _primary_keys = 'id'

    def _before_create(self, resource, validate):
        resource["ctime"] = datetime.datetime.now()

    def _before_update(self, rid, resource, validate):
        resource["mtime"] = datetime.datetime.now()


# TODO 主机视图search_enpoint
class SearchEndPointResource(ResourceBase):
    orm_meta = models.SearchEndPoint
    _primary_keys = 'hostname'
