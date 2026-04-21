# coding: utf-8

from monitor.apps.host_report.api import netline_resource_capacity_api
from monitor.common import const_define
from monitor.common.controller import CollectionController
from monitor.core.exceptions import ValidationError


class HostResourceCapacityWeekController(CollectionController):
    name = 'monitor.netline_stat'
    allow_methods = ('GET',)
    resource = netline_resource_capacity_api.NetLineResourceCapacityApi

    def on_get(self, req, resp, **kwargs):
        self._validate_method(req)
        criteria = self._build_criteria(req)
        filters = criteria["filters"]
        orders = criteria["orders"]
        count_limit = None
        if "stat_type" in filters.keys():
            stat_type = filters.pop("stat_type", None)
            if stat_type == const_define.NetlineCapacityType.DayTable:
                netline_stat_api = netline_resource_capacity_api.NetLineResourceCapacityApi()
            elif stat_type == const_define.NetlineCapacityType.WeekTable:
                netline_stat_api = netline_resource_capacity_api.NetLineResourceCapacityWeekApi()
            else:
                raise ValidationError("params参数 stat_type: %s, 必须在%s 中" % (stat_type, const_define.NetlineCapacityType.ALL_TYPE))
        else:
            raise ValidationError("params参数 stat_type: 不能为空")
        if "filter_strategy_id" in filters.keys():
            filter_strategy_id = filters.pop("filter_strategy_id", None)
            if filter_strategy_id == const_define.NetlineCapacityFilterStrategyType.NetInOctetTop20:
                count_limit = 20
                orders_new = ["-f_net_in_octets"]
                if orders and isinstance(orders, list):
                    orders_new.extend(orders)
                    criteria["orders"] = orders_new
                else:
                    criteria["orders"] = orders_new

            if filter_strategy_id == const_define.NetlineCapacityFilterStrategyType.NetOutOctetTop20:
                count_limit = 20
                orders_new = ["-f_net_out_octets"]
                if orders and isinstance(orders, list):
                    orders_new.extend(orders)
                    criteria["orders"] = orders_new
                else:
                    criteria["orders"] = orders_new

            if filter_strategy_id == const_define.NetlineCapacityFilterStrategyType.NetInOctetLess20:
                count_limit = 20
                orders_new = ["+f_net_in_octets"]
                if orders and isinstance(orders, list):
                    orders_new.extend(orders)
                    criteria["orders"] = orders_new
                else:
                    criteria["orders"] = orders_new

            if filter_strategy_id == const_define.NetlineCapacityFilterStrategyType.NetOutOctetLess20:
                count_limit = 20
                orders_new = ["+f_net_out_octets"]
                if orders and isinstance(orders, list):
                    orders_new.extend(orders)
                    criteria["orders"] = orders_new
                else:
                    criteria["orders"] = orders_new

        fields = criteria.pop('fields', None)
        if count_limit:
            if not criteria["limit"] or (isinstance(criteria["limit"], int) and criteria["limit"] > count_limit):
                criteria["limit"] = count_limit
        refs = netline_stat_api.list(**criteria)
        if fields is not None:
            refs = [self._simplify_info(ref, fields) for ref in refs]
        count = netline_stat_api.count(filters=filters, limit=count_limit)
        resp.json = {'count': count, 'data': refs}