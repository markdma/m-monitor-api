#!/usr/bin/python
# -*- coding:utf-8 -*-

import json
import logging

from monitor.apps.database_server.api import falcon_portal_api
from monitor.apps.host_report.api import database_resource_capacity_api
from monitor.apps.host_report.api import host_resource_capacity_api, capacity_metric_filter_strategy_api
from monitor.common import time_util, const_define
from monitor.common.controller import CollectionController
from monitor.common.decorators import tenant_project_func
from monitor.core.exceptions import ValidationError


class DatabaseResourceCapacityBase(object):

    @staticmethod
    def _arg_model_get_allocation_statistics_data():
        base_define = {
            10: "0-10",
            50: "10-50",
            90: "50-90",
            100: "90-100"
        }
        return base_define

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

    @staticmethod
    def get_statistic_database_type(db_resource_list):
        statistic_dict = {"oracle": 0, "mysql": 0, "postgresql": 0, "mongo": 0, "redis": 0, "sqlserver": 0}
        statistic_storage_used_dict = {}
        for d in db_resource_list:
            k = d['f_type']
            k = 'other' if not k else k
            if k not in statistic_dict.keys():
                statistic_dict[k] = 0
            statistic_dict[k] = statistic_dict[k] + 1

            storage_used_key = k + '_storage_used'
            if storage_used_key not in statistic_storage_used_dict:
                statistic_storage_used_dict[storage_used_key] = 0.0
            statistic_storage_used_dict[storage_used_key] = statistic_storage_used_dict[storage_used_key] \
                                                            + d['f_storage_used']

        metric_statistic_dict = {}
        for key in statistic_dict.keys():
            value_arr = list([])
            value_arr.append(statistic_dict[key])
            storage_used = statistic_storage_used_dict.get(key + '_storage_used', 0.0)
            value_arr.append(storage_used)
            metric_statistic_dict[key] = value_arr

        return metric_statistic_dict

    @staticmethod
    def get_statistic_storage_type(db_resource_list):
        metric_statistic_dict = {"通用型": 0}
        for d in db_resource_list:
            storage_type = d['f_storage_type']
            if storage_type not in metric_statistic_dict.keys():
                metric_statistic_dict[storage_type] = d['f_storage_total']
                continue
            metric_statistic_dict[storage_type] += d['f_storage_total']
        return metric_statistic_dict


class DatabaseResourceCapacityController(CollectionController, DatabaseResourceCapacityBase):
    name = 'monitor.db_stat'
    allow_methods = ('GET',)
    resource = database_resource_capacity_api.DatabaseResourceCapacityApi

    @tenant_project_func(True, "f_tenant_id", "f_project_id", False)
    def _build_criteria(self, req, supported_filters=None):
        return super(DatabaseResourceCapacityController, self)._build_criteria(req)

    def on_get(self, req, resp, **kwargs):
        self._validate_method(req)
        criteria = self._build_criteria(req)
        filters = criteria["filters"]
        export_flag = filters.pop("export", None)
        filters_dict = {}
        if "stat_type" in filters.keys():
            stat_type = filters.pop("stat_type", None)
            if stat_type == const_define.DatabaseCapacityType.DayTable:
                database_stat_api = database_resource_capacity_api.DatabaseResourceCapacityApi()
                self.host_stat_api = host_resource_capacity_api.HostResourceCapacityApi()
            elif stat_type == const_define.DatabaseCapacityType.WeekTable:
                database_stat_api = database_resource_capacity_api.DatabaseResourceCapacityWeekApi()
                self.host_stat_api = host_resource_capacity_api.HostResourceCapacityWeekApi()
            elif stat_type == const_define.DatabaseCapacityType.MonthTable:
                database_stat_api = database_resource_capacity_api.DatabaseResourceCapacityMonthApi()
                self.host_stat_api = host_resource_capacity_api.HostResourceCapacityMonthApi()
                try:
                    for k in filters['f_date_time']:  # 日期截断 去除日字段
                        filters['f_date_time'][k] = filters['f_date_time'][k][:7]
                except Exception as e:
                    pass
            else:
                raise ValidationError(
                    "param参数 stat_type: %s, 必选在 %s中" % (stat_type, const_define.DatabaseCapacityType.ALL_TYPE))
        else:
            raise ValidationError("params参数 stat_type: 不能为空")

        if "filter_strategy_id" in filters.keys():

            filter_strategy_id = filters.pop("filter_strategy_id", None)
            if filter_strategy_id is not None:
                filters_dict = capacity_metric_filter_strategy_api.CapacityMetricFilterStrategyApi().get_filter_dict(
                    filter_strategy_id)
            else:
                raise ValidationError("params参数 filter_strategy_id 不能为空")

        fields = criteria.pop('fields', None)
        criteria["filters"].update(filters_dict)
        logging.debug("get_filter_dict criteria: %s", json.dumps(criteria))
        refs = database_stat_api.list(**criteria)
        if fields is not None:
            refs = [self._simplify_info(ref, fields) for ref in refs]
        count = database_stat_api.count(filters)
        tmp_dict = {}
        if not export_flag:
            for i in refs:
                f_uuid = i["f_uuid"]
                if f_uuid in tmp_dict:
                    tmp_dict[f_uuid].append(i["f_date_time"])
                else:
                    tmp_dict[f_uuid] = [i["f_date_time"]]
            host_capacity_dict = self._get_host_capacity(tmp_dict)
            for i in refs:
                i["host_capacity"] = host_capacity_dict.get(i["f_uuid"]+i["f_date_time"]) or []
        resp.json = {'count': count, 'data': refs}

    def _get_host_capacity(self, tmp_dict):
        db_uuids = tmp_dict.keys()
        refs = falcon_portal_api.CMDBDBInstanceManageResourceApi().list(filters={"db_uuid": {"in": db_uuids}})
        tmp_host_dict = {}
        for db_instance in refs:
            date_times = tmp_dict.get(db_instance["db_uuid"]) or []
            for date_time in date_times:
                try:
                    host_refs = self.host_stat_api.list(
                        filters={"f_uuid": db_instance["host_uuid"], "f_date_time": date_time})
                    if not host_refs:
                        continue
                    db_uuid_date_time = db_instance["db_uuid"] + date_time
                    if db_uuid_date_time in tmp_host_dict:
                        tmp_host_dict[db_uuid_date_time].append(host_refs[0])
                    else:
                        tmp_host_dict[db_uuid_date_time] = host_refs
                except KeyError:
                    continue
        return tmp_host_dict


class DatabaseResourceCapacityStatisticsController(CollectionController, DatabaseResourceCapacityBase):
    name = 'monitor_database_statistics'
    allow_methods = ('GET',)
    resource = database_resource_capacity_api.DatabaseResourceCapacityApi

    @tenant_project_func(True, "f_tenant_id", "f_project_id", False)
    def _build_criteria(self, req, supported_filters=None):
        return super(DatabaseResourceCapacityStatisticsController, self)._build_criteria(req)

    def on_get(self, req, resp, **kwargs):
        self._validate_method(req)
        criteria = self._build_criteria(req)
        filters = criteria["filters"]
        for k, v in filters.items():
            if k not in ["f_date_time", "f_az_id", "f_region_id", "f_project_id", "f_tenant_id", "tenant.name"]:
                filters.pop(k, None)
        database_stat_api = self.resource()
        data_time = filters.get("f_date_time")
        if data_time and time_util.is_data_str(data_time):
            day_str = data_time
        else:
            day_str = time_util.get_yesterday_str()
        filters.update({"f_date_time": day_str})
        db_resource_data = database_stat_api.list(filters=filters)
        storage_allocation_list = []
        storage_used_percent_list = []
        for i in db_resource_data:
            storage_allocation_list.append(i['f_storage_free_percent_p95'])
            storage_used_percent_list.append(i['f_storage_used_percent_p95'])
        metric_name_resp_list = []
        free_statistic_dict = self.get_statistic_data_by_value(self._arg_model_get_allocation_statistics_data(),
                                                               storage_allocation_list)
        metric_name_resp_list.append({"f_storage_free_percent_p95": free_statistic_dict})
        used_statistic_dict = self.get_statistic_data_by_value(self._arg_model_get_used_statistics_data(),
                                                               storage_used_percent_list)
        metric_name_resp_list.append({"f_storage_used_percent_p95": used_statistic_dict})

        database_type_statistic_dict = self.get_statistic_database_type(db_resource_data)
        metric_name_resp_list.append({"f_type": database_type_statistic_dict})
        storage_type_statistic_dict = self.get_statistic_storage_type(db_resource_data)
        metric_name_resp_list.append({"f_storage_type": storage_type_statistic_dict})
        resp.json = {"count": len(metric_name_resp_list), "data": metric_name_resp_list}
