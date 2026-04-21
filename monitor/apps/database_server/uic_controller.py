# coding: utf-8
from monitor.apps.database_server.api import uic_api
from monitor.common.controller import CollectionController, ItemController, ResourceInterface


class DatabaseServerSessionManageController(CollectionController):
    name = 'database_server.session'
    allow_methods = ('GET', 'POST')
    resource = uic_api.SessionManageResourceApi


class DatabaseServerSessionItemManageController(ItemController):
    name = 'database_server.session.item'
    allow_methods = ('GET', 'PATCH', 'DELETE')
    resource = uic_api.SessionManageResourceApi


class DatabaseServerSessionBatchSyncManageController(ResourceInterface):
    name = 'database_server.session.batch_sync'
    allow_methods = ('PATCH',)
    resource = uic_api.SessionManageResourceApi


class DatabaseServerUserManageController(CollectionController):
    name = 'database_server.user'
    allow_methods = ('GET', 'POST')
    resource = uic_api.UserManageResourceApi


class DatabaseServerUserItemManageController(ItemController):
    name = 'database_server.user.item'
    allow_methods = ('GET', 'PATCH', 'DELETE')
    resource = uic_api.UserManageResourceApi


class DatabaseServerUserBatchSyncManageController(ResourceInterface):
    name = 'database_server.user.batch_sync'
    allow_methods = ('PATCH',)
    resource = uic_api.UserManageResourceApi
