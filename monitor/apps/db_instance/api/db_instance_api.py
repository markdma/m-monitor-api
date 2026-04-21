# coding: utf-8
from __future__ import absolute_import

from monitor.apps.db_instance.dbresources import resource


class DBInstanceManageApi(resource.CMDBDBManageResource):

    pass


class DBNodesManageApi(resource.CMDBDBInstanceManageResource):

    pass
