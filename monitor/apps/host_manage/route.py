# coding: utf-8
from __future__ import absolute_import

from monitor.apps.host_manage.host_manage_controller import HostManageItemController, HostManageController, \
    SearchEndPointController


def add_routes(api):
    api.add_route('/v1/monitor/host_manage', HostManageController())
    api.add_route('/v1/monitor/host_manage/{rid}', HostManageItemController())
    api.add_route('/v1/monitor/search_endpoint_manage', SearchEndPointController())
