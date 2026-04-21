#!/usr/bin/python
# -*- coding:utf-8 -*-

from monitor.common.controller import CollectionController
from monitor.apps.host_report.api import ceph_resource_capacity_api, capacity_metric_filter_strategy_api
from monitor.common import time_util, const_define
from monitor.core.exceptions import ValidationError


class CephResourceCapacityBase(object):
    @staticmethod
    def _arg_model_get_used_statistics_data():
        base_define = {
            10: "0-10",
            50: "10-50",
            90: "50-90",
            100: "90-100"
        }
        return base_define

    @staticmethod
    def get_statistic_data_by_value(metric_threshold_dict, metric_value_list):
        metric_statistic_dict = {k: 0 for k in metric_threshold_dict.values()}
        new_metric_threshold_list = sorted(metric_threshold_dict.keys())
        for metric_value in metric_value_list:
            for metric_threshold in new_metric_threshold_list:
                if metric_value <= metric_threshold:
                    metric_statistic_dict[metric_threshold_dict[metric_threshold]] += 1
                    break
        return metric_statistic_dict


class CephResourceCapacityController(CollectionController, CephResourceCapacityBase):
    name = 'monitor.db_stat'
    allow_methods = ('GET',)
    resource = ceph_resource_capacity_api.CephResourceCapacityApi

    special_filter_keys = ('t_if_az.id', 't_if_az.name', 't_if_region.id', 't_if_region.name')

    def on_get(self, req, resp, **kwargs):
        self._validate_method(req)
        criteria = self._build_criteria(req)
        filters = criteria["filters"]
        filters_dict = {}
        if "stat_type" in filters.keys():
            stat_type = filters.pop("stat_type", None)
            ceph_stat_api = ceph_resource_capacity_api.CephResourceCapacityApi()
            if stat_type in const_define.CephCapacityType.ALL_TYPE:
                filters['category'] = stat_type
            else:
                raise ValidationError("param参数 stat_type: %s, 必须在 %s中" % (stat_type, const_define.DiskCapacityType.ALL_TYPE))
        else:
            raise ValidationError("params参数 stat_type: 不能为空")

        if "filter_strategy_id" in filters.keys():
            filter_strategy_id = filters.pop("filter_strategy_id", None)
            if filter_strategy_id is not None:
                filters_dict = capacity_metric_filter_strategy_api.CapacityMetricFilterStrategyApi().get_filter_dict(filter_strategy_id)
            else:
                raise ValidationError("param参数 filter_stragegy_id不能为空")

        fields = criteria.pop('fields', None)
        add_filter = False
        cbs_filters = {}
        count = 0
        for key in filters.keys():
            if key in self.special_filter_keys:
                cbs_filters[key] = filters[key]
                add_filter = True

        if not add_filter:
            criteria["filters"].update(filters_dict)
            refs = ceph_stat_api.list(**criteria)
            count = self.count(req, criteria, results=refs, **kwargs)
        else:
            new_result = []
            size = criteria.pop('limit', 0)
            off_set = criteria.pop('offset', 0)
            criteria["filters"].update(filters_dict)
            refs = ceph_stat_api.list(**criteria)
            for ref in refs:
                if self.check_add_filter(cbs_filters, ref['ceph_info']):
                    off_set = off_set - 1
                    count = count + 1
                    if (size > 0) and (off_set < 0):
                        size = size - 1
                        new_result.append(ref)
            refs = new_result

        if fields is not None:
            refs = [self._simplify_info(ref, fields) for ref in refs]
        resp.json = {'count': count, 'data': refs}

        if fields is not None:
            refs = [self._simplify_info(ref, fields) for ref in refs]
        resp.json = {'count': count, 'data': refs}

    def check_add_filter(self, filters, ceph_info):
        if not isinstance(ceph_info, dict):
            return False
        check_result = True
        for key_string in filters.keys():
            keys = key_string.split('.')
            if not isinstance(ceph_info.get(keys[0], {}), dict):
                check_result = False
                break
            if (len(keys) == 2) and (filters.get(key_string, '') not in ceph_info.get(keys[0], {}).get(keys[1], '')):
                check_result = False
        return check_result


class CephResourceCapacityStatisticsController(CollectionController, CephResourceCapacityBase):
    name = 'monitor_database_statistics'
    allow_methods = ('GET',)
    resource = ceph_resource_capacity_api.CephResourceCapacityApi

    def on_get(self, req, resp, **kwargs):
        self._validate_method(req)
        criteria = self._build_criteria(req)
        filters = criteria["filters"]
        for k, v in filters.items():
            if k not in ["datetime", "ceph_info.region_id", "ceph_info.az_id"]:
                filters.pop(k, None)
        ceph_stat_api = self.resource()
        data_time = filters.get("datetime")
        if data_time and time_util.is_data_str(data_time):
            day_str = data_time
        else:
            day_str = time_util.get_yesterday_str()
        filters.update({"datetime": day_str})
        ceph_resource_data = ceph_stat_api.list(filters=filters)
        if "ceph_info.region_id" in filters.keys():
            region_id = filters.get("ceph_info.region_id", "")
            ceph_resource_data = capacity_metric_filter_strategy_api.CapacityMetricFilterStrategyApi().filter_list_data(
                ceph_resource_data, "ceph_info.region_id", region_id)
        if "ceph_info.az_id" in filters.keys():
            az_id = filters.get("ceph_info.az_id", "")
            ceph_resource_data = capacity_metric_filter_strategy_api.CapacityMetricFilterStrategyApi().filter_list_data(
                ceph_resource_data, "ceph_info.az_id", az_id)
        used_percent_allocation_list = []
        for i in ceph_resource_data:
            used_percent_allocation_list.append(i['usage_used_percent_p95'])
        metric_name_resp_list = []
        used_percent_statistic_dict = self.get_statistic_data_by_value(self._arg_model_get_used_statistics_data(),
                                                                       used_percent_allocation_list)
        metric_name_resp_list.append({"usage_used_percent_p95": used_percent_statistic_dict})
        resp.json = {"count": len(metric_name_resp_list), "data": metric_name_resp_list}
