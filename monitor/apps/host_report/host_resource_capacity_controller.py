# coding: utf-8
import IPy

from monitor.apps.host_report.api import host_resource_capacity_api, capacity_metric_filter_strategy_api
from monitor.apps.host_report.api import tenant_api
from monitor.common import time_util, const_define
from monitor.common.controller import CollectionController
from monitor.common.decorators import tenant_project_func
from monitor.core.exceptions import ValidationError
from monitor.lib.redis_lib import RedisForCommon
from monitor.utils import utils


class HostResourceCapacityBase(object):

    @staticmethod
    def _arg_model_get_cpu_statistics_data():
        base_define = {
            0: "0-10",
            10: "10-50",
            50: "50-90",
            90: "90-100"
        }
        return base_define

    @staticmethod
    def _arg_model_get_mem_statistics_data():
        base_define = {
            0: "0-10",
            10: "10-50",
            50: "50-90",
            90: "90-100"
        }
        return base_define

    @staticmethod
    def get_statistic_data_by_value(metric_threshold_dict, metric_value_list):
        metric_statistic_dict = {k: 0 for k in metric_threshold_dict.values()}
        new_metric_threshold_list = sorted(metric_threshold_dict.keys(), reverse=True)
        for metric_value in metric_value_list:
            for metric_threshold in new_metric_threshold_list:
                if metric_value >= metric_threshold:
                    metric_statistic_dict[metric_threshold_dict[metric_threshold]] += 1
                    break
        return metric_statistic_dict


class HostResourceCapacityController(CollectionController, HostResourceCapacityBase):
    name = 'monitor.host_stat'
    allow_methods = ('GET',)
    resource = host_resource_capacity_api.HostResourceCapacityApi

    @tenant_project_func(True, "f_tenant_id", "f_project_id", False)
    def _build_criteria(self, req, supported_filters=None):
        return super(HostResourceCapacityController, self)._build_criteria(req)

    def on_get(self, req, resp, **kwargs):
        self._validate_method(req)
        criteria = self._build_criteria(req)
        filters = criteria["filters"]
        if filters.get("f_ip"):
            f_ip = filters.get("f_ip")
            if f_ip and isinstance(f_ip,dict):
                ip = f_ip.get('ilike')
                if ip and utils.ipv6_validator(ip):
                    ip = str(IPy.IP(ip))
                    filters["f_ip"].update({"ilike":ip})
        filters_dict = {}
        if "stat_type" in filters.keys():
            stat_type = filters.pop("stat_type", None)
            if stat_type == const_define.HostCapacityType.DayTable:
                host_stat_api = host_resource_capacity_api.HostResourceCapacityApi()
            elif stat_type == const_define.HostCapacityType.WeekTable:
                host_stat_api = host_resource_capacity_api.HostResourceCapacityWeekApi()
            elif stat_type == const_define.HostCapacityType.MonthTable:
                host_stat_api = host_resource_capacity_api.HostResourceCapacityMonthApi()
                try:
                    for k in filters['f_date_time']:  # 日期截断 去除日字段
                        filters['f_date_time'][k] = filters['f_date_time'][k][:7]
                except Exception as e:
                    pass
            elif stat_type == const_define.HostCapacityType.LastDaysTable:
                host_stat_api = host_resource_capacity_api.HostResourceCapacityLastDaysApi()
            else:
                raise ValidationError(
                    "params参数 stat_type: %s, 必须在 %s中" % (stat_type, const_define.HostCapacityType.ALL_TYPE))
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
        refs = host_stat_api.list(**criteria)
        uuids = [i.get("f_belong_to_host") for i in refs if i.get("f_belong_to_host")]
        uuid_hostname = self.resource().get_hostname_by_uuid(uuids)
        if fields is not None:
            refs = [self._simplify_info(ref, fields) for ref in refs]
        if uuid_hostname:
            for item in refs:
                f_belong_to_host = item.get("f_belong_to_host")
                if not f_belong_to_host:
                    continue
                # 展示主机名
                item["f_belong_to_host"] = uuid_hostname.get(f_belong_to_host, "")
        count = host_stat_api.count(filters)
        resp.json = {'count': count, 'data': refs}


class HostResourceCapacityStatisticsController(CollectionController, HostResourceCapacityBase):
    name = 'monitor.host_stat_statistics'
    allow_methods = ('GET',)
    resource = host_resource_capacity_api.HostResourceCapacityLastDaysApi
    tenant_resource_api = tenant_api.TenantApi()
    redis_conn = RedisForCommon.get_instance_for_common_1()

    def on_get(self, req, resp, **kwargs):
        self._validate_method(req)
        criteria = self._build_criteria(req)
        filters = criteria.get("filters") or {}
        # 这里特殊处理框架下切割可用区异常的问，例如ali-cn-MAZ3(a,b,c)格式的可用区
        if "f_az_id" in filters:
            import urlparse
            params_str = urlparse.urlparse(req.url)
            params_tmp = urlparse.parse_qs(params_str.query)
            filters["f_az_id"] = params_tmp["f_az_id"][0]

        # 判断是自定义层级还是标准层级
        is_oa_type = filters.pop("is_oa_type", None)
        project_id_list = filters.pop('project_ids', None) or []
        if project_id_list:  # 有项目忽略node_ids tenant_ids
            filters.pop("node_ids", None)
            filters.pop("tenant_ids", None)
        # 租户
        cloud_tenant_id_list = filters.pop('tenant_ids', None) or []
        tenant_list = []

        # 行政组织 标准层级
        node_ids = filters.get("node_ids", None)
        is_all = filters.get("is_all")  # 标准层级全选
        if (node_ids and is_oa_type) or (is_all and is_oa_type):
            if is_all:
                project_list = self.tenant_resource_api.get_project_id_by_node_ids(is_all=True)
            else:
                project_list = self.tenant_resource_api.get_project_id_by_node_ids(node_ids=node_ids)
            if project_list:
                project_id_list.extend(project_list)
            else:
                filters["f_project_id"] = []
        elif node_ids:
            # 自定义层级
            tenant_list = self.tenant_resource_api.get_tenant_id_by_node_ids(node_ids)
        if tenant_list:
            cloud_tenant_id_list.extend(tenant_list)
            filters["f_tenant_id"] = list(set(cloud_tenant_id_list))
        else:
            if cloud_tenant_id_list:
                filters["f_tenant_id"] = cloud_tenant_id_list
            else:
                # 传了tenant_ids还是空
                if "node_ids" in filters and not is_oa_type:
                    filters["f_tenant_id"] = []

        for k, v in filters.items():
            if k not in ["f_host_type", "f_date_time", "f_az_id", "f_region_id", "f_project_id", "f_tenant_id"]:
                filters.pop(k, None)

        # 项目
        if "f_project_id" not in filters and project_id_list:
            filters["f_project_id"] = list(set(project_id_list))

        # 用户门户 处理用户所授权的租户和项目
        headers = req.headers  # 转为全小写
        if "X-AUTH-TENANT" in headers or "X-AUTH-PROJECT" in headers:
            admin_flag = False  # 判断是否是用户门户
        else:
            admin_flag = True
        if not admin_flag:  # 区分用户门户和云管门户
            uid = headers.get("X-AUTH-UID", None)
            if uid:
                operating_dict = self.redis_conn.hgetall("operating_%s" % uid) or {}
                if operating_dict.get("admin") != "1":
                    authored_tenant_ids = operating_dict.get("tenant_id").split(",") \
                        if operating_dict.get("tenant_id") else []
                    authored_project_ids = operating_dict.get("project_id").split(",") \
                        if operating_dict.get("project_id") else []
                    if "f_project_id" in filters:
                        project_id_filter = filters.get("f_project_id")
                        authored_project_ids = [i for i in project_id_filter if i in authored_project_ids]
                    if "f_tenant_id" in filters:
                        tenant_id_filter = filters.get("f_tenant_id")
                        authored_tenant_ids = [i for i in tenant_id_filter if i in authored_tenant_ids]
                    filters["f_project_id"] = authored_project_ids
                    # 是否为空
                    # if authored_tenant_ids:
                    #     filters["f_tenant_id"] = self.tenant_resource_api.get_cmdb_uuid_by_list(authored_tenant_ids)
                    # else:
                    #     filters["f_tenant_id"] = []
                    filters["f_tenant_id"] = authored_tenant_ids
            else:
                filters["f_project_id"] = []
                filters["f_tenant_id"] = []
        # else:
        #     if "f_tenant_id" in filters:
        #         tenant_id_filter = filters.get("f_tenant_id")
        #         if tenant_id_filter:
        #             filters["f_tenant_id"] = self.tenant_resource_api.get_cmdb_uuid_by_list(tenant_id_filter)
        #         else:
        #             filters["f_tenant_id"] = []

        host_type = filters.get("f_host_type") or "vm"
        date_time = filters.get("f_date_time")
        if host_type not in ["vm", "host"]:
            raise ValidationError("host_type: %s, must be in [vm, host]" % host_type)
        if date_time and time_util.is_data_str(date_time):
            day_str = date_time
        else:
            day_str = time_util.get_yesterday_str()
        filters.update({"f_host_type": host_type, "f_date_time": day_str})

        select_fields = ["f_cpu_busy_p95", "f_mem_use_percent_p95", "f_tenant_id", "f_project_id"]
        # 为了优化查询 使用sql获取数据
        host_stat_list = self.resource().select_host_data(
            select_fields=select_fields, filters=filters, admin=admin_flag)

        metric_name_resp_list = self._get_metric_name_resp_list(host_stat_list)
        resp.json = {"count": len(metric_name_resp_list), "data": metric_name_resp_list}

    def _get_metric_name_resp_list(self, host_stat_list):
        """
        根据data计算出容量数据
        :param host_stat_list: list
        :return: list
        """
        cpu_busy_list = []
        mem_use_percent_list = []
        for i in host_stat_list:
            cpu_busy_list.append(i[0])
            mem_use_percent_list.append(i[1])
        metric_name_resp_list = []
        cpu_statistic_dict = self.get_statistic_data_by_value(self._arg_model_get_cpu_statistics_data(), cpu_busy_list)
        metric_name_resp_list.append({"f_cpu_busy_p95": cpu_statistic_dict})
        mem_statistic_dict = self.get_statistic_data_by_value(self._arg_model_get_mem_statistics_data(),
                                                              mem_use_percent_list)
        metric_name_resp_list.append({"f_mem_use_percent_p95": mem_statistic_dict})
        return metric_name_resp_list
