# coding: utf-8
import copy
import time
import datetime

from monitor.apps.host_report.api import host_report_api
from monitor.common.controller import CollectionController, ItemController
from monitor.core.exceptions import NotFoundError


class HostReportBase(object):

    pass


class HostReportController(CollectionController, HostReportBase):
    name = 'monitor.host_report'
    allow_methods = ('GET',)
    resource = host_report_api.HostReportApi

    def on_get(self, req, resp, **kwargs):
        self._validate_method(req)
        criteria = self._build_criteria(req)
        date_filter_flag = False
        for k in req.params.keys():
            if str(k).startswith("day_date"):
                date_filter_flag = True
                break
        # 默认显示昨天的数据
        if not date_filter_flag:
            yesterday = datetime.datetime.strptime(time.strftime("%Y-%m-%d"), '%Y-%m-%d') + datetime.timedelta(days=-1)
            yesterday_str = yesterday.strftime("%Y-%m-%d")
            criteria['filters'].update({'day_date': yesterday_str})
        refs = self.list(req, copy.deepcopy(criteria), **kwargs)
        count = self.count(req, criteria, results=refs, **kwargs)
        resp.json = {'count': count, 'data': refs}


class HostReportItemController(ItemController, HostReportBase):
    name = 'monitor.host_report.item'
    allow_methods = ('GET',)
    resource = host_report_api.HostReportApi

    def on_get(self, req, resp, **kwargs):
        host_report_id = kwargs.pop('rid')
        host_report_api = self.make_resource(req)
        network_device_info = host_report_api.get(host_report_id)
        if not network_device_info:
            raise NotFoundError("host report id:%s不存在" % host_report_id)
        resp.json = network_device_info
