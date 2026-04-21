# coding: utf-8
from __future__ import absolute_import

from monitor.apps.network_manage.hardware_model_controller import HardwareModelManageController, \
    HardwareModelItemManageController, HardwareModelBatchSyncController
from monitor.apps.network_manage.network_manage_controller import NetworkSpecialLineItemController, \
    NetworkSpecialLineController, NetworkDeviceController, NetworkDeviceItemController, HardwareModelOidsItemController, \
    HardwareModelOidsController, NetPodsManageController, NetPodsBatchSyncController, NetSubsManageController, \
    NetSubsBatchSyncController, NetworkRelsManageController, NetworkRelsBatchSyncController


def add_routes(api):
    # 网络专线
    api.add_route('/v1/monitor/network_special_line', NetworkSpecialLineController())
    api.add_route('/v1/monitor/network_special_line/{rid}', NetworkSpecialLineItemController())

    # 网络设备
    api.add_route('/v1/monitor/network_device', NetworkDeviceController())
    api.add_route('/v1/monitor/network_device/{rid}', NetworkDeviceItemController())

    # 网络设备oid
    api.add_route('/v1/monitor/hardware_model/oid', HardwareModelOidsController())
    api.add_route('/v1/monitor/hardware_model/oid/{rid}', HardwareModelOidsItemController())

    # 硬件设备
    api.add_route('/v1/monitor/hardware_model', HardwareModelManageController())
    api.add_route('/v1/monitor/hardware_model/{rid}', HardwareModelItemManageController())
    api.add_route('/v1/monitor/hardware_model/batch_sync', HardwareModelBatchSyncController())

    # net_pod
    api.add_route('/v1/monitor/net_pods', NetPodsManageController())
    api.add_route('/v1/monitor/net_pods/batch_sync', NetPodsBatchSyncController())

    # net_subs
    api.add_route('/v1/monitor/net_subs', NetSubsManageController())
    api.add_route('/v1/monitor/net_subs/batch_sync', NetSubsBatchSyncController())

    # network_rels
    api.add_route('/v1/monitor/network_rels', NetworkRelsManageController())
    api.add_route('/v1/monitor/network_rels/batch_sync', NetworkRelsBatchSyncController())
