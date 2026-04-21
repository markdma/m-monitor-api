# coding: utf-8

from monitor.apps.load_balance.service.service import LoadBalanceService
from monitor.common.controller import CollectionController, ItemController


class LoadBalanceManageController(CollectionController):
    name = 'monitor.load_balance'
    allow_methods = ('GET', 'POST')
    resource = LoadBalanceService()

    # def create(self, req, data, **kwargs):
    #     return super(LoadBalanceManageController, self).create(req, data, **kwargs)


class LoadBalanceItemManageController(ItemController):
    name = 'monitor.load_balance.item'
    allow_methods = ('GET', 'POST', 'PATCH', 'DELETE')
    resource = LoadBalanceService()

    # def delete(self):
    #     pass


'''
class LoadBalanceManageController(CollectionController):
    name = 'monitor.load_balance'
    allow_methods = ('GET',)
    resource = LoadBalanceService

    @tenant_project_func(tenant_field="db_instance.tenant_id", project_field="db_instance.project_id")
    def _build_criteria(self, req, supported_filters=None):
        return super(LoadBalanceManageController, self)._build_criteria(req, supported_filters)

    def on_get(self, req, resp, **kwargs):
        self._validate_method(req)
        criteria = self._build_criteria(req)
        filters = criteria.get("filters")
        # server_ip = filters.get("server_ip")
        # if server_ip and isinstance(server_ip,dict):
        #     ip = server_ip.get('ilike')
        #     if ip and utils.ipv6_validator(ip):
        #         ip = str(IPy.IP(ip))
        #         filters["server_ip"].update({"ilike": ip})
        refs = self.list(req, copy.deepcopy(criteria), **kwargs)
        count = self.count(req, criteria, results=refs, **kwargs)
        resp.json = {'count': count, 'data': refs}


class LoadBalanceItemManageController(ItemController):
    name = 'monitor.load_balance.item'
    allow_methods = ('GET', 'PATCH')
    resource = LoadBalanceService

    @set_operate_user_func()
    def get(self, req, **kwargs):
        return self.make_resource(req).get(**kwargs)

    @set_operate_user_func()
    def update(self, req, data, **kwargs):
        rid = kwargs.pop('rid')
        return self.make_resource(req).update(rid, data, operate_flag=True)
'''
