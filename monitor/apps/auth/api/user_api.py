# coding: utf-8
from __future__ import absolute_import

from monitor.apps.auth.dbresources import resource


class UserManageApi(resource.UserManageResource):
    pass


class UserPolicyManageApi(resource.UserPolicyManageResource):

    @property
    def default_filter(self):
        return {'is_deleted': 0}
