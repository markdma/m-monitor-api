# coding: utf-8
import copy
import os
import falcon

from monitor.apps.host_report.api import capacity_metric_filter_strategy_api
from monitor.apps.host_report.dbresources.resource import RegionResource, AvailableZoneResource, TenantResource, \
    CapacityMetricResource, ProjectResource, CsapacityStrategyTreeRouteResource
from monitor.common.controller import CollectionController, ItemController
from monitor.common import const_define
from monitor.core.exceptions import ValidationError, NotFoundError, ForbiddenError
from monitor.lib.validation import check_params_with_model
import logging


class CapacityMetricFilterStrategyBase(object):

    @staticmethod
    def _arg_model_create_data():
        base_define = {
            "object_tree_type": {"type": basestring, "notnull": True, "required": True,
                                 "format": {"in": const_define.CapacityTreeType.ALL_TYPE}},
            "region_id": {"type": basestring, "notnull": False, "required": False, "format": {">": 0, "<": 37}},
            "az_id": {"type": basestring, "notnull": False, "required": False, "format": {">": 0, "<": 37}},
            "tenant_id": {"type": basestring, "notnull": False, "required": False, "format": {">": 0, "<": 33}},
            "project_id": {"type": basestring, "notnull": False, "required": False, "format": {">": 0, "<": 33}},
            "name": {"type": basestring, "notnull": True, "required": True, "format": {">": 0, "<": 256}},
            "metric_id": {"type": basestring, "notnull": True, "required": True, "format": {">": 0, "<": 256}},
            "metric_type": {"type": int, "notnull": True, "required": True, "format": {">": 0}},
            "math_operator": {"type": basestring, "notnull": True, "required": True, "format": {">": 0, "<": 256}},
            "threshold_value": {"type": basestring, "notnull": True, "required": True, "format": {">": 0, "<": 256}},
            "creator": {"type": basestring, "notnull": True, "required": True, "format": {">": 0, "<": 65}},
            "tree_route": {"type": basestring, "notnull": True, "required": False, "format": {">": 0, "<": 2048}}
        }
        return base_define

    @staticmethod
    def _arg_model_update_data():
        base_define = {
            "metric_id": {"type": basestring, "notnull": True, "required": False, "format": {">": 0, "<": 256}},
            "math_operator": {"type": basestring, "notnull": True, "required": False, "format": {">": 0, "<": 256}},
            "threshold_value": {"type": basestring, "notnull": True, "required": False, "format": {">": 0, "<": 256}},
            "enable": {"type": int, "notnull": True, "required": False, "format": {"in": [0, 1]}},
            "name": {"type": basestring, "notnull": True, "required": False, "format": {">": 0, "<": 256}}
        }
        return base_define

    @staticmethod
    def _arg_model_mapping():
        base_define = {
            "object_tree_type": "f_object_type",
            "region_id": "f_region_id",
            "az_id": "f_az_id",
            "tenant_id": "f_tenant_id",
            "project_id": "f_project_id",
            "name": "f_name",
            "metric_id": "f_metric_id",
            "metric_type": "f_metric_type",
            "math_operator": "f_math_operator",
            "threshold_value": "f_threshold_value",
            "creator": "f_creator",
            "enable": "f_enabled"
        }
        return base_define

    def replace_args_name(self, mapping_value, replace_dict):
        if isinstance(mapping_value, dict) and isinstance(replace_dict, dict):
            for k, v in mapping_value.items():
                if k in replace_dict:
                    replace_dict[v] = replace_dict.pop(k, None)
        return replace_dict

    def check_region(self, region_id):
        if region_id:
            region_info = RegionResource().get(region_id)
            if not region_info:
                raise ValidationError("该区域id: %s, 不存在" % region_id)

    def check_az(self, az_id):
        if az_id:
            az_info = AvailableZoneResource().get(az_id)
            if not az_info:
                raise ValidationError("该可用区id: %s, 不存在" % az_id)

    def check_tenant(self, tenant_id):
        if tenant_id:
            tenant_info = TenantResource().get(tenant_id)
            if not tenant_info:
                raise ValidationError("该租户id: %s, 不存在" % tenant_id)

    def check_project(self, project_id):
        if project_id:
            project_info = ProjectResource().get(project_id)
            if not project_info:
                raise ValidationError("该项目id: %s, 不存在" % project_id)

    def check_object_tree_type(self, json_data):
        object_tree_type = json_data.get("object_tree_type")
        if object_tree_type == const_define.CapacityTreeType.ProjectTreeType:
            if not json_data.get("tree_route"):
                raise ValidationError("集合路径不能为空")
            json_data.pop("region_id", None)
            json_data.pop("az_id", None)
        elif object_tree_type == const_define.CapacityTreeType.AzTreeType:
            # if region_id:
            #     self.check_region(region_id)
            # if az_id:
            #     self.check_az(az_id)
            json_data.pop("project_id", None)
            json_data.pop("tenant_id", None)
        return json_data

    def check_metric_data(self, data):
        metric_ids = data.get("f_metric_id", None)
        math_operator = data.get("f_math_operator", None)
        threshold_value = data.get("f_threshold_value", None)
        if (metric_ids is None) and (math_operator is None) and (threshold_value is None):
            return data
        if (metric_ids is None) or (math_operator is None) or (threshold_value is None):
            raise ValidationError("metric_id,math_operator,threshold_value 需同时输入,请检查!")
        metric_ids_list = str(metric_ids).split(":")
        metric_ids_list_new = [i.strip() for i in metric_ids_list]
        metrics = CapacityMetricResource().list(filters={"f_id": metric_ids_list_new})
        metrics_existed_list = [str(info["f_id"]) for info in metrics]
        metrics_not_existed_list = list(set(metric_ids_list_new) - set(metrics_existed_list))
        if len(metrics_not_existed_list) > 0:
            raise NotFoundError("metric_id: %s, 不存在" % metrics_not_existed_list)

        math_operator_list = str(math_operator).split(":")
        math_operator_list_new = [i.strip() for i in math_operator_list]

        threshold_value_list = str(threshold_value).split(":")
        threshold_value_list_new = [i.strip() for i in threshold_value_list]

        if len(metric_ids_list_new) == len(math_operator_list_new) == len(threshold_value_list_new):
            if len(metric_ids_list_new) > const_define.CapacityFilterStrategy.MetricExpressionsMaxCount:
                raise ValidationError("表达式条件不能超过%s个" % const_define.CapacityFilterStrategy.MetricExpressionsMaxCount)
            data["f_metric_id"] = ":".join(metric_ids_list)
            data["f_math_operator"] = ":".join(math_operator_list_new)
            data["f_threshold_value"] = ":".join(threshold_value_list_new)
        else:
            raise ValidationError("metric_id,math_operator,threshold_value 数据不匹配,请检查!")
        return data

    @staticmethod
    def get_metric_name_dict():
        metrics = CapacityMetricResource().list()
        metric_name_dict = {str(info["f_id"]): str(info["f_metric_name"]) for info in metrics}
        return metric_name_dict

    @staticmethod
    def get_expression_by_info(filter_strategy_info, metrics_name_dict):
        """
        根据 filter_strategy_info
        :param filter_strategy_info:
        :param metrics_name_dict:
        :return:
        """
        expression_list = []
        metric_ids = filter_strategy_info["f_metric_id"]
        math_operator = filter_strategy_info["f_math_operator"]
        threshold_value = filter_strategy_info["f_threshold_value"]
        metric_ids_list = str(metric_ids).split(":")
        metric_ids_list = [i.strip() for i in metric_ids_list]
        metric_name_list = [metrics_name_dict.get(metric_id, "指标值") for metric_id in metric_ids_list]
        math_operator_list = [i.strip() for i in str(math_operator).split(":")]
        threshold_value_list = [i.strip() for i in str(threshold_value).split(":")]
        if len(metric_name_list) == len(math_operator_list) == len(threshold_value_list):
            for i in range(len(metric_name_list)):
                expression_str_tmp = metric_name_list[i] + math_operator_list[i] + threshold_value_list[i]
                expression_list.append(expression_str_tmp)
        else:
            expression_list.append("指标表达式获取异常")
        return expression_list


class CapacityMetricController(CollectionController):
    name = 'monitor.capacity_metric'
    allow_methods = ('GET',)
    resource = capacity_metric_filter_strategy_api.CapacityMetricApi

    def on_get(self, req, resp, **kwargs):
        self._validate_method(req)
        criteria = self._build_criteria(req)
        refs = self.list(req, copy.deepcopy(criteria), **kwargs)
        count = self.count(req, criteria, results=refs, **kwargs)
        resp.json = {'count': count, 'data': refs}


class CapacityMetricFilterStrategyController(CollectionController, CapacityMetricFilterStrategyBase):
    name = 'monitor.capacity_metric_filter_strategy'
    allow_methods = ('GET', 'POST')
    resource = capacity_metric_filter_strategy_api.CapacityMetricFilterStrategyApi

    def on_get(self, req, resp, **kwargs):
        self._validate_method(req)
        criteria = self._build_criteria(req)
        filters = criteria["filters"]
        filters = self.check_object_tree_type(filters)
        filters_new = self.replace_args_name(self._arg_model_mapping(), filters)
        if filters_new.has_key("f_creator"):
            creator_filter = filters_new.get("f_creator")
            if creator_filter and isinstance(creator_filter, list):
                creator_filter.append("")
                filters_new["f_creator"] = creator_filter
            if creator_filter and isinstance(creator_filter, basestring):
                creator_filter_new = [creator_filter, ""]
                filters_new["f_creator"] = creator_filter_new
        criteria["filters"] = filters_new

        # todo 兼容可用区(a,b)
        f_az_id = criteria["filters"].get("f_az_id")
        if f_az_id and isinstance(f_az_id, list):
            tmp = ""
            i = 0
            dict_tmp = {0: f_az_id[0]}
            for v in f_az_id[1:]:
                if len(v) < 3:
                    tmp += v
                    dict_tmp[i] = dict_tmp[i] + "," + v
                else:
                    i += 1
                    dict_tmp[i] = v
            f_az_id_tmp = dict_tmp.values()
            if len(f_az_id_tmp) == 1:
                f_az_id_tmp = f_az_id_tmp[0]
            criteria["filters"]["f_az_id"] = f_az_id_tmp

        refs = []
        count = 0
        # 集群 区域可用区自定标签
        f_object_type = filters_new.get("f_object_type")
        if f_object_type == const_define.CapacityTreeType.AzTreeType:
            f_region_id = criteria["filters"].get("f_region_id")
            f_az_id = criteria["filters"].get("f_az_id")
            # 区域继承
            if f_region_id:
                criteria["filters"]["f_region_id"] = [f_region_id, "", None]
                criteria["filters"]["f_az_id"] = [f_az_id, "", None]
            elif not f_region_id and not f_az_id:
                criteria["filters"]["f_az_id"] = ["", None]
                criteria["filters"]["f_region_id"] = ["", None]

            refs = self.list(req, copy.deepcopy(criteria), **kwargs)
            count = self.count(req, criteria, results=refs, **kwargs)
        elif f_object_type == const_define.CapacityTreeType.ProjectTreeType:
            # 项目 租户自定义标签
            tree_routes = criteria["filters"].pop("tree_route", "")
            strategy_id_list = []
            f_metric_type = filters_new.get("f_metric_type")
            cst = CsapacityStrategyTreeRouteResource()
            # 项目租户继承
            if isinstance(tree_routes, str):
                tree_routes = [tree_routes]
            for tree_route in tree_routes:
                try:
                    def get_strategy(route):
                        if len(route) == 1:
                            return
                        # 根据tree_route获取自定义标签
                        ret = cst.list(filters={"tree_route": route, "metric_type": f_metric_type})
                        for i in ret:
                            if i["strategy_id"] in strategy_id_list:
                                continue
                            # 自定义标签列表
                            strategy_id_list.append(i["strategy_id"])
                        res = os.path.split(route)[0]
                        get_strategy(res)
                except Exception as e:
                    logging.error("get strategy failed: %s" % e)
                    raise NotFoundError("数据异常，获取标签策略失败")
                get_strategy(tree_route)
            criteria["filters"]["f_id"] = strategy_id_list
            refs = self.list(req, copy.deepcopy(criteria), **kwargs)
            count = len(refs)

        criteria["filters"] = {}
        criteria["filters"]["f_object_type"] = 3
        criteria["filters"]["f_metric_type"] = filters_new.get('f_metric_type', 1)
        refs_tmp = self.list(req, copy.deepcopy(criteria), **kwargs)  # 获取默认的指标信息
        count_tmp = self.count(req, criteria, results=refs, **kwargs)
        refs = refs_tmp + refs
        count += count_tmp

        metric_name_dict = self.get_metric_name_dict()
        if len(refs) > const_define.CapacityFilterStrategy.OnceSelectMaxCount:
            raise ValidationError("该接口单次查询结果数不能超过%s" % const_define.CapacityFilterStrategy.OnceSelectMaxCount)
        for filter_strategy_info in refs:
            filter_strategy_info["metric_expressions"] = self.get_expression_by_info(filter_strategy_info,
                                                                                     metric_name_dict)
        resp.json = {'count': count, 'data': refs}

    def on_post(self, req, resp, **kwargs):
        self._validate_method(req)
        checked_data = check_params_with_model(req.json, self._arg_model_create_data(), keep_extra_key=False)
        checked_data = self.check_object_tree_type(checked_data)
        checked_data_new = self.replace_args_name(self._arg_model_mapping(), checked_data)
        checked_data_new = self.check_metric_data(checked_data_new)
        tree_route = checked_data_new.pop("tree_route", "")
        capacity_metric_filter_strategy_api = self.make_resource(req)
        resp.status = falcon.HTTP_201
        resp.json = capacity_metric_filter_strategy_api.create(checked_data_new)
        # 创建标签和tree_route的绑定关系
        f_id = resp.json["f_id"]
        self.on_post_strategytreeroute(checked_data, f_id, tree_route)

    @staticmethod
    def on_post_strategytreeroute(checked_data, f_id, tree_routes):
        """
        创建标签与策略绑定
        :param checked_data: 标签数据
        :param f_id: 标签id
        :param tree_routes: 租户路径
        :return:
        """
        try:
            if checked_data.get("object_tree_type") != const_define.CapacityTreeType.ProjectTreeType \
                    and not tree_routes:
                return
            cst = CsapacityStrategyTreeRouteResource()
            data = {
                "strategy_id": f_id,
                "metric_type": checked_data["f_metric_type"]
            }
            for tree_route in tree_routes.split(","):
                data["tree_route"] = tree_route
                try:
                    cst.create(data)
                except Exception as e:
                    logging.error("create strategytreeroute failed: %s" % e)
                    continue
        except Exception as e:
            logging.error("on_post_strategytreeroute failed: %s" % e)


class CapacityMetricFilterStrategyItemController(ItemController, CapacityMetricFilterStrategyBase):
    name = 'monitor.capacity_metric_filter_strategy.item'
    allow_methods = ('GET', 'PATCH', 'DELETE')
    resource = capacity_metric_filter_strategy_api.CapacityMetricFilterStrategyApi

    def on_get(self, req, resp, **kwargs):
        self._validate_method(req)
        capacity_metric_filter_strategy_id = kwargs.pop('rid')
        capacity_metric_filter_strategy_api = self.make_resource(req)
        capacity_metric_filter_strategy_info = capacity_metric_filter_strategy_api.get(
            capacity_metric_filter_strategy_id)
        if not capacity_metric_filter_strategy_info:
            raise NotFoundError("filter_strategy_id: %s, 不存在" % capacity_metric_filter_strategy_id)
        resp.json = capacity_metric_filter_strategy_info

    def on_patch(self, req, resp, **kwargs):
        self._validate_method(req)
        capacity_metric_filter_strategy_id = kwargs.pop('rid')
        capacity_metric_filter_strategy_api = self.make_resource(req)
        capacity_metric_filter_strategy_info = capacity_metric_filter_strategy_api.get(
            capacity_metric_filter_strategy_id)
        if not capacity_metric_filter_strategy_info:
            raise NotFoundError("filter_strategy_id: %s, 不存在" % capacity_metric_filter_strategy_id)
        json_data = req.json
        creator = json_data.get("creator", None) or None
        is_admin = json_data.get("is_admin", False) or False
        checked_data = check_params_with_model(json_data, self._arg_model_update_data(), keep_extra_key=False)
        f_creator = capacity_metric_filter_strategy_info["f_creator"]
        if creator != f_creator and not is_admin:
            raise ForbiddenError("Forbidden, The operation is not allowed!")
        if not checked_data:
            resp.json = capacity_metric_filter_strategy_info
        else:
            checked_data_new = self.replace_args_name(self._arg_model_mapping(), checked_data)
            checked_data_new = self.check_metric_data(checked_data_new)
            before, after = capacity_metric_filter_strategy_api.update(capacity_metric_filter_strategy_id,
                                                                       checked_data_new)
            resp.json = after

    def on_delete(self, req, resp, **kwargs):
        self._validate_method(req)
        capacity_metric_filter_strategy_id = kwargs.pop('rid')
        capacity_metric_filter_strategy_api = self.make_resource(req)
        capacity_metric_filter_strategy_info = capacity_metric_filter_strategy_api.get(
            capacity_metric_filter_strategy_id)
        if not capacity_metric_filter_strategy_info:
            raise NotFoundError("filter_strategy_id: %s, 不存在" % capacity_metric_filter_strategy_id)
        else:
            json_data = req.json
            creator = json_data.get("creator", None) or None
            is_admin = json_data.get("is_admin", False) or False
            f_creator = capacity_metric_filter_strategy_info["f_creator"]
            if creator != f_creator and not is_admin:
                raise ForbiddenError("Forbidden, The operation is not allowed!")
            before, after = capacity_metric_filter_strategy_api.update(capacity_metric_filter_strategy_id,
                                                                       {"f_enabled": 0})
            resp.json = {"count": 1, "data": [after]}
            self.on_delete_strategytreeroute(capacity_metric_filter_strategy_id)

    @staticmethod
    def on_delete_strategytreeroute(f_id):
        """
        删除所有标签与tree_route记录
        :param f_id: 标签id
        :return:
        """
        try:
            cst = CsapacityStrategyTreeRouteResource()
            cst.delete_all({"strategy_id": f_id})
        except Exception as e:
            logging.error("on_delete_strategytreeroute failed: %s" % e)
