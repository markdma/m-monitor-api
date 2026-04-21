# coding: utf-8
from __future__ import absolute_import

from monitor.apps.host_report.dbresources import resource
from monitor.core.exceptions import ValidationError, NotFoundError
from monitor.apps.host_report.dbresources.resource import CapacityMetricFilterStrategyResource, \
    CapacityMetricResource
import logging
import json


class CapacityMetricFilterStrategyApi(resource.CapacityMetricFilterStrategyResource):

    @staticmethod
    def _get_symbol_mapping():
        base_define = {
            "<=": "lte",
            "<": "lt",
            ">": "gt",
            ">=": "gte",
            "=": "eq",
            "!=": "ne"
        }
        return base_define

    @property
    def default_filter(self):
        return {'f_enabled': 1}

    def get_filter_dict(self, filter_strategy_id):
        logging.debug("get_filter_dict, filter_strategy_id: %s\r\n", filter_strategy_id)
        filters_dict = {}
        filter_strategy_id = str(filter_strategy_id).strip()
        filter_strategy_info = CapacityMetricFilterStrategyResource().get(filter_strategy_id)
        logging.debug("get_filter_dict filter_strategy_info:%s \r\n", filter_strategy_info)
        if not filter_strategy_info:
            raise NotFoundError("params参数 filter_strategy_id: %s, 不存在" % filter_strategy_id)
        else:
            metric_ids = filter_strategy_info["f_metric_id"]
            math_operator = filter_strategy_info["f_math_operator"]
            threshold_value = filter_strategy_info["f_threshold_value"]

            if not metric_ids or not math_operator or not threshold_value:
                raise ValidationError("params参数 filter_strategy_id 数据异常")

            metric_ids_list = str(metric_ids).split(":")
            metric_ids_list = [i.strip() for i in metric_ids_list]
            metrics = CapacityMetricResource().list(filters={"f_id": metric_ids_list})
            metrics_dict = {str(info["f_id"]): str(info["f_store_metric_name"]) for info in metrics}
            metric_list_new = []
            for info in metric_ids_list:
                if info in metrics_dict.keys():
                    metric_list_new.append(metrics_dict[info])
                else:
                    raise ValidationError("params参数 filter_strategy_id 的f_metric_id字段数据异常")

            math_operator_list = str(math_operator).split(":")
            math_operator_list_new = [i.strip() for i in math_operator_list]

            threshold_value_list = str(threshold_value).split(":")
            threshold_value_list_new = [i.strip() for i in threshold_value_list]

            if len(metric_list_new) == len(math_operator_list_new) == len(threshold_value_list_new):
                for i in range(len(metric_list_new)):
                    filters_symbol = {
                        self._get_symbol_mapping().get(math_operator_list_new[i]): threshold_value_list_new[i]}
                    filters_str = metric_list_new[i]
                    if filters_dict.has_key(filters_str):
                        if isinstance(filters_dict[filters_str], dict):
                            filters_dict[filters_str].update(filters_symbol)
                    else:
                        filters_dict[filters_str] = filters_symbol

            else:
                raise ValidationError("params参数 filter_strategy_id 数据异常")
            logging.debug("get_filter_dict filters_dict: %s \r\n", json.dumps(filters_dict))
            return filters_dict

    @staticmethod
    def filter_list_data(list_data, key_string, value):
        new_list = []
        for d in list_data:
            compare_data = d
            keys = key_string.split(".")
            keys_count = len(keys)
            for i in range(keys_count):
                if isinstance(compare_data, dict):
                    compare_data = compare_data[keys[i]]
                    if i == keys_count - 1 and compare_data == value:
                        new_list.append(d)
        return new_list


class CapacityMetricApi(resource.CapacityMetricResource):

    pass

