# coding: utf-8
from monitor.apps.database_server.api import dashboard_api
from monitor.common.controller import CollectionController, ItemController, ResourceInterface


class DatabaseServerButtonManageController(CollectionController):
    name = 'database_server.button'
    allow_methods = ('GET', 'POST')
    resource = dashboard_api.ButtonManageResourceApi


class DatabaseServerButtonItemManageController(ItemController):
    name = 'database_server.button.item'
    allow_methods = ('GET', 'PATCH', 'DELETE')
    resource = dashboard_api.ButtonManageResourceApi


class DatabaseServerButtonBatchSyncManageController(ResourceInterface):
    name = 'database_server.button.batch_sync'
    allow_methods = ('PATCH', )
    resource = dashboard_api.ButtonManageResourceApi


class DatabaseServerChartManageController(CollectionController):
    name = 'database_server.chart'
    allow_methods = ('GET', 'POST')
    resource = dashboard_api.ChartManageResourceApi


class DatabaseServerChartItemManageController(ItemController):
    name = 'database_server.chart.item'
    allow_methods = ('GET', 'PATCH', 'DELETE')
    resource = dashboard_api.ChartManageResourceApi


class DatabaseServerChartBatchSyncManageController(ResourceInterface):
    name = 'database_server.chart.batch_sync'
    allow_methods = ('PATCH', )
    resource = dashboard_api.ChartManageResourceApi


class DatabaseServerCustomDashBoardManageController(CollectionController):
    name = 'database_server.custom_dashboard'
    allow_methods = ('GET', 'POST')
    resource = dashboard_api.CustomDashBoardManageResourceApi


class DatabaseServerCustomDashBoardItemManageController(ItemController):
    name = 'database_server.custom_dashboard.item'
    allow_methods = ('GET', 'PATCH', 'DELETE')
    resource = dashboard_api.CustomDashBoardManageResourceApi


class DatabaseServerCustomDashBoardBatchSyncManageController(ResourceInterface):
    name = 'database_server.custom_dashboard.batch_sync'
    allow_methods = ('PATCH', )
    resource = dashboard_api.CustomDashBoardManageResourceApi


class DatabaseServerDashBoardManageController(CollectionController):
    name = 'database_server.dashboard'
    allow_methods = ('GET', 'POST')
    resource = dashboard_api.DashBoardManageResourceApi


class DatabaseServerDashBoardItemManageController(ItemController):
    name = 'database_server.dashboard.item'
    allow_methods = ('GET', 'PATCH', 'DELETE')
    resource = dashboard_api.DashBoardManageResourceApi


class DatabaseServerDashBoardBatchSyncManageController(ResourceInterface):
    name = 'database_server.dashboard.batch_sync'
    allow_methods = ('PATCH', )
    resource = dashboard_api.DashBoardManageResourceApi


class DatabaseServerDashBoardGraphManageController(CollectionController):
    name = 'database_server.dashboard_graph'
    allow_methods = ('GET', 'POST')
    resource = dashboard_api.DashBoardGraphManageResourceApi


class DatabaseServerDashBoardGraphItemManageController(ItemController):
    name = 'database_server.dashboard_graph.item'
    allow_methods = ('GET', 'PATCH', 'DELETE')
    resource = dashboard_api.DashBoardGraphManageResourceApi


class DatabaseServerDashBoardGraphBatchSyncManageController(ResourceInterface):
    name = 'database_server.dashboard_graph.batch_sync'
    allow_methods = ('PATCH', )
    resource = dashboard_api.DashBoardGraphManageResourceApi


class DatabaseServerDashBoardScreenManageController(CollectionController):
    name = 'database_server.dashboard_screen'
    allow_methods = ('GET', 'POST')
    resource = dashboard_api.DashBoardScreenManageResourceApi


class DatabaseServerDashBoardScreenItemManageController(ItemController):
    name = 'database_server.dashboard_screen.item'
    allow_methods = ('GET', 'PATCH', 'DELETE')
    resource = dashboard_api.DashBoardScreenManageResourceApi


class DatabaseServerDashBoardScreenBatchSyncManageController(ResourceInterface):
    name = 'database_server.dashboard_screen.batch_sync'
    allow_methods = ('PATCH', )
    resource = dashboard_api.DashBoardScreenManageResourceApi


class DatabaseServerHostScreenCFGManageController(CollectionController):
    name = 'database_server.host_screen_cfg'
    allow_methods = ('GET', 'POST')
    resource = dashboard_api.HostScreenCFGManageResourceApi


class DatabaseServerHostScreenCFGItemManageController(ItemController):
    name = 'database_server.host_screen_cfg.item'
    allow_methods = ('GET', 'PATCH', 'DELETE')
    resource = dashboard_api.HostScreenCFGManageResourceApi


class DatabaseServerHostScreenCFGBatchSyncManageController(ResourceInterface):
    name = 'database_server.host_screen_cfg.batch_sync'
    allow_methods = ('PATCH', )
    resource = dashboard_api.HostScreenCFGManageResourceApi


class DatabaseServerMessageManageController(CollectionController):
    name = 'database_server.message'
    allow_methods = ('GET', 'POST')
    resource = dashboard_api.MessageManageResourceApi


class DatabaseServerMessageItemManageController(ItemController):
    name = 'database_server.message.item'
    allow_methods = ('GET', 'PATCH', 'DELETE')
    resource = dashboard_api.MessageManageResourceApi


class DatabaseServerMessageBatchSyncManageController(ResourceInterface):
    name = 'database_server.message.batch_sync'
    allow_methods = ('PATCH', )
    resource = dashboard_api.MessageManageResourceApi


class DatabaseServerOptionManageController(CollectionController):
    name = 'database_server.option'
    allow_methods = ('GET', 'POST')
    resource = dashboard_api.OptionManageResourceApi


class DatabaseServerOptionItemManageController(ItemController):
    name = 'database_server.option.item'
    allow_methods = ('GET', 'PATCH', 'DELETE')
    resource = dashboard_api.OptionManageResourceApi


class DatabaseServerOptionBatchSyncManageController(ResourceInterface):
    name = 'database_server.option.batch_sync'
    allow_methods = ('PATCH', )
    resource = dashboard_api.OptionManageResourceApi


class DatabaseServerPanelManageController(CollectionController):
    name = 'database_server.panel'
    allow_methods = ('GET', 'POST')
    resource = dashboard_api.PanelManageResourceApi


class DatabaseServerPanelItemManageController(ItemController):
    name = 'database_server.panel.item'
    allow_methods = ('GET', 'PATCH', 'DELETE')
    resource = dashboard_api.PanelManageResourceApi


class DatabaseServerPanelBatchSyncManageController(ResourceInterface):
    name = 'database_server.panel.batch_sync'
    allow_methods = ('PATCH', )
    resource = dashboard_api.PanelManageResourceApi


class DatabaseServerSearchManageController(CollectionController):
    name = 'database_server.search'
    allow_methods = ('GET', 'POST')
    resource = dashboard_api.SearchManageResourceApi


class DatabaseServerSearchItemManageController(ItemController):
    name = 'database_server.search.item'
    allow_methods = ('GET', 'PATCH', 'DELETE')
    resource = dashboard_api.SearchManageResourceApi


class DatabaseServerSearchBatchSyncManageController(ResourceInterface):
    name = 'database_server.search.batch_sync'
    allow_methods = ('PATCH', )
    resource = dashboard_api.SearchManageResourceApi


class DatabaseServerTmpGraphManageController(CollectionController):
    name = 'database_server.tmp_graph'
    allow_methods = ('GET', 'POST')
    resource = dashboard_api.TmpGraphManageResourceApi


class DatabaseServerTmpGraphItemManageController(ItemController):
    name = 'database_server.tmp_graph.item'
    allow_methods = ('GET', 'PATCH', 'DELETE')
    resource = dashboard_api.TmpGraphManageResourceApi


class DatabaseServerTmpGraphBatchSyncManageController(ResourceInterface):
    name = 'database_server.tmp_graph.batch_sync'
    allow_methods = ('PATCH', )
    resource = dashboard_api.TmpGraphManageResourceApi
