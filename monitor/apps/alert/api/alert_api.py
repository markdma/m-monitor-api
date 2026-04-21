# coding: utf-8
from __future__ import absolute_import

from monitor.apps.alert.dbresources import resource


class AlertCaseManageApi(resource.EventCasesManageResource):

    @property
    def default_filter(self):
        return {'status': 'PROBLEM'}


class ShieldListManageApi(resource.MaintainCounterManageResource):

    pass


class AlarmScheManageApi(resource.AlarmScheManageResource):

    @property
    def default_filter(self):
        return {'isenable': 0}



