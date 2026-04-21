# coding: utf-8
from monitor.apps.database_server.api import alrams_api
from monitor.common.controller import CollectionController, ItemController, ResourceInterface


class DatabaseServerEventCasesManageController(CollectionController):
    name = 'database_server.event_cases'
    allow_methods = ('GET', 'POST')
    resource = alrams_api.EventCasesManageResourceApi


class DatabaseServerEventCasesItemManageController(ItemController):
    name = 'database_server.event_cases.item'
    allow_methods = ('GET', 'PATCH', 'DELETE')
    resource = alrams_api.EventCasesManageResourceApi


class DatabaseServerEventCasesBatchSyncManageController(ResourceInterface):
    name = 'database_server.event_cases.batch_sync'
    allow_methods = ('PATCH', )
    resource = alrams_api.EventCasesManageResourceApi
    

class DatabaseServerAlarmStatusManageController(CollectionController):
    name = 'database_server.alarm_status'
    allow_methods = ('GET', 'POST')
    resource = alrams_api.AlarmStatusManageResourceApi


class DatabaseServerAlarmStatusItemManageController(ItemController):
    name = 'database_server.alarm_status.item'
    allow_methods = ('GET', 'PATCH', 'DELETE')
    resource = alrams_api.AlarmStatusManageResourceApi


class DatabaseServerAlarmStatusBatchSyncManageController(ResourceInterface):
    name = 'database_server.alarm_status.batch_sync'
    allow_methods = ('PATCH', )
    resource = alrams_api.AlarmStatusManageResourceApi


class DatabaseServerDelLogManageController(CollectionController):
    name = 'database_server.del_log'
    allow_methods = ('GET', 'POST')
    resource = alrams_api.DelLogManageManageResourceApi


class DatabaseServerDelLogItemManageController(ItemController):
    name = 'database_server.del_log.item'
    allow_methods = ('GET', 'PATCH', 'DELETE')
    resource = alrams_api.DelLogManageManageResourceApi


class DatabaseServerDelLogBatchSyncManageController(ResourceInterface):
    name = 'database_server.del_log.batch_sync'
    allow_methods = ('PATCH', )
    resource = alrams_api.DelLogManageManageResourceApi


class DatabaseServerEventReportManageController(CollectionController):
    name = 'database_server.event_report'
    allow_methods = ('GET', 'POST')
    resource = alrams_api.EventReportManageResourceApi


class DatabaseServerEventReportItemManageController(ItemController):
    name = 'database_server.event_report.item'
    allow_methods = ('GET', 'PATCH', 'DELETE')
    resource = alrams_api.EventReportManageResourceApi


class DatabaseServerEventReportBatchSyncManageController(ResourceInterface):
    name = 'database_server.event_report.batch_sync'
    allow_methods = ('PATCH', )
    resource = alrams_api.EventReportManageResourceApi


class DatabaseServerEventsManageController(CollectionController):
    name = 'database_server.events'
    allow_methods = ('GET', 'POST')
    resource = alrams_api.EventsManageResourceApi


class DatabaseServerEventsItemManageController(ItemController):
    name = 'database_server.events.item'
    allow_methods = ('GET', 'PATCH', 'DELETE')
    resource = alrams_api.EventsManageResourceApi


class DatabaseServerEventsBatchSyncManageController(ResourceInterface):
    name = 'database_server.events.batch_sync'
    allow_methods = ('PATCH', )
    resource = alrams_api.EventsManageResourceApi


class DatabaseServerRemarkCommonManageController(CollectionController):
    name = 'database_server.remark_common'
    allow_methods = ('GET', 'POST')
    resource = alrams_api.RemarkCommonManageResourceApi


class DatabaseServerRemarkCommonItemManageController(ItemController):
    name = 'database_server.remark_common.item'
    allow_methods = ('GET', 'PATCH', 'DELETE')
    resource = alrams_api.RemarkCommonManageResourceApi


class DatabaseServerRemarkCommonBatchSyncManageController(ResourceInterface):
    name = 'database_server.remark_common.batch_sync'
    allow_methods = ('PATCH', )
    resource = alrams_api.RemarkCommonManageResourceApi
