# coding: utf-8
from __future__ import absolute_import

from monitor.apps.host_report.dbresources import resource
import logging

LOG = logging.getLogger(__name__)


class TenantApi(resource.TenantResource):

    @property
    def default_filter(self):
        return {'is_deleted': 0}

    def get_cmdb_uuid(self, admin_uuid):
        cmdb_uuid = admin_uuid
        tenants = super(TenantApi, self).list(filters={"admin_uuid": admin_uuid})
        if len(tenants) > 0:
            cmdb_uuid = tenants[0]["uuid"]
        return cmdb_uuid

    def get_cmdb_uuid_by_list(self, tenant_list):
        # 将云管的tenant_id转化为监控的tenant_id
        tenant_info = self.list(filters={'admin_uuid': {'in': tenant_list}})
        return [i['uuid'] for i in tenant_info]

    def get_project_id_by_node_ids(self, node_ids=None, is_all=False):
        """
        根据node_ids调动falcon_api获取项目id
        :param node_ids:
        :param is_all: 全选标准层级 只获取挂载到标准层级的项目id
        :return: list
        """
        try:
            project_list = self.falcon_api.get_project_id_by_node_ids(node_ids, is_all)
            LOG.info("node_id(%s) get project_id(%s) count(%d)" % (node_ids, project_list, len(project_list)))
            return project_list
        except Exception as e:
            LOG.error("get organization project_id failed(%s)" % e)
            return []

    def get_tenant_id_by_node_ids(self, node_ids):
        """
        根据node_ids调动falcon_api获取tenant_id
        :param node_ids:
        :return: list
        """
        try:
            tenant_list = self.falcon_api.get_tenant_id_by_node_ids(node_ids)
            LOG.info("node_id(%s) get tenant_id(%s) count(%d)" % (node_ids, tenant_list, len(tenant_list)))
            return tenant_list
        except Exception as e:
            LOG.error("get tenant_id failed(%s)" % e)
            return []
