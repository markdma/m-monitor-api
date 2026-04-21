# encoding=utf-8
import copy

from monitor.apps.database_server.dbresources.resource import HostResource
from monitor.apps.host_manage.dbresources.resource import SearchEndPointResource
from monitor.apps.load_balance.db_repo.repo import LoadBalanceRepo


class LoadBalanceService(LoadBalanceRepo):
    __name__ = "负载均衡"
    hostRepo = HostResource()  # models.Host()
    searchEndPointRepo = SearchEndPointResource()  # models.SearchEndPoint()

    def _before_create(self, resource, validate):
        super(LoadBalanceService, self)._before_create(resource, validate)
        if not resource['host_uuid']:
            raise ValueError('host_uuid is required')
        resource['id'] = "%s-%s" % (resource['host_uuid'].lower(), resource['lb_type'])

    def _before_update(self, rid, resource, validate):
        super(LoadBalanceService, self)._before_update(rid, resource, validate)
        if not resource['host_uuid']:
            raise ValueError('host_uuid is required')

    def _before_delete(self, rid, filters):
        super(LoadBalanceService, self)._before_delete(rid, filters)
        if not rid:
            raise ValueError('rid is required')
        # .lower()
        rid = rid.lower()

    def create(self, resource, validate=True, detail=True, operate_flag=False):
        # host_uuid 已校验
        item = super(LoadBalanceService, self).create(resource, validate, detail, operate_flag)
        host_list = self.hostRepo.list(filters={"hostname": resource['host_uuid'], "type": "linux"})
        if not host_list:
            raise Exception("对应主机不存在:%s", resource['host_uuid'])
        host_list_0 = copy.copy(host_list[0])
        # // id <- '', hostname <- item.get('host_uuid'), type <- item.get('lb_type')
        host_list_0.update({'id': None, 'hostname': item.get('id'), 'type': item.get('lb_type')})
        try:
            self.hostRepo.create(host_list_0)
        except Exception as e:
            super(LoadBalanceService, self).delete(item.get('id'))
            raise e
        # // todo 加事务
        return item

    def delete(self, rid, filters=None, operate_flag=False, delete_user=None):
        c = super(LoadBalanceService, self).delete(rid, filters, operate_flag, delete_user)
        self.hostRepo.delete_all({'hostname': rid})
        return c or 1
