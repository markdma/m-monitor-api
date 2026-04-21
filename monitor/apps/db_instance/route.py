# coding: utf-8
from __future__ import absolute_import

from monitor.apps.db_instance.db_instance_controller import DBNodesManageController, DBNodesItemManageController


def add_routes(api):
    api.add_route('/v1/monitor/db_nodes', DBNodesManageController())
    api.add_route('/v1/monitor/db_nodes/{rid}', DBNodesItemManageController())

