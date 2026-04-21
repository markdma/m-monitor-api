from monitor.apps.ceph_cluster.db_resource import resource


class CephClusterApi(resource.CephClusterResource):
    pass


class CephClusterHostApi(resource.CephClusterHostResource):
    pass


class CephClusterRgwApi(resource.CephClusterRgwResource):
    pass
