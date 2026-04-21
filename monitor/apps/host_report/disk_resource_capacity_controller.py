#!/usr/bin/python
# -*- coding:utf-8 -*-

from monitor.common.controller import CollectionController
from monitor.apps.host_report.api import disk_resource_capacity_api, capacity_metric_filter_strategy_api
from monitor.apps.host_report.dbresources.resource import DiskResourceCapacityResource
from monitor.apps.host_report.api import tenant_api
from monitor.common import time_util, const_define
from monitor.core.exceptions import ValidationError
from monitor.lib.redis_lib import RedisForCommon
from monitor.common.decorators import tenant_project_func
from monitor.apps.alert.dbresources.resource import TenantResource, ProjectResource
from monitor.apps.database_server.dbresources.resource import AvailableZoneResource

class DiskResourceCapacityBase(object):

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


class DiskResourceCapacityController(CollectionController, DiskResourceCapacityBase):
    name = 'monitor.db_stat'
    allow_methods = ('GET',)
    resource = disk_resource_capacity_api.DiskResourceCapacityApi

    special_filter_keys = ('t_if_project.id', 't_if_project.name', 't_iam_tenant.uuid', 't_iam_tenant.name',
    't_if_region.id', 't_if_region.name', 't_if_az.id', 't_if_az.name', 'cmdb_cbs.tenant_id', 'cmdb_cbs.project_id','cmdb_cbs.az_id')

    @tenant_project_func(True, "cmdb_cbs.tenant_id", "cmdb_cbs.project_id", False)
    def _build_criteria(self, req, supported_filters=None):
        return super(DiskResourceCapacityController, self)._build_criteria(req)

    def on_get(self, req, resp, **kwargs):
        self._validate_method(req)
        criteria = self._build_criteria(req)
        filters = criteria["filters"]
        filters_dict = {}
        if "stat_type" in filters.keys():
            stat_type = filters.pop("stat_type", None)
            disk_stat_api = disk_resource_capacity_api.DiskResourceCapacityApi()
            if stat_type in const_define.DiskCapacityType.ALL_TYPE:
                filters['category'] = stat_type
            else:
                raise ValidationError(
                    "param参数 stat_type: %s, 必须在 %s中" % (stat_type, const_define.DiskCapacityType.ALL_TYPE))
        else:
            raise ValidationError("params参数 stat_type: 不能为空")

        if "filter_strategy_id" in filters.keys():
            filter_strategy_id = filters.pop("filter_strategy_id", None)
            if filter_strategy_id is not None:
                filters_dict = capacity_metric_filter_strategy_api.CapacityMetricFilterStrategyApi().get_filter_dict(
                    filter_strategy_id)
                criteria["filters"].update(filters_dict)
            else:
                raise ValidationError("param参数 filter_stragegy_id不能为空")

        fields = criteria.pop('fields', None)
        add_filter = False
        cbs_filters = {}
        for key in filters.keys():
            if key in self.special_filter_keys:
                cbs_filters[key] = filters[key]
                add_filter = True

        if not add_filter:  # 这里返回信息的第三级关联无法使用框架的过滤，单独处理
            refs = disk_stat_api.list(**criteria)
            count = self.count(req, criteria, results=refs, **kwargs)
        else:
            filters = criteria["filters"]
            offset = criteria["offset"]
            orders = criteria["orders"]
            limit = criteria["limit"]
            filter = self.convert_filters(cbs_filters)
            filters.update(filter)
            count, refs = disk_stat_api.select_stat_with_tenant_project(filters, offset, limit, orders, filters_dict)
        if fields is not None:
            refs = [self._simplify_info(ref, fields) for ref in refs]
        # 磁盘实际使用量是不对用户门户开放
        if req.headers.get('X-AUTH-PROJECT') and req.headers.get('X-AUTH-TENANT'):
            for ref in refs:
                ref.pop('actual_used_size')
                ref.pop('used_rate')
        resp.json = {'count': count, 'data': refs}

    def convert_filters(self, cbs_filters):
        filter = {}
        for key, value in cbs_filters.items():
            if key == "t_iam_tenant.name":
                filter["tenant_id"] = TenantResource().get_id_by_name(value)
            elif key == "t_iam_tenant.uuid":
                filter["tenant_id"] = value
            elif key == "t_if_project.name":
                filter["project_id"] = ProjectResource().get_id_by_name(value)
            elif key == "t_if_project.id":
                if isinstance(value, str):
                    filter["project_id"] = [value]
                elif isinstance(value, list):
                    filter["project_id"] = value
            elif key == "t_if_region.id":
                if isinstance(value, str):
                    filter["t_if_region"] = [value]
                elif isinstance(value, list):
                    filter["t_if_region"] = value
            elif key == "t_if_az.name":
                filter["az_id"] = AvailableZoneResource().get_id_by_name(cbs_filters[key])
            elif key == "t_if_az.id":
                if isinstance(value, str):
                    filter["az_id"] = [value]
                elif isinstance(value, list):
                    filter["az_id"] = value
            elif key == "cmdb_cbs.tenant_id":
                if isinstance(value, str):
                    filter["tenant_id"] = [value]
                elif isinstance(value, list):
                    filter["tenant_id"] = value
            elif key == "cmdb_cbs.project_id":
                if isinstance(value, str):
                    filter["project_id"] = [value]
                elif isinstance(value, list):
                    filter["project_id"] = value
            elif key == "cmdb_cbs.az_id":
                if isinstance(value, str):
                    filter["az_id"] = [value]
                elif isinstance(value, list):
                    filter["az_id"] = value
        return filter

class DiskResourceCapacityStatisticsController(CollectionController, DiskResourceCapacityBase):
    name = 'monitor_database_statistics'
    allow_methods = ('GET',)
    resource = DiskResourceCapacityResource
    tenant_resource_api = tenant_api.TenantApi()
    redis_conn = RedisForCommon.get_instance_for_common_1()

    @staticmethod
    def _base_resp_list():
        return [
            {"disk_io_util_p95": {"90-100": 0, "50-90": 0, "10-50": 0, "0-10": 0}},
            {"disk_io_write_requests_p95": {"90-100": 0, "50-90": 0, "10-50": 0, "0-10": 0}},
            {"disk_io_read_requests_p95": {"90-100": 0, "50-90": 0, "10-50": 0, "0-10": 0}}
        ]

    def on_get(self, req, resp, **kwargs):
        self._validate_method(req)
        criteria = self._build_criteria(req)
        filters = criteria["filters"]
        # 这里特殊处理框架下切割可用区异常的问，例如ali-cn-MAZ3(a,b,c)格式的可用区
        if "cmdb_cbs.az_id" in filters:
            import urlparse
            params_str = urlparse.urlparse(req.url)
            params_tmp = urlparse.parse_qs(params_str.query)
            filters["cmdb_cbs.az_id"] = params_tmp["f_az_id"][0]

        project_id_list = filters.pop('project_ids', None) or []
        if project_id_list:  # 有项目忽略node_ids tenant_ids
            filters.pop("node_ids", None)
            filters.pop("tenant_ids", None)
        tenant_id_filter = filters.pop("tenant_ids", None) or []
        tenant_list = []

        # 行政组织
        is_oa_type = filters.pop("is_oa_type", None)
        node_ids = filters.get("node_ids", None)
        is_all = filters.pop("is_all", None)
        if (node_ids and is_oa_type) or (is_all and is_oa_type):
            if is_all:
                project_list = self.tenant_resource_api.get_project_id_by_node_ids(is_all=True)
            else:
                project_list = self.tenant_resource_api.get_project_id_by_node_ids(node_ids=node_ids)
            if project_list:
                project_id_list.extend(project_list)
            else:
                filters["cmdb_cbs.project_id"] = []
        elif node_ids:
            # 自定义层级
            tenant_list = self.tenant_resource_api.get_tenant_id_by_node_ids(node_ids)
        if tenant_list:
            tenant_id_filter.extend(tenant_list)
            filters["cmdb_cbs.tenant_id"] = list(set(tenant_id_filter))
        else:
            if tenant_id_filter:
                filters["cmdb_cbs.tenant_id"] = tenant_id_filter
            else:
                # node_ids获取tenant_id为空
                if "node_ids" in filters and not is_oa_type:
                    filters["cmdb_cbs.tenant_id"] = []
        filters.pop("node_ids", None)

        # 项目
        if "cmdb_cbs.project_id" not in filters and project_id_list:
            filters["cmdb_cbs.project_id"] = list(set(project_id_list))

        headers = req.headers  # 转为全小写
        if "X-AUTH-TENANT" in headers or "X-AUTH-PROJECT" in headers:
            admin_flag = False  # 判断是否是用户门户
        else:
            admin_flag = True

        classify_type = filters.pop("classify_type",None)
        if classify_type == "admin":
            admin_flag = True

        # if "cmdb_cbs.tenant_id" in filters and admin_flag:
        #     tenant_id_filter = filters.get("cmdb_cbs.tenant_id")
        #     if tenant_id_filter:
        #         filters["cmdb_cbs.tenant_id"] = self.tenant_resource_api.get_cmdb_uuid_by_list(tenant_id_filter)
        #     else:
        #         filters["cmdb_cbs.tenant_id"] = []
        if "cmdb_cbs.project_id" in filters and "cmdb_cbs.tenant_id" in filters and admin_flag:
            project_id_filter = filters.pop("cmdb_cbs.project_id")
            tenant_id_filter = filters.pop("cmdb_cbs.tenant_id")
            filters["$or"] = [{"cmdb_cbs.project_id": project_id_filter},
                              {"cmdb_cbs.tenant_id": tenant_id_filter}]

        # 用户门户 处理用户所授权的租户和项目
        if not admin_flag:  # 区分用户门户和云管门户
            uid = headers.get("X-AUTH-UID", None)
            if uid:
                operating_dict = self.redis_conn.hgetall("operating_%s" % uid) or {}
                if operating_dict.get("admin") != "1":
                    authored_tenant_ids = operating_dict.get("tenant_id").split(",") \
                        if operating_dict.get("tenant_id") else []
                    authored_project_ids = operating_dict.get("project_id").split(",") \
                        if operating_dict.get("project_id") else []
                    if "cmdb_cbs.project_id" in filters:
                        project_id_filter = filters.get("cmdb_cbs.project_id")
                        authored_project_ids = [i for i in project_id_filter if i in authored_project_ids]
                    if "cmdb_cbs.tenant_id" in filters:
                        tenant_id_filter = filters.get("cmdb_cbs.tenant_id")
                        authored_tenant_ids = [i for i in tenant_id_filter if i in authored_tenant_ids]
                    filters["cmdb_cbs.project_id"] = authored_project_ids
                    # if authored_tenant_ids:
                    #     filters["cmdb_cbs.tenant_id"] = self.tenant_resource_api.get_cmdb_uuid_by_list(authored_tenant_ids)
                    # else:
                    #     filters["cmdb_cbs.tenant_id"] = []
                    filters["cmdb_cbs.tenant_id"] = authored_tenant_ids

            else:
                filters["cmdb_cbs.project_id"] = []
                filters["cmdb_cbs.tenant_id"] = []

        host_stat_api = self.resource()
        yesterday_str = time_util.get_yesterday_str()
        now_str = time_util.get_now_str()
        # 添加过滤daily
        if not filters.get("category"):
            filters["category"] = "last30days"
        # 去除埋点
        filters.pop("tRequestId", None)
        filters.update({"timestamp_lte": now_str, "timestamp_gte": yesterday_str})
        host_stat_list = host_stat_api.select_stat_statistic(filters)
        metric_name_resp_list = self._get_metric_name_resp_list(host_stat_list)
        resp.json = {"count": len(metric_name_resp_list), "data": metric_name_resp_list}

    @staticmethod
    def _get_metric_name_resp_list(host_stat_list):
        metric_threshold_dict = {
            0: "0-10",
            10: "10-50",
            50: "50-90",
            90: "90-100"
        }
        disk_io_util_p95_dict = {k: 0 for k in metric_threshold_dict.values()}
        disk_io_write_requests_p95_dict = {k: 0 for k in metric_threshold_dict.values()}
        disk_io_read_requests_p95_dict = {k: 0 for k in metric_threshold_dict.values()}
        new_metric_threshold_list = sorted(metric_threshold_dict.keys(), reverse=True)

        for i in host_stat_list:
            if isinstance(i, dict):
                disk_io_util_p95 = i["disk_io_util_p95"]
                disk_io_write_requests_p95 = i["disk_io_write_requests_p95"]
                disk_io_read_requests_p95 = i["disk_io_read_requests_p95"]
            else:
                disk_io_util_p95 = i[0]
                disk_io_write_requests_p95 = i[1]
                disk_io_read_requests_p95 = i[2]
            # 10 50 90 100
            for metric_threshold in new_metric_threshold_list:
                if disk_io_util_p95 >= metric_threshold:
                    # 0-10: 0
                    disk_io_util_p95_dict[metric_threshold_dict[metric_threshold]] += 1
                    break
            for metric_threshold in new_metric_threshold_list:
                if disk_io_read_requests_p95 >= metric_threshold:
                    disk_io_read_requests_p95_dict[metric_threshold_dict[metric_threshold]] += 1
                    break
            for metric_threshold in new_metric_threshold_list:
                if disk_io_write_requests_p95 >= metric_threshold:
                    disk_io_write_requests_p95_dict[metric_threshold_dict[metric_threshold]] += 1
                    break

        metric_name_resp_list = list()
        metric_name_resp_list.append({"disk_io_util_p95": disk_io_util_p95_dict})
        metric_name_resp_list.append({"disk_io_read_requests_p95": disk_io_read_requests_p95_dict})
        metric_name_resp_list.append({"disk_io_write_requests_p95": disk_io_write_requests_p95_dict})
        return metric_name_resp_list
