# coding: utf-8
from __future__ import absolute_import

from monitor.apps.monitor_env.env_controller import EnvironmentManageController, EnvironmentManageItemController
from monitor.apps.monitor_env.module_controller import ModuleManageController, ModuleManageItemController


def add_routes(api):
    api.add_route('/v1/monitor/environment', EnvironmentManageController())
    api.add_route('/v1/monitor/environment/{rid}', EnvironmentManageItemController())

    api.add_route('/v1/monitor/module', ModuleManageController())
    api.add_route('/v1/monitor/module/{rid}', ModuleManageItemController())
