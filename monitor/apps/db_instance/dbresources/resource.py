# coding: utf-8
from __future__ import absolute_import

import datetime

from monitor.db import models, validator
from monitor.db.crud import ResourceBase, ColumnValidator


class CMDBDBManageResource(ResourceBase):
    orm_meta = models.CMDBDBManage
    _default_order = ['-ctime']
    _primary_keys = 'uuid'

    def _before_create(self, resource, validate):
        resource["ctime"] = datetime.datetime.now()

    def _before_update(self, rid, resource, validate):
        resource["mtime"] = datetime.datetime.now()


class CMDBDBInstanceManageResource(ResourceBase):
    orm_meta = models.CMDBDBInstanceManage
    _default_order = ['-ctime']
    _primary_keys = 'id'
    _project_field = "db_instance.project_id"
    _tenant_field = "db_instance.tenant_id"
    _validate = [
        ColumnValidator(field='user',
                        rule_type='length',
                        rule='1,33',
                        nullable=True,
                        validate_on=['update:O']),
        ColumnValidator(field='password',
                        rule_type='length',
                        rule='1,33',
                        nullable=True,
                        validate_on=['update:O']),
        ColumnValidator(field='enabled',
                        rule_type='integer',
                        rule=validator.InValidator([0, 1]),
                        validate_on=['update:O'])
    ]

    def _before_create(self, resource, validate):
        resource["ctime"] = datetime.datetime.now()

    def _before_update(self, rid, resource, validate):
        resource["mtime"] = datetime.datetime.now()

    @staticmethod
    def update_password_by_sql(session, db_node_id, password):
        execute_sql = r"""UPDATE cmdb_db_instance
        SET password=HEX(AES_ENCRYPT('%s', UNHEX(MD5('%s'))))
        WHERE id = '%s';""" % (password, db_node_id, db_node_id)
        ret = session.execute(execute_sql)
        return ret

    def update(self, rid, resource, filters=None, validate=True, detail=True, operate_flag=False):
        password = resource.pop('password', None)
        with self.transaction() as session:
            before_update, after_update = super(CMDBDBInstanceManageResource, self).update(rid, resource, filters,
                                                                                           validate, detail,
                                                                                           operate_flag)
            if password:
                self.update_password_by_sql(session, rid, password)
            return before_update, after_update
