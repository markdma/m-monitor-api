# coding: utf-8
from monitor.apps.database_server.api import falcon_portal_api
from monitor.common.controller import CollectionController, ItemController, ResourceInterface


class DatabaseServerHostReportManageController(CollectionController):
    name = 'database_server.host_report'
    allow_methods = ('GET', 'POST')
    resource = falcon_portal_api.HostReportResourceApi


class DatabaseServerHostReportBatchSyncManageController(ResourceInterface):
    name = 'database_server.host_report.batch_sync'
    allow_methods = ('PATCH',)
    resource = falcon_portal_api.HostReportResourceApi


class DatabaseServerHostReportItemManageController(ItemController):
    name = 'database_server.host_report.item'
    allow_methods = ('GET', 'PATCH', 'DELETE')
    resource = falcon_portal_api.HostReportResourceApi


class DatabaseServerHostManageController(CollectionController):
    name = 'database_server.host'
    allow_methods = ('GET', 'POST')
    resource = falcon_portal_api.HostResourceApi


class DatabaseServerHostBatchSyncManageController(ResourceInterface):
    name = 'database_server.host.batch_sync'
    allow_methods = ('PATCH',)
    resource = falcon_portal_api.HostResourceApi


class DatabaseServerHostItemManageController(ItemController):
    name = 'database_server.host.item'
    allow_methods = ('GET', 'PATCH', 'DELETE')
    resource = falcon_portal_api.HostResourceApi


class DatabaseServerAvailableZoneManageController(CollectionController):
    name = 'database_server.available_zone'
    allow_methods = ('GET', 'POST')
    resource = falcon_portal_api.AvailableZoneResourceApi


class DatabaseServerAvailableZoneItemManageController(ItemController):
    name = 'database_server.available_zone.item'
    allow_methods = ('GET', 'PATCH', 'DELETE')
    resource = falcon_portal_api.AvailableZoneResourceApi


class DatabaseServerAvailableZoneBatchSyncManageController(ResourceInterface):
    name = 'database_server.available_zone.batch_sync'
    allow_methods = ('PATCH', )
    resource = falcon_portal_api.AvailableZoneResourceApi


class DatabaseServerIfRegionManageController(CollectionController):
    name = 'database_server.if_region'
    allow_methods = ('GET', 'POST')
    resource = falcon_portal_api.RegionResourceApi


class DatabaseServerIfRegionItemManageController(ItemController):
    name = 'database_server.if_region.item'
    allow_methods = ('GET', 'PATCH', 'DELETE')
    resource = falcon_portal_api.RegionResourceApi


class DatabaseServerIfRegionBatchSyncManageController(ResourceInterface):
    name = 'database_server.if_region.batch_sync'
    allow_methods = ('PATCH', )
    resource = falcon_portal_api.RegionResourceApi


class DatabaseServerCapacityMetricManageController(CollectionController):
    name = 'database_server.capacity_metric'
    allow_methods = ('GET', 'POST')
    resource = falcon_portal_api.CapacityMetricResourceApi


class DatabaseServerCapacityMetricItemManageController(ItemController):
    name = 'database_server.capacity_metric.item'
    allow_methods = ('GET', 'PATCH', 'DELETE')
    resource = falcon_portal_api.CapacityMetricResourceApi


class DatabaseServerCapacityMetricBatchSyncManageController(ResourceInterface):
    name = 'database_server.capacity_metric.batch_sync'
    allow_methods = ('PATCH', )
    resource = falcon_portal_api.CapacityMetricResourceApi


class DatabaseServerCapacityMetricFilterStrategyManageController(CollectionController):
    name = 'database_server.capacity_metric_filter_strategy'
    allow_methods = ('GET', 'POST')
    resource = falcon_portal_api.CapacityMetricFilterStrategyResourceApi


class DatabaseServerCapacityMetricFilterStrategyItemManageController(ItemController):
    name = 'database_server.capacity_metric_filter_strategy.item'
    allow_methods = ('GET', 'PATCH', 'DELETE')
    resource = falcon_portal_api.CapacityMetricFilterStrategyResourceApi


class DatabaseServerCapacityMetricFilterStrategyBatchSyncManageController(ResourceInterface):
    name = 'database_server.capacity_metric_filter_strategy.batch_sync'
    allow_methods = ('PATCH', )
    resource = falcon_portal_api.CapacityMetricFilterStrategyResourceApi


class DatabaseServerHostResourceCapacityManageController(CollectionController):
    name = 'database_server.host_resource_capacity'
    allow_methods = ('GET', 'POST')
    resource = falcon_portal_api.HostResourceCapacityResourceApi


class DatabaseServerHostResourceCapacityItemManageController(ItemController):
    name = 'database_server.host_resource_capacity.item'
    allow_methods = ('GET', 'PATCH', 'DELETE')
    resource = falcon_portal_api.HostResourceCapacityResourceApi


class DatabaseServerHostResourceCapacityBatchSyncManageController(ResourceInterface):
    name = 'database_server.host_resource_capacity.batch_sync'
    allow_methods = ('PATCH', )
    resource = falcon_portal_api.HostResourceCapacityResourceApi


class DatabaseServerHostResourceCapacityWeekManageController(CollectionController):
    name = 'database_server.host_resource_capacity_week'
    allow_methods = ('GET', 'POST')
    resource = falcon_portal_api.HostResourceCapacityWeekResourceApi


class DatabaseServerHostResourceCapacityWeekItemManageController(ItemController):
    name = 'database_server.host_resource_capacity_week.item'
    allow_methods = ('GET', 'PATCH', 'DELETE')
    resource = falcon_portal_api.HostResourceCapacityWeekResourceApi


class DatabaseServerHostResourceCapacityWeekBatchSyncManageController(ResourceInterface):
    name = 'database_server.host_resource_capacity_week.batch_sync'
    allow_methods = ('PATCH', )
    resource = falcon_portal_api.HostResourceCapacityWeekResourceApi


class DatabaseServerHostResourceCapacityMonthManageController(CollectionController):
    name = 'database_server.host_resource_capacity_month'
    allow_methods = ('GET',)
    resource = falcon_portal_api.HostResourceCapacityMonthResourceApi


class DatabaseServerNetLineResourceCapacityManageController(CollectionController):
    name = 'database_server.netline_resource_capacity'
    allow_methods = ('GET', 'POST')
    resource = falcon_portal_api.NetLineResourceCapacityApi


class DatabaseServerHNetLineResourceCapacityItemManageController(ItemController):
    name = 'database_server.netline_resource_capacity.item'
    allow_methods = ('GET', 'PATCH', 'DELETE')
    resource = falcon_portal_api.NetLineResourceCapacityApi


class DatabaseServerNetLineResourceCapacityBatchSyncManageController(ResourceInterface):
    name = 'database_server.netline_resource_capacity.batch_sync'
    allow_methods = ('PATCH', )
    resource = falcon_portal_api.NetLineResourceCapacityApi


class DatabaseServerNetLineResourceCapacityWeekManageController(CollectionController):
    name = 'database_server.netline_resource_capacity_week'
    allow_methods = ('GET', 'POST')
    resource = falcon_portal_api.NetLineResourceCapacityWeekApi


class DatabaseServerHNetLineResourceCapacityWeekItemManageController(ItemController):
    name = 'database_server.netline_resource_capacity_week.item'
    allow_methods = ('GET', 'PATCH', 'DELETE')
    resource = falcon_portal_api.NetLineResourceCapacityWeekApi


class DatabaseServerNetLineResourceCapacityWeekBatchSyncManageController(ResourceInterface):
    name = 'database_server.netline_resource_capacity_week.batch_sync'
    allow_methods = ('PATCH', )
    resource = falcon_portal_api.NetLineResourceCapacityWeekApi


class DatabaseServerProjectManageController(CollectionController):
    name = 'database_server.project'
    allow_methods = ('GET', 'POST')
    resource = falcon_portal_api.ProjectResourceApi


class DatabaseServerProjectItemManageController(ItemController):
    name = 'database_server.project.item'
    allow_methods = ('GET', 'PATCH', 'DELETE')
    resource = falcon_portal_api.ProjectResourceApi


class DatabaseServerProjectBatchSyncManageController(ResourceInterface):
    name = 'database_server.project.batch_sync'
    allow_methods = ('PATCH', )
    resource = falcon_portal_api.ProjectResourceApi


class DatabaseServerTenantManageController(CollectionController):
    name = 'database_server.tenant'
    allow_methods = ('GET', 'POST')
    resource = falcon_portal_api.TenantResourceApi


class DatabaseServerTenantItemManageController(ItemController):
    name = 'database_server.tenant.item'
    allow_methods = ('GET', 'PATCH', 'DELETE')
    resource = falcon_portal_api.TenantResourceApi


class DatabaseServerTenantBatchSyncManageController(ResourceInterface):
    name = 'database_server.tenant.batch_sync'
    allow_methods = ('PATCH', )
    resource = falcon_portal_api.TenantResourceApi


class DatabaseServerCMDBDBManageController(CollectionController):
    name = 'database_server.cmdb_db'
    allow_methods = ('GET', 'POST')
    resource = falcon_portal_api.CMDBDBManageResourceApi


class DatabaseServerCMDBDBItemManageController(ItemController):
    name = 'database_server.cmdb_db.item'
    allow_methods = ('GET', 'PATCH', 'DELETE')
    resource = falcon_portal_api.CMDBDBManageResourceApi


class DatabaseServerCMDBDBBatchSyncManageController(ResourceInterface):
    name = 'database_server.cmdb_db.batch_sync'
    allow_methods = ('PATCH', )
    resource = falcon_portal_api.CMDBDBManageResourceApi


class DatabaseServerEnvironmentManageController(CollectionController):
    name = 'database_server.environment'
    allow_methods = ('GET', 'POST')
    resource = falcon_portal_api.EnvironmentManageResourceApi


class DatabaseServerEnvironmentItemManageController(ItemController):
    name = 'database_server.environment.item'
    allow_methods = ('GET', 'PATCH', 'DELETE')
    resource = falcon_portal_api.EnvironmentManageResourceApi


class DatabaseServerEnvironmentBatchSyncManageController(ResourceInterface):
    name = 'database_server.environment.batch_sync'
    allow_methods = ('PATCH', )
    resource = falcon_portal_api.EnvironmentManageResourceApi


class DatabaseServerIfWanManageController(CollectionController):
    name = 'database_server.if_wan'
    allow_methods = ('GET', 'POST')
    resource = falcon_portal_api.NetworkSpecialLineResourceApi


class DatabaseServerIfWanItemManageController(ItemController):
    name = 'database_server.if_wan.item'
    allow_methods = ('GET', 'PATCH', 'DELETE')
    resource = falcon_portal_api.NetworkSpecialLineResourceApi


class DatabaseServerIfWanBatchSyncManageController(ResourceInterface):
    name = 'database_server.if_wan.batch_sync'
    allow_methods = ('PATCH', )
    resource = falcon_portal_api.NetworkSpecialLineResourceApi


class DatabaseServerSWIprangeManageController(CollectionController):
    name = 'database_server.sw_iprange'
    allow_methods = ('GET', 'POST')
    resource = falcon_portal_api.NetworkDeviceResourceApi


class DatabaseServerSWIprangeItemManageController(ItemController):
    name = 'database_server.sw_iprange.item'
    allow_methods = ('GET', 'PATCH', 'DELETE')
    resource = falcon_portal_api.NetworkDeviceResourceApi


class DatabaseServerSWIprangeBatchSyncManageController(ResourceInterface):
    name = 'database_server.sw_iprange.batch_sync'
    allow_methods = ('PATCH', )
    resource = falcon_portal_api.NetworkDeviceResourceApi


class DatabaseServerSWOIDSManageController(CollectionController):
    name = 'database_server.sw_oids'
    allow_methods = ('GET', 'POST')
    resource = falcon_portal_api.HardwareModelOidsResourceApi


class DatabaseServerSWOIDSItemManageController(ItemController):
    name = 'database_server.sw_oids.item'
    allow_methods = ('GET', 'PATCH', 'DELETE')
    resource = falcon_portal_api.HardwareModelOidsResourceApi


class DatabaseServerSWOIDSBatchSyncManageController(ResourceInterface):
    name = 'database_server.sw_oids.batch_sync'
    allow_methods = ('PATCH', )
    resource = falcon_portal_api.HardwareModelOidsResourceApi


class DatabaseServerIfHardwareModelManageController(CollectionController):
    name = 'database_server.if_hardware_model'
    allow_methods = ('GET', 'POST')
    resource = falcon_portal_api.HardwareModelResourceApi


class DatabaseServerIfHardwareModelItemManageController(ItemController):
    name = 'database_server.if_hardware_model.item'
    allow_methods = ('GET', 'PATCH', 'DELETE')
    resource = falcon_portal_api.HardwareModelResourceApi


class DatabaseServerIfHardwareModelBatchSyncManageController(ResourceInterface):
    name = 'database_server.if_hardware_model.batch_sync'
    allow_methods = ('PATCH', )
    resource = falcon_portal_api.HardwareModelResourceApi


class DatabaseServerNetPodsManageController(CollectionController):
    name = 'database_server.net_pods'
    allow_methods = ('GET', 'POST')
    resource = falcon_portal_api.NetPodsManageResourceApi


class DatabaseServerNetPodsItemManageController(ItemController):
    name = 'database_server.net_pods.item'
    allow_methods = ('GET', 'PATCH', 'DELETE')
    resource = falcon_portal_api.NetPodsManageResourceApi


class DatabaseServerNetPodsBatchSyncManageController(ResourceInterface):
    name = 'database_server.net_pods.batch_sync'
    allow_methods = ('PATCH', )
    resource = falcon_portal_api.NetPodsManageResourceApi


class DatabaseServerNetSubsManageController(CollectionController):
    name = 'database_server.net_subs'
    allow_methods = ('GET', 'POST')
    resource = falcon_portal_api.NetSubsManageResourceApi


class DatabaseServerNetSubsItemManageController(ItemController):
    name = 'database_server.net_subs.item'
    allow_methods = ('GET', 'PATCH', 'DELETE')
    resource = falcon_portal_api.NetSubsManageResourceApi


class DatabaseServerNetSubsBatchSyncManageController(ResourceInterface):
    name = 'database_server.net_subs.batch_sync'
    allow_methods = ('PATCH', )
    resource = falcon_portal_api.NetSubsManageResourceApi


class DatabaseServerNetworkRelsManageController(CollectionController):
    name = 'database_server.network_rels'
    allow_methods = ('GET', 'POST')
    resource = falcon_portal_api.NetworkRelsManageResourceApi


class DatabaseServerNetworkRelsItemManageController(ItemController):
    name = 'database_server.network_rels.item'
    allow_methods = ('GET', 'PATCH', 'DELETE')
    resource = falcon_portal_api.NetworkRelsManageResourceApi


class DatabaseServerNetworkRelsBatchSyncManageController(ResourceInterface):
    name = 'database_server.network_rels.batch_sync'
    allow_methods = ('PATCH', )
    resource = falcon_portal_api.NetworkRelsManageResourceApi


class DatabaseServerModuleManageController(CollectionController):
    name = 'database_server.module'
    allow_methods = ('GET', 'POST')
    resource = falcon_portal_api.ModuleManageResourceApi


class DatabaseServerModuleItemManageController(ItemController):
    name = 'database_server.module.item'
    allow_methods = ('GET', 'PATCH', 'DELETE')
    resource = falcon_portal_api.ModuleManageResourceApi


class DatabaseServerModuleBatchSyncManageController(ResourceInterface):
    name = 'database_server.module.batch_sync'
    allow_methods = ('PATCH', )
    resource = falcon_portal_api.ModuleManageResourceApi


class DatabaseServerCMDBHostManageController(CollectionController):
    name = 'database_server.cmdb_host'
    allow_methods = ('GET', 'POST')
    resource = falcon_portal_api.HostManageResourceApi


class DatabaseServerCMDBHostItemManageController(ItemController):
    name = 'database_server.cmdb_host.item'
    allow_methods = ('GET', 'PATCH', 'DELETE')
    resource = falcon_portal_api.HostManageResourceApi


class DatabaseServerCMDBHostBatchSyncManageController(ResourceInterface):
    name = 'database_server.cmdb_host.batch_sync'
    allow_methods = ('PATCH', )
    resource = falcon_portal_api.HostManageResourceApi


class DatabaseServerCMDBDBInstanceManageController(CollectionController):
    name = 'database_server.cmdb_db_instance'
    allow_methods = ('GET', 'POST')
    resource = falcon_portal_api.CMDBDBInstanceManageResourceApi


class DatabaseServerCMDBDBInstanceItemManageController(ItemController):
    name = 'database_server.cmdb_db_instance.item'
    allow_methods = ('GET', 'PATCH', 'DELETE')
    resource = falcon_portal_api.CMDBDBInstanceManageResourceApi


class DatabaseServerCMDBDBInstanceBatchSyncManageController(ResourceInterface):
    name = 'database_server.cmdb_db_instance.batch_sync'
    allow_methods = ('PATCH', )
    resource = falcon_portal_api.CMDBDBInstanceManageResourceApi


class DatabaseServerActionManageController(CollectionController):
    name = 'database_server.action'
    allow_methods = ('GET', 'POST')
    resource = falcon_portal_api.ActionManageManageApi


class DatabaseServerActionItemManageController(ItemController):
    name = 'database_server.action.item'
    allow_methods = ('GET', 'PATCH', 'DELETE')
    resource = falcon_portal_api.ActionManageManageApi


class DatabaseServerActionBatchSyncManageController(ResourceInterface):
    name = 'database_server.action.batch_sync'
    allow_methods = ('PATCH', )
    resource = falcon_portal_api.ActionManageManageApi


class DatabaseServerActionUserManageController(CollectionController):
    name = 'database_server.action_user'
    allow_methods = ('GET', 'POST')
    resource = falcon_portal_api.ActionUserManageApi


class DatabaseServerActionUserItemManageController(ItemController):
    name = 'database_server.action_user.item'
    allow_methods = ('GET', 'PATCH', 'DELETE')
    resource = falcon_portal_api.ActionUserManageApi


class DatabaseServerActionUserBatchSyncManageController(ResourceInterface):
    name = 'database_server.action_user.batch_sync'
    allow_methods = ('PATCH', )
    resource = falcon_portal_api.ActionUserManageApi


class DatabaseServerAlarmOtherManageController(CollectionController):
    name = 'database_server.alarm_other'
    allow_methods = ('GET', 'POST')
    resource = falcon_portal_api.AlarmOtherManageResourceApi


class DatabaseServerAlarmOtherItemManageController(ItemController):
    name = 'database_server.alarm_other.item'
    allow_methods = ('GET', 'PATCH', 'DELETE')
    resource = falcon_portal_api.AlarmOtherManageResourceApi


class DatabaseServerAlarmOtherBatchSyncManageController(ResourceInterface):
    name = 'database_server.alarm_other.batch_sync'
    allow_methods = ('PATCH', )
    resource = falcon_portal_api.AlarmOtherManageResourceApi


class DatabaseServerAlarmScheManageController(CollectionController):
    name = 'database_server.alarm_sche'
    allow_methods = ('GET', 'POST')
    resource = falcon_portal_api.AlarmScheManageResourceApi


class DatabaseServerAlarmScheItemManageController(ItemController):
    name = 'database_server.alarm_sche.item'
    allow_methods = ('GET', 'PATCH', 'DELETE')
    resource = falcon_portal_api.AlarmScheManageResourceApi


class DatabaseServerAlarmScheBatchSyncManageController(ResourceInterface):
    name = 'database_server.alarm_sche.batch_sync'
    allow_methods = ('PATCH', )
    resource = falcon_portal_api.AlarmScheManageResourceApi


class DatabaseServerAlarmTextCFGManageController(CollectionController):
    name = 'database_server.alarm_text_cfg'
    allow_methods = ('GET', 'POST')
    resource = falcon_portal_api.AlarmTextCfgManageResourceApi


class DatabaseServerAlarmTextCFGItemManageController(ItemController):
    name = 'database_server.alarm_text_cfg.item'
    allow_methods = ('GET', 'PATCH', 'DELETE')
    resource = falcon_portal_api.AlarmTextCfgManageResourceApi


class DatabaseServerAlarmTextCFGBatchSyncManageController(ResourceInterface):
    name = 'database_server.alarm_text_cfg.batch_sync'
    allow_methods = ('PATCH', )
    resource = falcon_portal_api.AlarmTextCfgManageResourceApi


class DatabaseServerAlarmTypeManageController(CollectionController):
    name = 'database_server.alarm_type'
    allow_methods = ('GET', 'POST')
    resource = falcon_portal_api.AlarmTypeManageResourceApi


class DatabaseServerAlarmTypeItemManageController(ItemController):
    name = 'database_server.alarm_type.item'
    allow_methods = ('GET', 'PATCH', 'DELETE')
    resource = falcon_portal_api.AlarmTypeManageResourceApi


class DatabaseServerAlarmTypeBatchSyncManageController(ResourceInterface):
    name = 'database_server.alarm_type.batch_sync'
    allow_methods = ('PATCH', )
    resource = falcon_portal_api.AlarmTypeManageResourceApi


class DatabaseServerBigDataAlertManageController(CollectionController):
    name = 'database_server.bigdata_alert'
    allow_methods = ('GET', 'POST')
    resource = falcon_portal_api.BigDataAlertManageResourceApi


class DatabaseServerBigDataAlertItemManageController(ItemController):
    name = 'database_server.bigdata_alert.item'
    allow_methods = ('GET', 'PATCH', 'DELETE')
    resource = falcon_portal_api.BigDataAlertManageResourceApi


class DatabaseServerBigDataAlertBatchSyncManageController(ResourceInterface):
    name = 'database_server.bigdata_alert.batch_sync'
    allow_methods = ('PATCH', )
    resource = falcon_portal_api.BigDataAlertManageResourceApi


class DatabaseServerCheckIPManageController(CollectionController):
    name = 'database_server.check_ip'
    allow_methods = ('GET', 'POST')
    resource = falcon_portal_api.CheckIPManageResourceApi


class DatabaseServerCheckIPItemManageController(ItemController):
    name = 'database_server.check_ip.item'
    allow_methods = ('GET', 'PATCH', 'DELETE')
    resource = falcon_portal_api.CheckIPManageResourceApi


class DatabaseServerCheckIPBatchSyncManageController(ResourceInterface):
    name = 'database_server.check_ip.batch_sync'
    allow_methods = ('PATCH', )
    resource = falcon_portal_api.CheckIPManageResourceApi


class DatabaseServerCheckIPPortManageController(CollectionController):
    name = 'database_server.check_ip_port'
    allow_methods = ('GET', 'POST')
    resource = falcon_portal_api.CheckIPPortManageResourceApi


class DatabaseServerCheckIPPortItemManageController(ItemController):
    name = 'database_server.check_ip_port.item'
    allow_methods = ('GET', 'PATCH', 'DELETE')
    resource = falcon_portal_api.CheckIPPortManageResourceApi


class DatabaseServerCheckIPPortBatchSyncManageController(ResourceInterface):
    name = 'database_server.check_ip_port.batch_sync'
    allow_methods = ('PATCH', )
    resource = falcon_portal_api.CheckIPPortManageResourceApi


class DatabaseServerCheckPointManageController(CollectionController):
    name = 'database_server.check_point'
    allow_methods = ('GET', 'POST')
    resource = falcon_portal_api.CheckPointManageResourceApi


class DatabaseServerCheckPointItemManageController(ItemController):
    name = 'database_server.check_point.item'
    allow_methods = ('GET', 'PATCH', 'DELETE')
    resource = falcon_portal_api.CheckPointManageResourceApi


class DatabaseServerCheckPointBatchSyncManageController(ResourceInterface):
    name = 'database_server.check_point.batch_sync'
    allow_methods = ('PATCH', )
    resource = falcon_portal_api.CheckPointManageResourceApi


class DatabaseServerClusterManageController(CollectionController):
    name = 'database_server.cluster'
    allow_methods = ('GET', 'POST')
    resource = falcon_portal_api.ClusterManageResourceApi


class DatabaseServerClusterItemManageController(ItemController):
    name = 'database_server.cluster.item'
    allow_methods = ('GET', 'PATCH', 'DELETE')
    resource = falcon_portal_api.ClusterManageResourceApi


class DatabaseServerClusterBatchSyncManageController(ResourceInterface):
    name = 'database_server.cluster.batch_sync'
    allow_methods = ('PATCH', )
    resource = falcon_portal_api.ClusterManageResourceApi


class DatabaseServerCmdbSYSManageController(CollectionController):
    name = 'database_server.cmdb_sys'
    allow_methods = ('GET', 'POST')
    resource = falcon_portal_api.CmdbSYSManageResourceApi


class DatabaseServerCmdbSYSItemManageController(ItemController):
    name = 'database_server.cmdb_sys.item'
    allow_methods = ('GET', 'PATCH', 'DELETE')
    resource = falcon_portal_api.CmdbSYSManageResourceApi


class DatabaseServerCmdbSYSBatchSyncManageController(ResourceInterface):
    name = 'database_server.cmdb_sys.batch_sync'
    allow_methods = ('PATCH', )
    resource = falcon_portal_api.CmdbSYSManageResourceApi


class DatabaseServerCmdbSYSSecManageController(CollectionController):
    name = 'database_server.cmdb_sys_sec'
    allow_methods = ('GET', 'POST')
    resource = falcon_portal_api.CmdbSYSSecManageResourceApi


class DatabaseServerCmdbSYSSecItemManageController(ItemController):
    name = 'database_server.cmdb_sys_sec.item'
    allow_methods = ('GET', 'PATCH', 'DELETE')
    resource = falcon_portal_api.CmdbSYSSecManageResourceApi


class DatabaseServerCmdbSYSSecBatchSyncManageController(ResourceInterface):
    name = 'database_server.cmdb_sys_sec.batch_sync'
    allow_methods = ('PATCH', )
    resource = falcon_portal_api.CmdbSYSSecManageResourceApi


class DatabaseServerConfigKVManageController(CollectionController):
    name = 'database_server.config_kv'
    allow_methods = ('GET', 'POST')
    resource = falcon_portal_api.ConfigKVManageResourceApi


class DatabaseServerConfigKVItemManageController(ItemController):
    name = 'database_server.config_kv.item'
    allow_methods = ('GET', 'PATCH', 'DELETE')
    resource = falcon_portal_api.ConfigKVManageResourceApi


class DatabaseServerConfigKVBatchSyncManageController(ResourceInterface):
    name = 'database_server.config_kv.batch_sync'
    allow_methods = ('PATCH', )
    resource = falcon_portal_api.ConfigKVManageResourceApi


class DatabaseServerCounterManageController(CollectionController):
    name = 'database_server.counter'
    allow_methods = ('GET', 'POST')
    resource = falcon_portal_api.CounterManageResourceApi


class DatabaseServerCounterItemManageController(ItemController):
    name = 'database_server.counter.item'
    allow_methods = ('GET', 'PATCH', 'DELETE')
    resource = falcon_portal_api.CounterManageResourceApi


class DatabaseServerCounterBatchSyncManageController(ResourceInterface):
    name = 'database_server.counter.batch_sync'
    allow_methods = ('PATCH', )
    resource = falcon_portal_api.CounterManageResourceApi


class DatabaseServerCustomAlertManageController(CollectionController):
    name = 'database_server.custom_alert'
    allow_methods = ('GET', 'POST')
    resource = falcon_portal_api.CustomAlertManageResourceApi


class DatabaseServerCustomAlertItemManageController(ItemController):
    name = 'database_server.custom_alert.item'
    allow_methods = ('GET', 'PATCH', 'DELETE')
    resource = falcon_portal_api.CustomAlertManageResourceApi


class DatabaseServerCustomAlertBatchSyncManageController(ResourceInterface):
    name = 'database_server.custom_alert.batch_sync'
    allow_methods = ('PATCH', )
    resource = falcon_portal_api.CustomAlertManageResourceApi


class DatabaseServerCustomCounterManageController(CollectionController):
    name = 'database_server.custom_counter'
    allow_methods = ('GET', 'POST')
    resource = falcon_portal_api.CustomCounterManageResourceApi


class DatabaseServerCustomCounterItemManageController(ItemController):
    name = 'database_server.custom_counter.item'
    allow_methods = ('GET', 'PATCH', 'DELETE')
    resource = falcon_portal_api.CustomCounterManageResourceApi


class DatabaseServerCustomCounterBatchSyncManageController(ResourceInterface):
    name = 'database_server.custom_counter.batch_sync'
    allow_methods = ('PATCH', )
    resource = falcon_portal_api.CustomCounterManageResourceApi


class DatabaseServerExpressionManageController(CollectionController):
    name = 'database_server.expression'
    allow_methods = ('GET', 'POST')
    resource = falcon_portal_api.ExpressionManageResourceApi


class DatabaseServerExpressionItemManageController(ItemController):
    name = 'database_server.expression.item'
    allow_methods = ('GET', 'PATCH', 'DELETE')
    resource = falcon_portal_api.ExpressionManageResourceApi


class DatabaseServerExpressionBatchSyncManageController(ResourceInterface):
    name = 'database_server.expression.batch_sync'
    allow_methods = ('PATCH', )
    resource = falcon_portal_api.ExpressionManageResourceApi


class DatabaseServerGRPManageController(CollectionController):
    name = 'database_server.grp'
    allow_methods = ('GET', 'POST')
    resource = falcon_portal_api.GRPManageResourceApi


class DatabaseServerGRPItemManageController(ItemController):
    name = 'database_server.grp.item'
    allow_methods = ('GET', 'PATCH', 'DELETE')
    resource = falcon_portal_api.GRPManageResourceApi


class DatabaseServerGRPBatchSyncManageController(ResourceInterface):
    name = 'database_server.grp.batch_sync'
    allow_methods = ('PATCH', )
    resource = falcon_portal_api.GRPManageResourceApi


class DatabaseServerGRPHostManageController(CollectionController):
    name = 'database_server.grp_host'
    allow_methods = ('GET', 'POST')
    resource = falcon_portal_api.GRPHostManageResourceApi


class DatabaseServerGRPHostItemManageController(ItemController):
    name = 'database_server.grp_host.item'
    allow_methods = ('GET', 'PATCH', 'DELETE')
    resource = falcon_portal_api.GRPHostManageResourceApi


class DatabaseServerGRPHostBatchSyncManageController(ResourceInterface):
    name = 'database_server.grp_host.batch_sync'
    allow_methods = ('PATCH', )
    resource = falcon_portal_api.GRPHostManageResourceApi


class DatabaseServerGRPHostnameManageController(CollectionController):
    name = 'database_server.grp_hostname'
    allow_methods = ('GET', 'POST')
    resource = falcon_portal_api.GRPHostnameManageResourceApi


class DatabaseServerGRPHostnameItemManageController(ItemController):
    name = 'database_server.grp_hostname.item'
    allow_methods = ('GET', 'PATCH', 'DELETE')
    resource = falcon_portal_api.GRPHostnameManageResourceApi


class DatabaseServerGRPHostnameBatchSyncManageController(ResourceInterface):
    name = 'database_server.grp_hostname.batch_sync'
    allow_methods = ('PATCH', )
    resource = falcon_portal_api.GRPHostnameManageResourceApi


class DatabaseServerGRPTplManageController(CollectionController):
    name = 'database_server.grp_tpl'
    allow_methods = ('GET', 'POST')
    resource = falcon_portal_api.GRPTplManageResourceApi


class DatabaseServerGRPTplItemManageController(ItemController):
    name = 'database_server.grp_tpl.item'
    allow_methods = ('GET', 'PATCH', 'DELETE')
    resource = falcon_portal_api.GRPTplManageResourceApi


class DatabaseServerGRPTplBatchSyncManageController(ResourceInterface):
    name = 'database_server.grp_tpl.batch_sync'
    allow_methods = ('PATCH', )
    resource = falcon_portal_api.GRPTplManageResourceApi


class DatabaseServerHolidayManageController(CollectionController):
    name = 'database_server.holiday'
    allow_methods = ('GET', 'POST')
    resource = falcon_portal_api.HolidayManageResourceApi


class DatabaseServerHolidayItemManageController(ItemController):
    name = 'database_server.holiday.item'
    allow_methods = ('GET', 'PATCH', 'DELETE')
    resource = falcon_portal_api.HolidayManageResourceApi


class DatabaseServerHolidayBatchSyncManageController(ResourceInterface):
    name = 'database_server.holiday.batch_sync'
    allow_methods = ('PATCH', )
    resource = falcon_portal_api.HolidayManageResourceApi


class DatabaseServerHostMaintainingManageController(CollectionController):
    name = 'database_server.host_maintaining'
    allow_methods = ('GET', 'POST')
    resource = falcon_portal_api.HostMaintainingManageResourceApi


class DatabaseServerHostMaintainingItemManageController(ItemController):
    name = 'database_server.host_maintaining.item'
    allow_methods = ('GET', 'PATCH', 'DELETE')
    resource = falcon_portal_api.HostMaintainingManageResourceApi


class DatabaseServerHostMaintainingBatchSyncManageController(ResourceInterface):
    name = 'database_server.host_maintaining.batch_sync'
    allow_methods = ('PATCH', )
    resource = falcon_portal_api.HostMaintainingManageResourceApi


class DatabaseServerHostTplManageController(CollectionController):
    name = 'database_server.host_tpl'
    allow_methods = ('GET', 'POST')
    resource = falcon_portal_api.HostTplManageResourceApi


class DatabaseServerHostTplItemManageController(ItemController):
    name = 'database_server.host_tpl.item'
    allow_methods = ('GET', 'PATCH', 'DELETE')
    resource = falcon_portal_api.HostTplManageResourceApi


class DatabaseServerHostTplBatchSyncManageController(ResourceInterface):
    name = 'database_server.host_tpl.batch_sync'
    allow_methods = ('PATCH', )
    resource = falcon_portal_api.HostTplManageResourceApi


class DatabaseServerLastPluginVManageController(CollectionController):
    name = 'database_server.last_plugin_v'
    allow_methods = ('GET', 'POST')
    resource = falcon_portal_api.LastPluginVManageResourceApi


class DatabaseServerLastPluginVBatchSyncManageController(ResourceInterface):
    name = 'database_server.last_plugin_v.batch_sync'
    allow_methods = ('PATCH',)
    resource = falcon_portal_api.LastPluginVManageResourceApi


class DatabaseServerLastPluginVItemManageController(ItemController):
    name = 'database_server.last_plugin_v.item'
    allow_methods = ('GET', 'PATCH', 'DELETE')
    resource = falcon_portal_api.LastPluginVManageResourceApi


class DatabaseServerMaintainCounterManageController(CollectionController):
    name = 'database_server.maintain_counter'
    allow_methods = ('GET', 'POST')
    resource = falcon_portal_api.MaintainCounterManageResourceApi


class DatabaseServerMaintainCounterItemManageController(ItemController):
    name = 'database_server.maintain_counter.item'
    allow_methods = ('GET', 'PATCH', 'DELETE')
    resource = falcon_portal_api.MaintainCounterManageResourceApi


class DatabaseServerMaintainCounterBatchSyncManageController(ResourceInterface):
    name = 'database_server.maintain_counter.batch_sync'
    allow_methods = ('PATCH', )
    resource = falcon_portal_api.MaintainCounterManageResourceApi


class DatabaseServerNetPodsConfigManageController(CollectionController):
    name = 'database_server.net_pods_config'
    allow_methods = ('GET', 'POST')
    resource = falcon_portal_api.NetPodsConfigManageResourceApi


class DatabaseServerNetPodsConfigItemManageController(ItemController):
    name = 'database_server.net_pods_config.item'
    allow_methods = ('GET', 'PATCH', 'DELETE')
    resource = falcon_portal_api.NetPodsConfigManageResourceApi


class DatabaseServerNetPodsConfigBatchSyncManageController(ResourceInterface):
    name = 'database_server.net_pods_config.batch_sync'
    allow_methods = ('PATCH', )
    resource = falcon_portal_api.NetPodsConfigManageResourceApi


class DatabaseServerNetlineYSConfigManageController(CollectionController):
    name = 'database_server.netline_ys_config'
    allow_methods = ('GET', 'POST')
    resource = falcon_portal_api.NetlineYSConfigManageResourceApi


class DatabaseServerNetlineYSConfigItemManageController(ItemController):
    name = 'database_server.netline_ys_config.item'
    allow_methods = ('GET', 'PATCH', 'DELETE')
    resource = falcon_portal_api.NetlineYSConfigManageResourceApi


class DatabaseServerNetlineYSConfigBatchSyncManageController(ResourceInterface):
    name = 'database_server.netline_ys_config.batch_sync'
    allow_methods = ('PATCH', )
    resource = falcon_portal_api.NetlineYSConfigManageResourceApi


class DatabaseServerPluginDirManageController(CollectionController):
    name = 'database_server.plugin_dir'
    allow_methods = ('GET', 'POST')
    resource = falcon_portal_api.PluginDirManageResourceApi


class DatabaseServerPluginDirItemManageController(ItemController):
    name = 'database_server.plugin_dir.item'
    allow_methods = ('GET', 'PATCH', 'DELETE')
    resource = falcon_portal_api.PluginDirManageResourceApi


class DatabaseServerPluginDirBatchSyncManageController(ResourceInterface):
    name = 'database_server.plugin_dir.batch_sync'
    allow_methods = ('PATCH', )
    resource = falcon_portal_api.PluginDirManageResourceApi


class DatabaseServerStorageAlertManageController(CollectionController):
    name = 'database_server.storage_alert'
    allow_methods = ('GET', 'POST')
    resource = falcon_portal_api.StorageAlertManageResourceApi


class DatabaseServerStorageAlertItemManageController(ItemController):
    name = 'database_server.storage_alert.item'
    allow_methods = ('GET', 'PATCH', 'DELETE')
    resource = falcon_portal_api.StorageAlertManageResourceApi


class DatabaseServerStorageAlertBatchSyncManageController(ResourceInterface):
    name = 'database_server.storage_alert.batch_sync'
    allow_methods = ('PATCH', )
    resource = falcon_portal_api.StorageAlertManageResourceApi


class DatabaseServerStorageCMDBManageController(CollectionController):
    name = 'database_server.storage_cmdb'
    allow_methods = ('GET', 'POST')
    resource = falcon_portal_api.StorageCMDBManageResourceApi


class DatabaseServerStorageCMDBItemManageController(ItemController):
    name = 'database_server.storage_cmdb.item'
    allow_methods = ('GET', 'PATCH', 'DELETE')
    resource = falcon_portal_api.StorageCMDBManageResourceApi


class DatabaseServerStorageCMDBBatchSyncManageController(ResourceInterface):
    name = 'database_server.storage_cmdb.batch_sync'
    allow_methods = ('PATCH', )
    resource = falcon_portal_api.StorageCMDBManageResourceApi


class DatabaseServerStorageStrategyManageController(CollectionController):
    name = 'database_server.storage_strategy'
    allow_methods = ('GET', 'POST')
    resource = falcon_portal_api.StorageStrategyManageResourceApi


class DatabaseServerStorageStrategyItemManageController(ItemController):
    name = 'database_server.storage_strategy.item'
    allow_methods = ('GET', 'PATCH', 'DELETE')
    resource = falcon_portal_api.StorageStrategyManageResourceApi


class DatabaseServerStorageStrategyBatchSyncManageController(ResourceInterface):
    name = 'database_server.storage_strategy.batch_sync'
    allow_methods = ('PATCH', )
    resource = falcon_portal_api.StorageStrategyManageResourceApi


class DatabaseServerStrategyManageController(CollectionController):
    name = 'database_server.strategy'
    allow_methods = ('GET', 'POST')
    resource = falcon_portal_api.StrategyManageResourceApi


class DatabaseServerStrategyItemManageController(ItemController):
    name = 'database_server.strategy.item'
    allow_methods = ('GET', 'PATCH', 'DELETE')
    resource = falcon_portal_api.StrategyManageResourceApi


class DatabaseServerStrategyBatchSyncManageController(ResourceInterface):
    name = 'database_server.strategy.batch_sync'
    allow_methods = ('PATCH', )
    resource = falcon_portal_api.StrategyManageResourceApi


class DatabaseServerStrategyCallbackManageController(CollectionController):
    name = 'database_server.strategy_callback'
    allow_methods = ('GET', 'POST')
    resource = falcon_portal_api.StrategyCallbackManageResourceApi


class DatabaseServerStrategyCallbackItemManageController(ItemController):
    name = 'database_server.strategy_callback.item'
    allow_methods = ('GET', 'PATCH', 'DELETE')
    resource = falcon_portal_api.StrategyCallbackManageResourceApi


class DatabaseServerStrategyCallbackBatchSyncManageController(ResourceInterface):
    name = 'database_server.strategy_callback.batch_sync'
    allow_methods = ('PATCH', )
    resource = falcon_portal_api.StrategyCallbackManageResourceApi


class DatabaseServerTPLManageController(CollectionController):
    name = 'database_server.tpl'
    allow_methods = ('GET', 'POST')
    resource = falcon_portal_api.TPLManageResourceApi


class DatabaseServerTPLItemManageController(ItemController):
    name = 'database_server.tpl.item'
    allow_methods = ('GET', 'PATCH', 'DELETE')
    resource = falcon_portal_api.TPLManageResourceApi


class DatabaseServerTPLBatchSyncManageController(ResourceInterface):
    name = 'database_server.tpl.batch_sync'
    allow_methods = ('PATCH', )
    resource = falcon_portal_api.TPLManageResourceApi


class DatabaseServerUnitManageController(CollectionController):
    name = 'database_server.unit'
    allow_methods = ('GET', 'POST')
    resource = falcon_portal_api.UnitManageResourceApi


class DatabaseServerUnitItemManageController(ItemController):
    name = 'database_server.unit.item'
    allow_methods = ('GET', 'PATCH', 'DELETE')
    resource = falcon_portal_api.UnitManageResourceApi


class DatabaseServerUnitBatchSyncManageController(ResourceInterface):
    name = 'database_server.unit.batch_sync'
    allow_methods = ('PATCH', )
    resource = falcon_portal_api.UnitManageResourceApi


class DatabaseServerUpgrateAgentVersionManageController(CollectionController):
    name = 'database_server.upgrate_agent_version'
    allow_methods = ('GET', 'POST')
    resource = falcon_portal_api.UpgrateAgentVersionManageResourceApi


class DatabaseServerUpgrateAgentVersionItemManageController(ItemController):
    name = 'database_server.upgrate_agent_version.item'
    allow_methods = ('GET', 'PATCH', 'DELETE')
    resource = falcon_portal_api.UpgrateAgentVersionManageResourceApi


class DatabaseServerUpgrateAgentVersionBatchSyncManageController(ResourceInterface):
    name = 'database_server.upgrate_agent_version.batch_sync'
    allow_methods = ('PATCH', )
    resource = falcon_portal_api.UpgrateAgentVersionManageResourceApi


class DatabaseServerUrlMonitorManageController(CollectionController):
    name = 'database_server.url_monitor'
    allow_methods = ('GET', 'POST')
    resource = falcon_portal_api.UrlMonitorManageResourceApi


class DatabaseServerUrlMonitorItemManageController(ItemController):
    name = 'database_server.url_monitor.item'
    allow_methods = ('GET', 'PATCH', 'DELETE')
    resource = falcon_portal_api.UrlMonitorManageResourceApi


class DatabaseServerUrlMonitorBatchSyncManageController(ResourceInterface):
    name = 'database_server.url_monitor.batch_sync'
    allow_methods = ('PATCH', )
    resource = falcon_portal_api.UrlMonitorManageResourceApi


class DatabaseServerUserHostManageController(CollectionController):
    name = 'database_server.user_host'
    allow_methods = ('GET', 'POST')
    resource = falcon_portal_api.UserHostManageResourceApi


class DatabaseServerUserHostItemManageController(ItemController):
    name = 'database_server.user_host.item'
    allow_methods = ('GET', 'PATCH', 'DELETE')
    resource = falcon_portal_api.UserHostManageResourceApi


class DatabaseServerUserHostBatchSyncManageController(ResourceInterface):
    name = 'database_server.user_host.batch_sync'
    allow_methods = ('PATCH', )
    resource = falcon_portal_api.UserHostManageResourceApi


class DatabaseServerSystemGroupManageController(CollectionController):
    name = 'database_server.system_group'
    allow_methods = ('GET', 'POST')
    resource = falcon_portal_api.SystemGroupManageResourceApi


class DatabaseServerSystemGroupItemManageController(ItemController):
    name = 'database_server.system_group.item'
    allow_methods = ('GET', 'PATCH', 'DELETE')
    resource = falcon_portal_api.SystemGroupManageResourceApi


class DatabaseServerSystemGroupBatchSyncManageController(ResourceInterface):
    name = 'database_server.system_group.batch_sync'
    allow_methods = ('PATCH', )
    resource = falcon_portal_api.SystemGroupManageResourceApi


class DatabaseServerSystemManageController(CollectionController):
    name = 'database_server.system'
    allow_methods = ('GET', 'POST')
    resource = falcon_portal_api.SystemManageResourceApi


class DatabaseServerSystemItemManageController(ItemController):
    name = 'database_server.system.item'
    allow_methods = ('GET', 'PATCH', 'DELETE')
    resource = falcon_portal_api.SystemManageResourceApi


class DatabaseServerSystemBatchSyncManageController(ResourceInterface):
    name = 'database_server.system.batch_sync'
    allow_methods = ('PATCH',)
    resource = falcon_portal_api.SystemManageResourceApi


class DatabaseServerSubSystemManageController(CollectionController):
    name = 'database_server.subsystem'
    allow_methods = ('GET', 'POST')
    resource = falcon_portal_api.SubSystemManageResourceApi


class DatabaseServerSubSystemItemManageController(ItemController):
    name = 'database_server.subsystem.item'
    allow_methods = ('GET', 'PATCH', 'DELETE')
    resource = falcon_portal_api.SubSystemManageResourceApi


class DatabaseServerSubSystemBatchSyncManageController(ResourceInterface):
    name = 'database_server.subsystem.batch_sync'
    allow_methods = ('PATCH',)
    resource = falcon_portal_api.SubSystemManageResourceApi


class DatabaseServerPublishUnitManageController(CollectionController):
    name = 'database_server.publish_unit'
    allow_methods = ('GET', 'POST')
    resource = falcon_portal_api.PublishUnitManageResourceApi


class DatabaseServerPublishUnitItemManageController(ItemController):
    name = 'database_server.publish_unit.item'
    allow_methods = ('GET', 'PATCH', 'DELETE')
    resource = falcon_portal_api.PublishUnitManageResourceApi


class DatabaseServerPublishUnitBatchSyncManageController(ResourceInterface):
    name = 'database_server.publish_unit.batch_sync'
    allow_methods = ('PATCH',)
    resource = falcon_portal_api.PublishUnitManageResourceApi


class DatabaseServerUnitInstanceManageController(CollectionController):
    name = 'database_server.unit_instance'
    allow_methods = ('GET', 'POST')
    resource = falcon_portal_api.UnitInstanceManageResourceApi


class DatabaseServerUnitInstanceItemManageController(ItemController):
    name = 'database_server.unit_instance.item'
    allow_methods = ('GET', 'PATCH', 'DELETE')
    resource = falcon_portal_api.UnitInstanceManageResourceApi


class DatabaseServerUnitInstanceBatchSyncManageController(ResourceInterface):
    name = 'database_server.unit_instance.batch_sync'
    allow_methods = ('PATCH',)
    resource = falcon_portal_api.UnitInstanceManageResourceApi


class DatabaseServerIamPolicyManageController(CollectionController):
    name = 'database_server.iam_policy'
    allow_methods = ('GET',)
    resource = falcon_portal_api.IamPolicyManageResourceApi
