# coding: utf-8
from monitor.apps.database_server.api import graph_api
from monitor.common.controller import CollectionController, ItemController, ResourceInterface


class DatabaseServerCounterTextManageController(CollectionController):
    name = 'database_server.counter_text'
    allow_methods = ('GET', 'POST')
    resource = graph_api.CounterTextManageResourceApi


class DatabaseServerCounterTextItemManageController(ItemController):
    name = 'database_server.counter_text.item'
    allow_methods = ('GET', 'PATCH', 'DELETE')
    resource = graph_api.CounterTextManageResourceApi


class DatabaseServerCounterTextBatchSyncManageController(ResourceInterface):
    name = 'database_server.counter_text.batch_sync'
    allow_methods = ('PATCH', )
    resource = graph_api.CounterTextManageResourceApi


class DatabaseServerEndpointManageController(CollectionController):
    name = 'database_server.endpoint'
    allow_methods = ('GET', 'POST')
    resource = graph_api.EndpointManageResourceApi


class DatabaseServerEndpointItemManageController(ItemController):
    name = 'database_server.endpoint.item'
    allow_methods = ('GET', 'PATCH', 'DELETE')
    resource = graph_api.EndpointManageResourceApi
    
    
class DatabaseServerEndpointBatchSyncManageController(ResourceInterface):
    name = 'database_server.endpoint.batch_sync'
    allow_methods = ('PATCH', )
    resource = graph_api.EndpointManageResourceApi


class DatabaseServerEndpointCounterManageController(CollectionController):
    name = 'database_server.endpoint_counter'
    allow_methods = ('GET', 'POST')
    resource = graph_api.EndpointCounterManageResourceApi


class DatabaseServerEndpointCounterItemManageController(ItemController):
    name = 'database_server.endpoint_counter.item'
    allow_methods = ('GET', 'PATCH', 'DELETE')
    resource = graph_api.EndpointCounterManageResourceApi


class DatabaseServerEndpointCounterBatchSyncManageController(ResourceInterface):
    name = 'database_server.endpoint_counter.batch_sync'
    allow_methods = ('PATCH', )
    resource = graph_api.EndpointCounterManageResourceApi


class DatabaseServerTagEndpointManageController(CollectionController):
    name = 'database_server.tag_endpoint'
    allow_methods = ('GET', 'POST')
    resource = graph_api.TagEndpointManageResourceApi


class DatabaseServerTagEndpointItemManageController(ItemController):
    name = 'database_server.tag_endpoint.item'
    allow_methods = ('GET', 'PATCH', 'DELETE')
    resource = graph_api.TagEndpointManageResourceApi


class DatabaseServerTagEndpointBatchSyncManageController(ResourceInterface):
    name = 'database_server.tag_endpoint.batch_sync'
    allow_methods = ('PATCH', )
    resource = graph_api.TagEndpointManageResourceApi
