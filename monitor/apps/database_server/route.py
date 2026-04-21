# coding: utf-8
from __future__ import absolute_import

from monitor.apps.database_server.alarms_controller import *
from monitor.apps.database_server.dashboard_controller import *
from monitor.apps.database_server.falcon_portal_controller import *
from monitor.apps.database_server.graph_controller import *
from monitor.apps.database_server.uic_controller import *


def add_routes(api):
    # falcon_portal下的表
    api.add_route('/v1/database_server/host_report', DatabaseServerHostReportManageController())
    api.add_route('/v1/database_server/host_report/batch_sync', DatabaseServerHostReportBatchSyncManageController())
    api.add_route('/v1/database_server/host_report/{rid}', DatabaseServerHostReportItemManageController())

    api.add_route('/v1/database_server/host', DatabaseServerHostManageController())
    api.add_route('/v1/database_server/host/batch_sync', DatabaseServerHostBatchSyncManageController())
    api.add_route('/v1/database_server/host/{rid}', DatabaseServerHostItemManageController())

    api.add_route('/v1/database_server/available_zone', DatabaseServerAvailableZoneManageController())
    api.add_route('/v1/database_server/available_zone/batch_sync', DatabaseServerAvailableZoneBatchSyncManageController())
    api.add_route('/v1/database_server/available_zone/{rid}', DatabaseServerAvailableZoneItemManageController())

    api.add_route('/v1/database_server/if_region', DatabaseServerIfRegionManageController())
    api.add_route('/v1/database_server/if_region/batch_sync',
                  DatabaseServerIfRegionBatchSyncManageController())
    api.add_route('/v1/database_server/if_region/{rid}', DatabaseServerIfRegionItemManageController())

    api.add_route('/v1/database_server/capacity_metric', DatabaseServerCapacityMetricManageController())
    api.add_route('/v1/database_server/capacity_metric/batch_sync',
                  DatabaseServerCapacityMetricBatchSyncManageController())
    api.add_route('/v1/database_server/capacity_metric/{rid}', DatabaseServerCapacityMetricItemManageController())

    api.add_route('/v1/database_server/capacity_metric_filter_strategy', DatabaseServerCapacityMetricFilterStrategyManageController())
    api.add_route('/v1/database_server/capacity_metric_filter_strategy/batch_sync',
                  DatabaseServerCapacityMetricFilterStrategyBatchSyncManageController())
    api.add_route('/v1/database_server/capacity_metric_filter_strategy/{rid}', DatabaseServerCapacityMetricFilterStrategyItemManageController())

    api.add_route('/v1/database_server/host_resource_capacity',
                  DatabaseServerHostResourceCapacityManageController())
    api.add_route('/v1/database_server/host_resource_capacity/batch_sync',
                  DatabaseServerHostResourceCapacityBatchSyncManageController())
    api.add_route('/v1/database_server/host_resource_capacity/{rid}',
                  DatabaseServerHostResourceCapacityItemManageController())

    api.add_route('/v1/database_server/host_resource_capacity_week',
                  DatabaseServerHostResourceCapacityWeekManageController())
    api.add_route('/v1/database_server/host_resource_capacity_week/batch_sync',
                  DatabaseServerHostResourceCapacityWeekBatchSyncManageController())
    api.add_route('/v1/database_server/host_resource_capacity_week/{rid}',
                  DatabaseServerHostResourceCapacityWeekItemManageController())

    api.add_route('/v1/database_server/host_resource_capacity_month',
                  DatabaseServerHostResourceCapacityMonthManageController())

    api.add_route('/v1/database_server/project', DatabaseServerProjectManageController())
    api.add_route('/v1/database_server/project/batch_sync', DatabaseServerProjectBatchSyncManageController())
    api.add_route('/v1/database_server/project/{rid}', DatabaseServerProjectItemManageController())

    api.add_route('/v1/database_server/tenant', DatabaseServerTenantManageController())
    api.add_route('/v1/database_server/tenant/batch_sync', DatabaseServerTenantBatchSyncManageController())
    api.add_route('/v1/database_server/tenant/{rid}', DatabaseServerTenantItemManageController())

    api.add_route('/v1/database_server/cmdb_db', DatabaseServerCMDBDBManageController())
    api.add_route('/v1/database_server/cmdb_db/batch_sync', DatabaseServerCMDBDBBatchSyncManageController())
    api.add_route('/v1/database_server/cmdb_db/{rid}', DatabaseServerCMDBDBItemManageController())

    api.add_route('/v1/database_server/environment', DatabaseServerEnvironmentManageController())
    api.add_route('/v1/database_server/environment/batch_sync', DatabaseServerEnvironmentBatchSyncManageController())
    api.add_route('/v1/database_server/environment/{rid}', DatabaseServerEnvironmentItemManageController())

    api.add_route('/v1/database_server/if_wan', DatabaseServerIfWanManageController())
    api.add_route('/v1/database_server/if_wan/batch_sync', DatabaseServerIfWanBatchSyncManageController())
    api.add_route('/v1/database_server/if_wan/{rid}', DatabaseServerIfWanItemManageController())

    api.add_route('/v1/database_server/sw_iprange', DatabaseServerSWIprangeManageController())
    api.add_route('/v1/database_server/sw_iprange/batch_sync', DatabaseServerSWIprangeBatchSyncManageController())
    api.add_route('/v1/database_server/sw_iprange/{rid}', DatabaseServerSWIprangeItemManageController())

    api.add_route('/v1/database_server/sw_oids', DatabaseServerSWOIDSManageController())
    api.add_route('/v1/database_server/sw_oids/batch_sync', DatabaseServerSWOIDSBatchSyncManageController())
    api.add_route('/v1/database_server/sw_oids/{rid}', DatabaseServerSWOIDSItemManageController())

    api.add_route('/v1/database_server/if_hardware_model', DatabaseServerIfHardwareModelManageController())
    api.add_route('/v1/database_server/if_hardware_model/batch_sync', DatabaseServerIfHardwareModelBatchSyncManageController())
    api.add_route('/v1/database_server/if_hardware_model/{rid}', DatabaseServerIfHardwareModelItemManageController())

    api.add_route('/v1/database_server/net_pods', DatabaseServerNetPodsManageController())
    api.add_route('/v1/database_server/net_pods/batch_sync', DatabaseServerNetPodsBatchSyncManageController())
    api.add_route('/v1/database_server/net_pods/{rid}', DatabaseServerNetPodsItemManageController())

    api.add_route('/v1/database_server/net_subs', DatabaseServerNetSubsManageController())
    api.add_route('/v1/database_server/net_subs/batch_sync', DatabaseServerNetSubsBatchSyncManageController())
    api.add_route('/v1/database_server/net_subs/{rid}', DatabaseServerNetSubsItemManageController())

    api.add_route('/v1/database_server/network_rels', DatabaseServerNetworkRelsManageController())
    api.add_route('/v1/database_server/network_rels/batch_sync', DatabaseServerNetworkRelsBatchSyncManageController())
    api.add_route('/v1/database_server/network_rels/{rid}', DatabaseServerNetworkRelsItemManageController())

    api.add_route('/v1/database_server/module', DatabaseServerModuleManageController())
    api.add_route('/v1/database_server/module/batch_sync', DatabaseServerModuleBatchSyncManageController())
    api.add_route('/v1/database_server/module/{rid}', DatabaseServerModuleItemManageController())

    api.add_route('/v1/database_server/cmdb_host', DatabaseServerCMDBHostManageController())
    api.add_route('/v1/database_server/cmdb_host/batch_sync', DatabaseServerCMDBHostBatchSyncManageController())
    api.add_route('/v1/database_server/cmdb_host/{rid}', DatabaseServerCMDBHostItemManageController())

    api.add_route('/v1/database_server/cmdb_db_instance', DatabaseServerCMDBDBInstanceManageController())
    api.add_route('/v1/database_server/cmdb_db_instance/batch_sync', DatabaseServerCMDBDBInstanceBatchSyncManageController())
    api.add_route('/v1/database_server/cmdb_db_instance/{rid}', DatabaseServerCMDBDBInstanceItemManageController())

    api.add_route('/v1/database_server/action', DatabaseServerActionManageController())
    api.add_route('/v1/database_server/action/batch_sync', DatabaseServerActionBatchSyncManageController())
    api.add_route('/v1/database_server/action/{rid}', DatabaseServerActionItemManageController())

    api.add_route('/v1/database_server/action_user', DatabaseServerActionUserManageController())
    api.add_route('/v1/database_server/action_user/batch_sync', DatabaseServerActionUserBatchSyncManageController())
    api.add_route('/v1/database_server/action_user/{rid}', DatabaseServerActionUserItemManageController())

    api.add_route('/v1/database_server/alarm_other', DatabaseServerAlarmOtherManageController())
    api.add_route('/v1/database_server/alarm_other/batch_sync', DatabaseServerAlarmOtherBatchSyncManageController())
    api.add_route('/v1/database_server/alarm_other/{rid}', DatabaseServerAlarmOtherItemManageController())

    api.add_route('/v1/database_server/alarm_sche', DatabaseServerAlarmScheManageController())
    api.add_route('/v1/database_server/alarm_sche/batch_sync', DatabaseServerAlarmScheBatchSyncManageController())
    api.add_route('/v1/database_server/alarm_sche/{rid}', DatabaseServerAlarmScheItemManageController())

    api.add_route('/v1/database_server/alarm_text_cfg', DatabaseServerAlarmTextCFGManageController())
    api.add_route('/v1/database_server/alarm_text_cfg/batch_sync', DatabaseServerAlarmTextCFGBatchSyncManageController())
    api.add_route('/v1/database_server/alarm_text_cfg/{rid}', DatabaseServerAlarmTextCFGItemManageController())

    api.add_route('/v1/database_server/alarm_type', DatabaseServerAlarmTypeManageController())
    api.add_route('/v1/database_server/alarm_type/batch_sync', DatabaseServerAlarmTypeBatchSyncManageController())
    api.add_route('/v1/database_server/alarm_type/{rid}', DatabaseServerAlarmTypeItemManageController())

    api.add_route('/v1/database_server/bigdata_alert', DatabaseServerBigDataAlertManageController())
    api.add_route('/v1/database_server/bigdata_alert/batch_sync', DatabaseServerBigDataAlertBatchSyncManageController())
    api.add_route('/v1/database_server/bigdata_alert/{rid}', DatabaseServerBigDataAlertItemManageController())

    api.add_route('/v1/database_server/check_ip', DatabaseServerCheckIPManageController())
    api.add_route('/v1/database_server/check_ip/batch_sync', DatabaseServerCheckIPBatchSyncManageController())
    api.add_route('/v1/database_server/check_ip/{rid}', DatabaseServerCheckIPItemManageController())

    api.add_route('/v1/database_server/check_ip_port', DatabaseServerCheckIPPortManageController())
    api.add_route('/v1/database_server/check_ip_port/batch_sync', DatabaseServerCheckIPPortBatchSyncManageController())
    api.add_route('/v1/database_server/check_ip_port/{rid}', DatabaseServerCheckIPPortItemManageController())

    api.add_route('/v1/database_server/check_point', DatabaseServerCheckPointManageController())
    api.add_route('/v1/database_server/check_point/batch_sync', DatabaseServerCheckPointBatchSyncManageController())
    api.add_route('/v1/database_server/check_point/{rid}', DatabaseServerCheckPointItemManageController())

    api.add_route('/v1/database_server/cluster', DatabaseServerClusterManageController())
    api.add_route('/v1/database_server/cluster/batch_sync', DatabaseServerClusterBatchSyncManageController())
    api.add_route('/v1/database_server/cluster/{rid}', DatabaseServerClusterItemManageController())

    api.add_route('/v1/database_server/cmdb_sys', DatabaseServerCmdbSYSManageController())
    api.add_route('/v1/database_server/cmdb_sys/batch_sync', DatabaseServerCmdbSYSBatchSyncManageController())
    api.add_route('/v1/database_server/cmdb_sys/{rid}', DatabaseServerCmdbSYSItemManageController())

    api.add_route('/v1/database_server/cmdb_sys_sec', DatabaseServerCmdbSYSSecManageController())
    api.add_route('/v1/database_server/cmdb_sys_sec/batch_sync', DatabaseServerCmdbSYSSecBatchSyncManageController())
    api.add_route('/v1/database_server/cmdb_sys_sec/{rid}', DatabaseServerCmdbSYSSecItemManageController())

    api.add_route('/v1/database_server/config_kv', DatabaseServerConfigKVManageController())
    api.add_route('/v1/database_server/config_kv/batch_sync', DatabaseServerConfigKVBatchSyncManageController())
    api.add_route('/v1/database_server/config_kv/{rid}', DatabaseServerConfigKVItemManageController())

    api.add_route('/v1/database_server/counter', DatabaseServerCounterManageController())
    api.add_route('/v1/database_server/counter/batch_sync', DatabaseServerCounterBatchSyncManageController())
    api.add_route('/v1/database_server/counter/{rid}', DatabaseServerCounterItemManageController())

    api.add_route('/v1/database_server/custom_alert', DatabaseServerCustomAlertManageController())
    api.add_route('/v1/database_server/custom_alert/batch_sync', DatabaseServerCustomAlertBatchSyncManageController())
    api.add_route('/v1/database_server/custom_alert/{rid}', DatabaseServerCustomAlertItemManageController())

    api.add_route('/v1/database_server/custom_counter', DatabaseServerCustomCounterManageController())
    api.add_route('/v1/database_server/custom_counter/batch_sync', DatabaseServerCustomCounterBatchSyncManageController())
    api.add_route('/v1/database_server/custom_counter/{rid}', DatabaseServerCustomCounterItemManageController())

    api.add_route('/v1/database_server/expression', DatabaseServerExpressionManageController())
    api.add_route('/v1/database_server/expression/batch_sync', DatabaseServerExpressionBatchSyncManageController())
    api.add_route('/v1/database_server/expression/{rid}', DatabaseServerExpressionItemManageController())

    api.add_route('/v1/database_server/grp', DatabaseServerGRPManageController())
    api.add_route('/v1/database_server/grp/batch_sync', DatabaseServerGRPBatchSyncManageController())
    api.add_route('/v1/database_server/grp/{rid}', DatabaseServerGRPItemManageController())

    api.add_route('/v1/database_server/grp_host', DatabaseServerGRPHostManageController())
    api.add_route('/v1/database_server/grp_host/batch_sync', DatabaseServerGRPHostBatchSyncManageController())
    api.add_route('/v1/database_server/grp_host/{rid}', DatabaseServerGRPHostItemManageController())

    api.add_route('/v1/database_server/grp_hostname', DatabaseServerGRPHostnameManageController())
    api.add_route('/v1/database_server/grp_hostname/batch_sync', DatabaseServerGRPHostnameBatchSyncManageController())
    api.add_route('/v1/database_server/grp_hostname/{rid}', DatabaseServerGRPHostnameItemManageController())

    api.add_route('/v1/database_server/grp_tpl', DatabaseServerGRPTplManageController())
    api.add_route('/v1/database_server/grp_tpl/batch_sync', DatabaseServerGRPTplBatchSyncManageController())
    api.add_route('/v1/database_server/grp_tpl/{rid}', DatabaseServerGRPTplItemManageController())

    api.add_route('/v1/database_server/holiday', DatabaseServerHolidayManageController())
    api.add_route('/v1/database_server/holiday/batch_sync', DatabaseServerHolidayBatchSyncManageController())
    api.add_route('/v1/database_server/holiday/{rid}', DatabaseServerHolidayItemManageController())

    api.add_route('/v1/database_server/host_maintaining', DatabaseServerHostMaintainingManageController())
    api.add_route('/v1/database_server/host_maintaining/batch_sync', DatabaseServerHostMaintainingBatchSyncManageController())
    api.add_route('/v1/database_server/host_maintaining/{rid}', DatabaseServerHostMaintainingItemManageController())

    api.add_route('/v1/database_server/host_tpl', DatabaseServerHostTplManageController())
    api.add_route('/v1/database_server/host_tpl/batch_sync', DatabaseServerHostTplBatchSyncManageController())
    api.add_route('/v1/database_server/host_tpl/{rid}', DatabaseServerHostTplItemManageController())

    api.add_route('/v1/database_server/last_plugin_v', DatabaseServerLastPluginVManageController())
    api.add_route('/v1/database_server/last_plugin_v/batch_sync', DatabaseServerLastPluginVBatchSyncManageController())
    api.add_route('/v1/database_server/last_plugin_v/{rid}', DatabaseServerLastPluginVItemManageController())

    api.add_route('/v1/database_server/maintain_counter', DatabaseServerMaintainCounterManageController())
    api.add_route('/v1/database_server/maintain_counter/batch_sync', DatabaseServerMaintainCounterBatchSyncManageController())
    api.add_route('/v1/database_server/maintain_counter/{rid}', DatabaseServerMaintainCounterItemManageController())

    api.add_route('/v1/database_server/net_pods_config', DatabaseServerNetPodsConfigManageController())
    api.add_route('/v1/database_server/net_pods_config/batch_sync', DatabaseServerNetPodsConfigBatchSyncManageController())
    api.add_route('/v1/database_server/net_pods_config/{rid}', DatabaseServerNetPodsConfigItemManageController())

    api.add_route('/v1/database_server/netline_ys_config', DatabaseServerExpressionManageController())
    api.add_route('/v1/database_server/netline_ys_config/batch_sync', DatabaseServerNetlineYSConfigBatchSyncManageController())
    api.add_route('/v1/database_server/netline_ys_config/{rid}', DatabaseServerNetlineYSConfigItemManageController())

    api.add_route('/v1/database_server/plugin_dir', DatabaseServerPluginDirManageController())
    api.add_route('/v1/database_server/plugin_dir/batch_sync', DatabaseServerPluginDirBatchSyncManageController())
    api.add_route('/v1/database_server/plugin_dir/{rid}', DatabaseServerPluginDirItemManageController())

    api.add_route('/v1/database_server/storage_alert', DatabaseServerStorageAlertManageController())
    api.add_route('/v1/database_server/storage_alert/batch_sync', DatabaseServerStorageAlertBatchSyncManageController())
    api.add_route('/v1/database_server/storage_alert/{rid}', DatabaseServerStorageAlertItemManageController())

    api.add_route('/v1/database_server/storage_cmdb', DatabaseServerStorageCMDBManageController())
    api.add_route('/v1/database_server/storage_cmdb/batch_sync', DatabaseServerStorageCMDBBatchSyncManageController())
    api.add_route('/v1/database_server/storage_cmdb/{rid}', DatabaseServerStorageCMDBItemManageController())

    api.add_route('/v1/database_server/storage_strategy', DatabaseServerStorageStrategyManageController())
    api.add_route('/v1/database_server/storage_strategy/batch_sync', DatabaseServerStorageStrategyBatchSyncManageController())
    api.add_route('/v1/database_server/storage_strategy/{rid}', DatabaseServerStorageStrategyItemManageController())

    api.add_route('/v1/database_server/strategy', DatabaseServerStrategyManageController())
    api.add_route('/v1/database_server/strategy/batch_sync', DatabaseServerStrategyBatchSyncManageController())
    api.add_route('/v1/database_server/strategy/{rid}', DatabaseServerStrategyItemManageController())

    api.add_route('/v1/database_server/strategy_callback', DatabaseServerStrategyCallbackManageController())
    api.add_route('/v1/database_server/strategy_callback/batch_sync', DatabaseServerStrategyCallbackBatchSyncManageController())
    api.add_route('/v1/database_server/strategy_callback/{rid}', DatabaseServerStorageCMDBItemManageController())

    api.add_route('/v1/database_server/tpl', DatabaseServerTPLManageController())
    api.add_route('/v1/database_server/tpl/batch_sync', DatabaseServerTPLBatchSyncManageController())
    api.add_route('/v1/database_server/tpl/{rid}', DatabaseServerTPLItemManageController())

    api.add_route('/v1/database_server/unit', DatabaseServerUnitManageController())
    api.add_route('/v1/database_server/unit/batch_sync', DatabaseServerUnitBatchSyncManageController())
    api.add_route('/v1/database_server/unit/{rid}', DatabaseServerUnitItemManageController())

    api.add_route('/v1/database_server/upgrate_agent_version', DatabaseServerUpgrateAgentVersionManageController())
    api.add_route('/v1/database_server/upgrate_agent_version/batch_sync', DatabaseServerUpgrateAgentVersionBatchSyncManageController())
    api.add_route('/v1/database_server/upgrate_agent_version/{rid}', DatabaseServerUpgrateAgentVersionItemManageController())

    api.add_route('/v1/database_server/url_monitor', DatabaseServerUrlMonitorManageController())
    api.add_route('/v1/database_server/url_monitor/batch_sync', DatabaseServerUrlMonitorBatchSyncManageController())
    api.add_route('/v1/database_server/url_monitor/{rid}', DatabaseServerUrlMonitorItemManageController())

    api.add_route('/v1/database_server/user_host', DatabaseServerUserHostManageController())
    api.add_route('/v1/database_server/user_host/batch_sync', DatabaseServerUserHostBatchSyncManageController())
    api.add_route('/v1/database_server/user_host/{rid}', DatabaseServerUserHostItemManageController())

    api.add_route('/v1/database_server/system_group', DatabaseServerSystemGroupManageController())
    api.add_route('/v1/database_server/system_group/batch_sync', DatabaseServerSystemGroupBatchSyncManageController())
    api.add_route('/v1/database_server/system_group/{rid}', DatabaseServerSystemGroupItemManageController())

    api.add_route('/v1/database_server/system', DatabaseServerSystemManageController())
    api.add_route('/v1/database_server/system/batch_sync', DatabaseServerSystemBatchSyncManageController())
    api.add_route('/v1/database_server/system/{rid}', DatabaseServerSystemItemManageController())

    api.add_route('/v1/database_server/subsystem', DatabaseServerSubSystemManageController())
    api.add_route('/v1/database_server/subsystem/batch_sync', DatabaseServerSubSystemBatchSyncManageController())
    api.add_route('/v1/database_server/subsystem/{rid}', DatabaseServerSubSystemItemManageController())

    api.add_route('/v1/database_server/publish_unit', DatabaseServerPublishUnitManageController())
    api.add_route('/v1/database_server/publish_unit/batch_sync', DatabaseServerPublishUnitBatchSyncManageController())
    api.add_route('/v1/database_server/publish_unit/{rid}', DatabaseServerPublishUnitItemManageController())

    api.add_route('/v1/database_server/unit_instance', DatabaseServerUnitInstanceManageController())
    api.add_route('/v1/database_server/unit_instance/batch_sync', DatabaseServerUnitInstanceBatchSyncManageController())
    api.add_route('/v1/database_server/unit_instance/{rid}', DatabaseServerUnitInstanceItemManageController())

    api.add_route('/v1/database_server/iam_policy', DatabaseServerIamPolicyManageController())

    # alarms下的表
    api.add_route('/v1/database_server/event_cases', DatabaseServerEventCasesManageController())
    api.add_route('/v1/database_server/event_cases/batch_sync', DatabaseServerEventCasesBatchSyncManageController())
    api.add_route('/v1/database_server/event_cases/{rid}', DatabaseServerEventCasesItemManageController())

    api.add_route('/v1/database_server/alarm_status', DatabaseServerAlarmStatusManageController())
    api.add_route('/v1/database_server/alarm_status/batch_sync', DatabaseServerAlarmStatusBatchSyncManageController())
    api.add_route('/v1/database_server/alarm_status/{rid}', DatabaseServerAlarmStatusItemManageController())

    api.add_route('/v1/database_server/del_log', DatabaseServerDelLogManageController())
    api.add_route('/v1/database_server/del_log/batch_sync', DatabaseServerDelLogBatchSyncManageController())
    api.add_route('/v1/database_server/del_log/{rid}', DatabaseServerDelLogItemManageController())

    api.add_route('/v1/database_server/event_report', DatabaseServerEventReportManageController())
    api.add_route('/v1/database_server/event_report/batch_sync', DatabaseServerEventReportBatchSyncManageController())
    api.add_route('/v1/database_server/event_report/{rid}', DatabaseServerEventReportItemManageController())

    api.add_route('/v1/database_server/events', DatabaseServerEventsManageController())
    api.add_route('/v1/database_server/events/batch_sync', DatabaseServerEventsBatchSyncManageController())
    api.add_route('/v1/database_server/events/{rid}', DatabaseServerEventsItemManageController())

    api.add_route('/v1/database_server/remark_common', DatabaseServerRemarkCommonManageController())
    api.add_route('/v1/database_server/remark_common/batch_sync', DatabaseServerRemarkCommonBatchSyncManageController())
    api.add_route('/v1/database_server/remark_common/{rid}', DatabaseServerRemarkCommonItemManageController())

    # dashboard下的表
    api.add_route('/v1/database_server/button', DatabaseServerButtonManageController())
    api.add_route('/v1/database_server/button/batch_sync', DatabaseServerButtonBatchSyncManageController())
    api.add_route('/v1/database_server/button/{rid}', DatabaseServerButtonItemManageController())

    api.add_route('/v1/database_server/chart', DatabaseServerChartManageController())
    api.add_route('/v1/database_server/chart/batch_sync', DatabaseServerChartBatchSyncManageController())
    api.add_route('/v1/database_server/chart/{rid}', DatabaseServerChartItemManageController())

    api.add_route('/v1/database_server/custom_dashboard', DatabaseServerCustomDashBoardManageController())
    api.add_route('/v1/database_server/custom_dashboard/batch_sync', DatabaseServerCustomDashBoardBatchSyncManageController())
    api.add_route('/v1/database_server/custom_dashboard/{rid}', DatabaseServerCustomDashBoardItemManageController())

    api.add_route('/v1/database_server/dashboard', DatabaseServerDashBoardManageController())
    api.add_route('/v1/database_server/dashboard/batch_sync', DatabaseServerDashBoardBatchSyncManageController())
    api.add_route('/v1/database_server/dashboard/{rid}', DatabaseServerDashBoardItemManageController())

    api.add_route('/v1/database_server/dashboard_graph', DatabaseServerDashBoardGraphManageController())
    api.add_route('/v1/database_server/dashboard_graph/batch_sync', DatabaseServerDashBoardGraphBatchSyncManageController())
    api.add_route('/v1/database_server/dashboard_graph/{rid}', DatabaseServerDashBoardGraphItemManageController())

    api.add_route('/v1/database_server/dashboard_screen', DatabaseServerDashBoardScreenManageController())
    api.add_route('/v1/database_server/dashboard_screen/batch_sync', DatabaseServerDashBoardScreenBatchSyncManageController())
    api.add_route('/v1/database_server/dashboard_screen/{rid}', DatabaseServerDashBoardScreenItemManageController())

    api.add_route('/v1/database_server/host_screen_cfg', DatabaseServerHostScreenCFGManageController())
    api.add_route('/v1/database_server/host_screen_cfg/batch_sync', DatabaseServerHostScreenCFGBatchSyncManageController())
    api.add_route('/v1/database_server/host_screen_cfg/{rid}', DatabaseServerHostScreenCFGItemManageController())

    api.add_route('/v1/database_server/message', DatabaseServerMessageManageController())
    api.add_route('/v1/database_server/message/batch_sync', DatabaseServerMessageBatchSyncManageController())
    api.add_route('/v1/database_server/message/{rid}', DatabaseServerMessageItemManageController())

    api.add_route('/v1/database_server/option', DatabaseServerOptionManageController())
    api.add_route('/v1/database_server/option/batch_sync', DatabaseServerOptionBatchSyncManageController())
    api.add_route('/v1/database_server/option/{rid}', DatabaseServerOptionItemManageController())

    api.add_route('/v1/database_server/panel', DatabaseServerPanelManageController())
    api.add_route('/v1/database_server/panel/batch_sync', DatabaseServerPanelBatchSyncManageController())
    api.add_route('/v1/database_server/panel/{rid}', DatabaseServerPanelItemManageController())

    api.add_route('/v1/database_server/search', DatabaseServerSearchManageController())
    api.add_route('/v1/database_server/search/batch_sync', DatabaseServerSearchBatchSyncManageController())
    api.add_route('/v1/database_server/search/{rid}', DatabaseServerSearchItemManageController())

    api.add_route('/v1/database_server/tmp_graph', DatabaseServerTmpGraphManageController())
    api.add_route('/v1/database_server/tmp_graph/batch_sync', DatabaseServerTmpGraphBatchSyncManageController())
    api.add_route('/v1/database_server/tmp_graph/{rid}', DatabaseServerTmpGraphItemManageController())

    # graph数据库下的表
    api.add_route('/v1/database_server/counter_text', DatabaseServerCounterTextManageController())
    api.add_route('/v1/database_server/counter_text/batch_sync', DatabaseServerCounterTextBatchSyncManageController())
    api.add_route('/v1/database_server/counter_text/{rid}', DatabaseServerCounterTextItemManageController())

    api.add_route('/v1/database_server/endpoint', DatabaseServerEndpointManageController())
    api.add_route('/v1/database_server/endpoint/batch_sync', DatabaseServerEndpointBatchSyncManageController())
    api.add_route('/v1/database_server/endpoint/{rid}', DatabaseServerEndpointItemManageController())

    api.add_route('/v1/database_server/endpoint_counter', DatabaseServerEndpointCounterManageController())
    api.add_route('/v1/database_server/endpoint_counter/batch_sync', DatabaseServerEndpointCounterBatchSyncManageController())
    api.add_route('/v1/database_server/endpoint_counter/{rid}', DatabaseServerEndpointCounterItemManageController())

    api.add_route('/v1/database_server/tag_endpoint', DatabaseServerTagEndpointManageController())
    api.add_route('/v1/database_server/tag_endpoint/batch_sync', DatabaseServerTagEndpointBatchSyncManageController())
    api.add_route('/v1/database_server/tag_endpoint/{rid}', DatabaseServerTagEndpointItemManageController())

    # uic数据库下的表

    api.add_route('/v1/database_server/session', DatabaseServerSessionManageController())
    api.add_route('/v1/database_server/session/batch_sync', DatabaseServerSessionBatchSyncManageController())
    api.add_route('/v1/database_server/session/{rid}', DatabaseServerSessionItemManageController())

    api.add_route('/v1/database_server/user', DatabaseServerUserManageController())
    api.add_route('/v1/database_server/user/batch_sync', DatabaseServerUserBatchSyncManageController())
    api.add_route('/v1/database_server/user/{rid}', DatabaseServerUserItemManageController())
