# coding: utf-8
from __future__ import absolute_import
from monitor.apps.audit.audit_controller import AuditStatisticsController, AuditHostController, \
    AuditDatabaseController, AuditNetworkController, AuditNetlineController


def add_routes(api):
    api.add_route('/v1/audit/audit_statistics', AuditStatisticsController())
    api.add_route('/v1/audit/host', AuditHostController())
    api.add_route('/v1/audit/database', AuditDatabaseController())
    api.add_route('/v1/audit/network', AuditNetworkController())
    api.add_route('/v1/audit/netline', AuditNetlineController())
