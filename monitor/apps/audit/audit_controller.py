# -*- coding:utf-8 -*-
import copy, datetime

from monitor.apps.audit.dbresource.resource import AuditStatisticsResource, AuditHostResource, \
    AuditDatabaseResource, AuditNetworkResource, AuditNetlineResource

from monitor.common.controller import CollectionController
from monitor.core import config
from monitor.db.crud import ResourceBase
import logging

LOG = logging.getLogger(__name__)

CONF = config.CONF


class AuditStatisticsController(CollectionController):
    name = 'audit.audit_statistics'
    allow_methods = ('GET',)
    resource = AuditStatisticsResource


class AuditBaseController(CollectionController):
    audit_type = ""  # 审计资源类型
    resource = None

    def on_get(self, req, resp, **kwargs):
        self._validate_method(req)
        criteria = self._build_criteria(req)
        now_time = datetime.datetime.now()
        audit_date = now_time.strftime("%Y-%m-%d")
        filters = criteria["filters"]
        filters["date_time"] = audit_date
        # 如果没有传入审计状态 默认获取异常数据
        if not filters.get("status"):
            filters["status"] = 0
        refs = self.list(req, copy.deepcopy(criteria), **kwargs)
        audit_statistics_res = self.audit_statistics_list(audit_date)
        resp.json = {"audit_statistics": audit_statistics_res, "data": refs}

    def audit_statistics_list(self, date_time):
        """
        获取对应资源类型的审计异常统计数据
        :param date_time: 当天日期
        :return: list
        """
        return self.resource().audit_statistics_list(self.audit_type, date_time)


class AuditHostController(AuditBaseController):
    name = 'audit.audit_host'
    allow_methods = ('GET',)
    resource = AuditHostResource
    audit_type = "host"  # 审计资源类型


class AuditDatabaseController(AuditBaseController):
    name = 'audit.audit_database'
    allow_methods = ('GET',)
    resource = AuditDatabaseResource
    audit_type = "database"  # 审计资源类型

    def audit_statistics_list(self, date_time):
        """
        获取对应资源类型的审计异常统计数据
        :param date_time: 当天日期
        :return: list
        """
        pop_fields = ["alive_error_count", "alive_sample_percent", "alive_strategy_error_count",
                      "alive_strategy_sample_percent"]
        return self.resource().audit_statistics_list(self.audit_type, date_time, pop_fields)


class AuditNetworkController(AuditBaseController):
    name = 'audit.audit_network'
    allow_methods = ('GET',)
    resource = AuditNetworkResource
    audit_type = "network"  # 审计资源类型

    def audit_statistics_list(self, date_time):
        """
        获取对应资源类型的审计异常统计数据
        :param date_time: 当天日期
        :return: list
        """
        pop_fields = ["capacity_error_count", "capacity_sample_percent"]
        return self.resource().audit_statistics_list(self.audit_type, date_time, pop_fields)


class AuditNetlineController(AuditBaseController):
    name = 'audit.audit_netline'
    allow_methods = ('GET',)
    resource = AuditNetlineResource
    audit_type = "netline"  # 审计资源类型
