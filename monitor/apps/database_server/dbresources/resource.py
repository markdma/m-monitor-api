# coding: utf-8
from __future__ import absolute_import

import datetime

from monitor.db import models, pool
from monitor.db.crud import ResourceBase


class HostReportResource(ResourceBase):
    orm_meta = models.HostReport
    _default_order = ['-created_date']
    _primary_keys = 'id'

    def _before_create(self, resource, validate):
        resource["created_date"] = datetime.datetime.now()


class AvailableZoneResource(ResourceBase):
    orm_meta = models.AvailableZone
    _default_order = ['-created_date']
    _primary_keys = 'id'

    def get_id_by_name(self, availablezone_names):
        with self.get_session() as session:
            query = session.query(models.AvailableZone.id).filter(models.AvailableZone.name.in_(availablezone_names))
            result = self._apply_filters(query, models.AvailableZone).all()
            return [item[0] for item in result]


class RegionResource(ResourceBase):
    orm_meta = models.Region
    _default_order = ['-create_time']
    _primary_keys = 'id'

    def _before_create(self, resource, validate):
        is_using = resource.get("is_using", None)
        resource["create_time"] = datetime.datetime.now()
        if is_using is None:
            resource["is_using"] = 0

    def _before_update(self, rid, resource, validate):
        resource["update_time"] = datetime.datetime.now()


class CapacityMetricResource(ResourceBase):
    orm_meta = models.CapacityMetric
    _default_order = ['-create_time']
    _primary_keys = 'f_id'


class CapacityMetricFilterStrategyResource(ResourceBase):
    orm_meta = models.CapacityMetricFilterStrategy
    _default_order = ['-f_create_time']
    _primary_keys = 'f_id'


class HostResourceCapacityResource(ResourceBase):
    orm_meta = models.HostResourceCapacity
    _default_order = ['-f_date_time']
    _primary_keys = 'f_id'


class HostResourceCapacityWeekResource(ResourceBase):
    orm_meta = models.HostResourceCapacityWeek
    _default_order = ['-f_date_time']
    _primary_keys = 'f_id'


class HostResourceCapacityMonthResource(ResourceBase):
    orm_meta = models.HostResourceCapacityMonth
    _default_order = ['-f_date_time']
    _primary_keys = 'f_id'


class NetLineResourceCapacityResource(ResourceBase):
    orm_meta = models.NetLineResourceCapacity
    _default_order = ['-f_date_time', '-f_name']
    _primary_keys = 'f_id'


class NetLineResourceCapacityWeekResource(ResourceBase):
    orm_meta = models.NetLineResourceCapacityWeek
    _default_order = ['-f_date_time', '-f_name']
    _primary_keys = 'f_id'


class HostResource(ResourceBase):
    '''
    DEPRECATED:
    此类已淘汰 应怎么加注释?要这样: 在类名上面加注释, 说明此类已经被淘汰, 不再使用 怎么加?要加
    '''
    orm_meta = models.Host
    _default_order = ['-id']
    _primary_keys = 'id'

    def _before_create(self, resource, validate):
        pass
        # resource["create_at"] = datetime.datetime.now()
        # resource["update_user"] = None

    def _before_update(self, rid, resource, validate):
        resource["update_at"] = datetime.datetime.now()


class ProjectResource(ResourceBase):
    orm_meta = models.Project
    _default_order = ['-name']
    _primary_keys = 'id'
    _soft_del_flag = {'is_deleted': 1}
    _soft_delete = True


class TenantResource(ResourceBase):
    orm_meta = models.Tenant
    _default_order = ['-name']
    _primary_keys = 'uuid'


class CMDBDBManageResource(ResourceBase):
    orm_meta = models.CMDBDBManage
    _default_order = ['-ctime']
    _primary_keys = 'uuid'

    def _before_create(self, resource, validate):
        resource["ctime"] = datetime.datetime.now()

    def _before_update(self, rid, resource, validate):
        resource["mtime"] = datetime.datetime.now()


class EnvironmentManageResource(ResourceBase):
    orm_meta = models.EnvironmentManage
    _default_order = ['-ctime']
    _primary_keys = 'id'

    def _before_create(self, resource, validate):
        resource["ctime"] = datetime.datetime.now()

    def _before_update(self, rid, resource, validate):
        resource["mtime"] = datetime.datetime.now()


class NetworkSpecialLineResource(ResourceBase):
    orm_meta = models.IFWanManage
    _default_order = ['-name']
    _primary_keys = 'id'

    def _before_update(self, rid, resource, validate):
        resource["uptime"] = datetime.datetime.now()


class NetworkDeviceResource(ResourceBase):
    orm_meta = models.SWIprangeManage
    _default_order = ['-name']
    _primary_keys = 'serial_num'

    def _before_update(self, rid, resource, validate):
        resource["uptime"] = datetime.datetime.now()


class HardwareModelOidsResource(ResourceBase):
    orm_meta = models.SWOidsManage
    _default_order = ['-model']
    _primary_keys = 'id'
    _soft_del_flag = {'is_deleted': 1, 'uptime': datetime.datetime.now()}
    _soft_delete = True

    def _before_create(self, resource, validate):
        resource["uptime"] = datetime.datetime.now()

    def _before_update(self, rid, resource, validate):
        resource["uptime"] = datetime.datetime.now()


class HardwareModelResource(ResourceBase):
    orm_meta = models.HardwareModelManage
    _default_order = ['-create_time']
    _primary_keys = 'id'

    def _before_update(self, rid, resource, validate):
        resource["update_time"] = datetime.datetime.now()


class NetPodsManageResource(ResourceBase):
    orm_meta = models.NetPodsManage
    _default_order = ['-name']
    _primary_keys = 'uuid'

    def _before_update(self, rid, resource, validate):
        resource["update_at"] = datetime.datetime.now()


class NetSubsManageResource(ResourceBase):
    orm_meta = models.NetSubsManage
    _default_order = ['-name']
    _primary_keys = 'uuid'

    def _before_update(self, rid, resource, validate):
        resource["update_at"] = datetime.datetime.now()


class NetworkRelsManageResource(ResourceBase):
    orm_meta = models.NetworkRelsManage
    _default_order = ['-src_device']
    _primary_keys = 'uuid'

    def _before_update(self, rid, resource, validate):
        resource["update_at"] = datetime.datetime.now()


class ModuleManageResource(ResourceBase):
    orm_meta = models.ModuleManage
    _default_order = ['-ctime']
    _primary_keys = 'id'

    def _before_create(self, resource, validate):
        resource["ctime"] = datetime.datetime.now()

    def _before_update(self, rid, resource, validate):
        resource["mtime"] = datetime.datetime.now()


class HostManageResource(ResourceBase):
    orm_meta = models.HostManage
    _default_order = ['-update_at']
    _primary_keys = 'uuid'

    def _before_create(self, resource, validate):
        resource["create_time"] = datetime.datetime.now()


class CMDBDBInstanceManageResource(ResourceBase):
    orm_meta = models.CMDBDBInstanceManage
    _default_order = ['-ctime']
    _primary_keys = 'id'

    def _before_create(self, resource, validate):
        resource["ctime"] = datetime.datetime.now()

    def _before_update(self, rid, resource, validate):
        resource["mtime"] = datetime.datetime.now()


class ActionManageResource(ResourceBase):
    orm_meta = models.ActionManage
    _default_order = ['-id']
    _primary_keys = 'id'


class ActionUserManageResource(ResourceBase):
    orm_meta = models.ActionUserManage
    _default_order = ['-id']
    _primary_keys = 'id'


class AlarmOtherManageResource(ResourceBase):
    orm_meta = models.AlarmOtherManage
    _default_order = ['-id']
    _primary_keys = 'id'


class AlarmScheManageResource(ResourceBase):
    orm_meta = models.AlarmScheManage
    _default_order = ['-id']
    _primary_keys = 'id'


class AlarmTextCfgManageResource(ResourceBase):
    orm_meta = models.AlarmTextCfgManage
    _default_order = ['-title']
    _primary_keys = 'metric'


class AlarmTypeManageResource(ResourceBase):
    orm_meta = models.AlarmTypeManage
    _default_order = ['-id']
    _primary_keys = 'id'


class BigDataAlertManageResource(ResourceBase):
    orm_meta = models.BigDataAlertManage
    _default_order = ['-id']
    _primary_keys = 'id'

    def _before_update(self, rid, resource, validate):
        resource['update_time'] = datetime.datetime.now()


class CheckIPManageResource(ResourceBase):
    orm_meta = models.CheckIPManage
    _default_order = ['-id']
    _primary_keys = 'id'


class CheckIPPortManageResource(ResourceBase):
    orm_meta = models.CheckIPPortManage
    _default_order = ['-id']
    _primary_keys = 'id'


class CheckPointManageResource(ResourceBase):
    orm_meta = models.CheckPointManage
    _default_order = ['-hostname']
    _primary_keys = 'hostname'


class ClusterManageResource(ResourceBase):
    orm_meta = models.ClusterManage
    _default_order = ['-id']
    _primary_keys = 'id'

    def _before_update(self, rid, resource, validate):
        resource['last_update'] = datetime.datetime.now()


class CmdbSYSManageResource(ResourceBase):
    orm_meta = models.CmdbSYSManage
    _default_order = ['-uuid']
    _primary_keys = 'uuid'


class CmdbSYSSecManageResource(ResourceBase):
    orm_meta = models.CmdbSYSSecManage
    _default_order = ['-uuid']
    _primary_keys = 'uuid'


class ConfigKVManageResource(ResourceBase):
    orm_meta = models.ConfigKVManage
    _default_order = ['-c_key']
    _primary_keys = 'c_key'


class CounterManageResource(ResourceBase):
    orm_meta = models.CounterManage
    _default_order = ['-id']
    _primary_keys = 'id'


class CustomAlertManageResource(ResourceBase):
    orm_meta = models.CustomAlertManage
    _default_order = ['-id']
    _primary_keys = 'id'

    def _before_update(self, rid, resource, validate):
        resource['update_time'] = datetime.datetime.now()


class CustomCounterManageResource(ResourceBase):
    orm_meta = models.CustomCounterManage
    _default_order = ['-id']
    _primary_keys = 'id'

    def _before_update(self, rid, resource, validate):
        resource['t_modify'] = datetime.datetime.now()


class ExpressionManageResource(ResourceBase):
    orm_meta = models.ExpressionManage
    _default_order = ['-id']
    _primary_keys = 'id'


class GRPManageResource(ResourceBase):
    orm_meta = models.GRPManage
    _default_order = ['-id']
    _primary_keys = 'id'

    def _before_create(self, resource, validate):
        resource['t_modify'] = datetime.datetime.now()


class GRPHostManageResource(ResourceBase):
    orm_meta = models.GRPHostManage
    _default_order = ['-id']
    _primary_keys = 'id'


class GRPHostnameManageResource(ResourceBase):
    orm_meta = models.GRPHostnameManage
    _default_order = ['-id']
    _primary_keys = 'id'


class GRPTplManageResource(ResourceBase):
    orm_meta = models.GRPTplManage
    _default_order = ['-id']
    _primary_keys = 'id'


class HolidayManageResource(ResourceBase):
    orm_meta = models.HolidayManage
    _default_order = ['-id']
    _primary_keys = 'id'


class HostMaintainingManageResource(ResourceBase):
    orm_meta = models.HostMaintainingManage
    _default_order = ['-id']
    _primary_keys = 'id'
    _soft_del_flag = {'is_deleted': 1, 'deleted_time': datetime.datetime.now()}
    _soft_delete = True


class HostTplManageResource(ResourceBase):
    orm_meta = models.HostTplManage
    _default_order = ['-id']
    _primary_keys = 'id'

    def _before_create(self, resource, validate):
        resource['create_at'] = datetime.datetime.now()


class LastPluginVManageResource(ResourceBase):
    orm_meta = models.LastPluginVManage
    _default_order = ['-id']
    _primary_keys = 'id'


class MaintainCounterManageResource(ResourceBase):
    orm_meta = models.MaintainCounterManage
    _default_order = ['-id']
    _primary_keys = 'id'


class NetPodsConfigManageResource(ResourceBase):
    orm_meta = models.NetPodsConfigManage
    _default_order = ['-id']
    _primary_keys = 'id'

    def _before_update(self, rid, resource, validate):
        resource['update_at'] = datetime.datetime.now()


class NetlineYSConfigManageResource(ResourceBase):
    orm_meta = models.NetlineYSConfigManage
    _default_order = ['-id']
    _primary_keys = 'id'


class PluginDirManageResource(ResourceBase):
    orm_meta = models.PluginDirManage
    _default_order = ['-id']
    _primary_keys = 'id'

    def _before_create(self, resource, validate):
        resource['create_at'] = datetime.datetime.now()


class StorageAlertManageResource(ResourceBase):
    orm_meta = models.StorageAlertManage
    _default_order = ['-id']
    _primary_keys = 'id'

    def _before_update(self, rid, resource, validate):
        resource['update_time'] = datetime.datetime.now()


class StorageCMDBManageResource(ResourceBase):
    orm_meta = models.StorageCMDBManage
    _default_order = ['-id']
    _primary_keys = 'id'

    def _before_update(self, rid, resource, validate):
        resource['t_modify'] = datetime.datetime.now()


class StorageStrategyManageResource(ResourceBase):
    orm_meta = models.StorageStrategyManage
    _default_order = ['-id']
    _primary_keys = 'id'

    def _before_update(self, rid, resource, validate):
        resource['t_modify'] = datetime.datetime.now()


class StrategyManageResource(ResourceBase):
    orm_meta = models.StrategyManage
    _default_order = ['-id']
    _primary_keys = 'id'


class StrategyCallbackManageResource(ResourceBase):
    orm_meta = models.StrategyCallbackManage
    _default_order = ['-strategy_id']
    _primary_keys = 'strategy_id'

    def _before_update(self, rid, resource, validate):
        resource['update_at'] = datetime.datetime.now()


class TPLManageResource(ResourceBase):
    orm_meta = models.TPLManage
    _default_order = ['-create_at']
    _primary_keys = 'id'

    def _before_create(self, resource, validate):
        resource['create_at'] = datetime.datetime.now()


class UnitManageResource(ResourceBase):
    orm_meta = models.UnitManage
    _default_order = ['-id']
    _primary_keys = 'id'


class UpgrateAgentVersionManageResource(ResourceBase):
    orm_meta = models.UpgrateAgentVersionManage
    _default_order = ['-id']
    _primary_keys = 'id'


class UrlMonitorManageResource(ResourceBase):
    orm_meta = models.UrlMonitorManage
    _default_order = ['-url']
    _primary_keys = 'url'


class UserHostManageResource(ResourceBase):
    orm_meta = models.UserHostManage
    _default_order = ['-id']
    _primary_keys = 'id'


class SystemGroupManageResource(ResourceBase):
    orm_meta = models.SystemGroupManage
    _default_order = ['-create_time']
    _primary_keys = 'id'

    def _before_create(self, resource, validate):
        resource['create_time'] = datetime.datetime.now()

    def _before_update(self, rid, resource, validate):
        resource['update_time'] = datetime.datetime.now()


class SystemManageResource(ResourceBase):
    orm_meta = models.SystemManage
    _default_order = ['-create_time']
    _primary_keys = 'id'

    def _before_create(self, resource, validate):
        resource['create_time'] = datetime.datetime.now()

    def _before_update(self, rid, resource, validate):
        resource['update_time'] = datetime.datetime.now()


class SubSystemManageResource(ResourceBase):
    orm_meta = models.SubSystemManage
    _default_order = ['-create_time']
    _primary_keys = 'id'

    def _before_create(self, resource, validate):
        resource['create_time'] = datetime.datetime.now()

    def _before_update(self, rid, resource, validate):
        resource['update_time'] = datetime.datetime.now()


class PublishUnitManageResource(ResourceBase):
    orm_meta = models.PublishUnitManage
    _default_order = ['-create_time']
    _primary_keys = 'id'

    def _before_create(self, resource, validate):
        resource['create_time'] = datetime.datetime.now()

    def _before_update(self, rid, resource, validate):
        resource['update_time'] = datetime.datetime.now()


class UnitInstanceManageResource(ResourceBase):
    orm_meta = models.UnitInstanceManage
    _default_order = ['-create_time']
    _primary_keys = 'id'

    def _before_create(self, resource, validate):
        resource['create_time'] = datetime.datetime.now()

    def _before_update(self, rid, resource, validate):
        resource['update_time'] = datetime.datetime.now()


class IamPolicyManageResource(ResourceBase):
    orm_meta = models.IamPolicyManage
    _default_order = ['-create_time']
    _primary_keys = 'id'

    def _before_create(self, resource, validate):
        resource['create_time'] = datetime.datetime.now()

    def _before_update(self, rid, resource, validate):
        resource['update_time'] = datetime.datetime.now()


class SessionManageResource(ResourceBase):
    orm_meta = models.SessionManage
    orm_pool = pool.POOLS.uic
    _default_order = ['-id']
    _primary_keys = 'id'


class UserManageResource(ResourceBase):
    orm_meta = models.UserManage
    orm_pool = pool.POOLS.uic
    _default_order = ['-id']
    _primary_keys = 'id'

    def _before_create(self, resource, validate):
        resource['created'] = datetime.datetime.now()


class EventCasesManageResource(ResourceBase):
    orm_meta = models.EventCasesManage
    orm_pool = pool.POOLS.alarms
    _default_order = ['-id']
    _primary_keys = 'id'

    def _before_update(self, rid, resource, validate):
        resource['update_at'] = datetime.datetime.now()


class AlarmStatusManageResource(ResourceBase):
    orm_meta = models.AlarmStatusManage
    orm_pool = pool.POOLS.alarms
    _default_order = ['-id']
    _primary_keys = 'id'

    def _before_update(self, rid, resource, validate):
        resource['update_at'] = datetime.datetime.now()


class DelLogManageManageResource(ResourceBase):
    orm_meta = models.DelLogManage
    orm_pool = pool.POOLS.alarms
    _default_order = ['-id']
    _primary_keys = 'id'


class EventReportManageResource(ResourceBase):
    orm_meta = models.EventReportManage
    orm_pool = pool.POOLS.alarms
    _default_order = ['-id']
    _primary_keys = 'id'

    def _before_update(self, rid, resource, validate):
        resource['update_at'] = datetime.datetime.now()


class EventsManageResource(ResourceBase):
    orm_meta = models.EventsManage
    orm_pool = pool.POOLS.alarms
    _default_order = ['-id']
    _primary_keys = 'id'


class RemarkCommonManageResource(ResourceBase):
    orm_meta = models.RemarkCommonManage
    orm_pool = pool.POOLS.alarms
    _default_order = ['-id']
    _primary_keys = 'id'

    def _before_update(self, rid, resource, validate):
        resource['update_at'] = datetime.datetime.now()


class ButtonManageResource(ResourceBase):
    orm_meta = models.ButtonManage
    orm_pool = pool.POOLS.dashboard
    _default_order = ['-id']
    _primary_keys = 'id'


class ChartManageResource(ResourceBase):
    orm_meta = models.ChartManage
    orm_pool = pool.POOLS.dashboard
    _default_order = ['-id']
    _primary_keys = 'id'


class CustomDashBoardManageResource(ResourceBase):
    orm_meta = models.CustomDashBoardManage
    orm_pool = pool.POOLS.dashboard
    _default_order = ['-id']
    _primary_keys = 'id'

    def _before_update(self, rid, resource, validate):
        resource['update_at'] = datetime.datetime.now()


class DashBoardManageResource(ResourceBase):
    orm_meta = models.DashBoardManage
    orm_pool = pool.POOLS.dashboard
    _default_order = ['-id']
    _primary_keys = 'id'


class DashBoardGraphManageResource(ResourceBase):
    orm_meta = models.DashBoardGraphManage
    orm_pool = pool.POOLS.dashboard
    _default_order = ['-id']
    _primary_keys = 'id'


class DashBoardScreenManageResource(ResourceBase):
    orm_meta = models.DashBoardScreenManage
    orm_pool = pool.POOLS.dashboard
    _default_order = ['-id']
    _primary_keys = 'id'


class HostScreenCFGManageResource(ResourceBase):
    orm_meta = models.HostScreenCFGManage
    orm_pool = pool.POOLS.dashboard
    _default_order = ['-id']
    _primary_keys = 'id'


class MessageManageResource(ResourceBase):
    orm_meta = models.MessageManage
    orm_pool = pool.POOLS.dashboard
    _default_order = ['-id']
    _primary_keys = 'id'


class OptionManageResource(ResourceBase):
    orm_meta = models.OptionManage
    orm_pool = pool.POOLS.dashboard
    _default_order = ['-id']
    _primary_keys = 'id'


class PanelManageResource(ResourceBase):
    orm_meta = models.PanelManage
    orm_pool = pool.POOLS.dashboard
    _default_order = ['-id']
    _primary_keys = 'id'


class SearchManageResource(ResourceBase):
    orm_meta = models.SearchManage
    orm_pool = pool.POOLS.dashboard
    _default_order = ['-id']
    _primary_keys = 'id'


class TmpGraphManageResource(ResourceBase):
    orm_meta = models.TmpGraphManage
    orm_pool = pool.POOLS.dashboard
    _default_order = ['-id']
    _primary_keys = 'id'


class CounterTextManageResource(ResourceBase):
    orm_meta = models.CounterTextManage
    orm_pool = pool.POOLS.graph
    _default_order = ['-counter']
    _primary_keys = 'counter'


class EndpointManageResource(ResourceBase):
    orm_meta = models.EndpointManage
    orm_pool = pool.POOLS.graph
    _default_order = ['-id']
    _primary_keys = 'id'

    def _before_create(self, resource, validate):
        resource['t_create'] = datetime.datetime.now()

    def _before_update(self, rid, resource, validate):
        resource['t_modify'] = datetime.datetime.now()


class EndpointCounterManageResource(ResourceBase):
    orm_meta = models.EndpointCounterManage
    orm_pool = pool.POOLS.graph
    _default_order = ['-id']
    _primary_keys = 'id'

    def _before_create(self, resource, validate):
        resource['t_create'] = datetime.datetime.now()

    def _before_update(self, rid, resource, validate):
        resource['t_modify'] = datetime.datetime.now()


class TagEndpointManageResource(ResourceBase):
    orm_meta = models.TagEndpointManage
    orm_pool = pool.POOLS.graph
    _default_order = ['-id']
    _primary_keys = 'id'

    def _before_create(self, resource, validate):
        resource['t_create'] = datetime.datetime.now()

    def _before_update(self, rid, resource, validate):
        resource['t_modify'] = datetime.datetime.now()
