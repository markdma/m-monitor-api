# coding: utf-8
from __future__ import absolute_import

from monitor.apps.collect_cfg.collect_cfg_controller import CollectCfgManageController, CollectCfgItemManageController


def add_routes(api):
    api.add_route('/v1/monitor/collect/cfg', CollectCfgManageController())
    api.add_route('/v1/monitor/collect/cfg/{rid}', CollectCfgItemManageController())
	
