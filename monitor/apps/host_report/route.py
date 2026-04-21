# coding: utf-8
from __future__ import absolute_import

from monitor.apps.host_report.az_controller import AvailableZoneController, AvailableZoneItemController
from monitor.apps.host_report.host_report_controller import HostReportItemController, HostReportController
from monitor.apps.host_report.host_resource_capacity_controller import HostResourceCapacityController, \
     HostResourceCapacityStatisticsController
from monitor.apps.host_report.capacity_metric_filter_strategy_controller import CapacityMetricFilterStrategyController,\
    CapacityMetricFilterStrategyItemController, CapacityMetricController
from monitor.apps.host_report.netline_resource_capacity_controller import HostResourceCapacityWeekController
from monitor.apps.host_report.project_controller import ProjectController, ProjectBatchSyncController
from monitor.apps.host_report.region_controller import RegionController, RegionItemController, RegionAZController
from monitor.apps.host_report.tenant_controller import TenantController, TenantBatchSyncController, \
    TenantProjectController
from monitor.apps.host_report.database_resource_capacity_controller import DatabaseResourceCapacityController, \
    DatabaseResourceCapacityStatisticsController
from monitor.apps.host_report.disk_resource_capacity_controller import DiskResourceCapacityController, \
    DiskResourceCapacityStatisticsController
from monitor.apps.host_report.ceph_resource_capacity_controller import CephResourceCapacityController, \
    CephResourceCapacityStatisticsController


def add_routes(api):
    api.add_route('/v1/monitor/host_reports', HostReportController())
    api.add_route('/v1/monitor/host_report/{rid}', HostReportItemController())

    api.add_route('/v1/monitor/available_zone', AvailableZoneController())
    api.add_route('/v1/monitor/available_zone/{rid}', AvailableZoneItemController())

    api.add_route('/v1/monitor/region', RegionController())
    api.add_route('/v1/monitor/region/{rid}', RegionItemController())

    api.add_route('/v1/monitor/region_azs', RegionAZController())
    # api.add_route('/v1/monitor/available_zones/batch_sync', AvailableZoneBatchSyncController())
    api.add_route('/v1/monitor/projects', ProjectController())
    api.add_route('/v1/monitor/projects/batch_sync', ProjectBatchSyncController())
    api.add_route('/v1/monitor/tenants', TenantController())

    api.add_route('/v1/monitor/tenant_projects', TenantProjectController())
    api.add_route('/v1/monitor/host_stat', HostResourceCapacityController())

    api.add_route('/v1/monitor/capacity_metric', CapacityMetricController())
    api.add_route('/v1/monitor/capacity_metric_filter_strategy', CapacityMetricFilterStrategyController())
    api.add_route('/v1/monitor/capacity_metric_filter_strategy/{rid}', CapacityMetricFilterStrategyItemController())

    api.add_route('/v1/monitor/netline_stat', HostResourceCapacityWeekController())
    api.add_route('/v1/monitor/tenants/batch_sync', TenantBatchSyncController())

    api.add_route('/v1/monitor/host_stat_statistics', HostResourceCapacityStatisticsController())
    api.add_route('/v1/monitor/database_stat', DatabaseResourceCapacityController())
    api.add_route('/v1/monitor/database_stat_statistics', DatabaseResourceCapacityStatisticsController())

    api.add_route('/v1/monitor/disk_stat', DiskResourceCapacityController())
    api.add_route('/v1/monitor/disk_stat_statistics', DiskResourceCapacityStatisticsController())
    api.add_route('/v1/monitor/ceph_stat', CephResourceCapacityController())
    api.add_route('/v1/monitor/ceph_stat_statistics', CephResourceCapacityStatisticsController())
