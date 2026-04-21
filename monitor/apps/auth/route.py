# coding: utf-8
from __future__ import absolute_import

from monitor.apps.auth.user_controller import UserItemController, UserController, UserPolicyController, \
    UserPolicyItemController


def add_routes(api):
    api.add_route('/v1/monitor/auth/user/{rid}', UserItemController())
    api.add_route('/v1/monitor/auth/user', UserController())

    api.add_route('/v1/monitor/auth/user_policies', UserPolicyController())
    api.add_route('/v1/monitor/auth/user_policies/{rid}', UserPolicyItemController())