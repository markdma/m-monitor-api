# coding=utf-8
from monitor.apps.ceph_cluster.ceph_cluster_controller import CephClusterHostsAlarmStatus, CephClusterHostMetric, \
    CephClusterView


def add_routes(api):
    # 集群主机告警状态
    api.add_route('/v1/monitor/ceph_cluster/hosts_alarms_status', CephClusterHostsAlarmStatus())
    # 单个ceph主机指标数据
    api.add_route('/v1/monitor/ceph_cluster/host/{rid}', CephClusterHostMetric())
    # 集群视图
    api.add_route('/v1/monitor/ceph_cluster/view/{rid}', CephClusterView())
    # osd视图
