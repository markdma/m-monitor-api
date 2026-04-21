# coding: utf-8
from __future__ import absolute_import

import datetime
import logging

from sqlalchemy import and_

from monitor.apps.alert.dbresources.resource import TPLManageResource, ServiceCatalogResource
from monitor.core.falcon_api_service import FalconApiService
from monitor.db import models, pool
from monitor.db.crud import ResourceBase
from monitor.db.models import CmdbCbs, DiskResourceCapacity, CapacityAvailableZone

LOG = logging.getLogger(__name__)


class HostReportResource(ResourceBase):
    orm_meta = models.HostReport
    _default_order = ['-created_date']
    _primary_keys = 'id'

    def _before_create(self, resource, validate):
        resource["created_date"] = datetime.datetime.now()


class AvailableZoneResource(ResourceBase):
    orm_meta = models.AvailableZone
    _default_order = ['-created_date']
    _primary_keys = 'id'


class RegionResource(ResourceBase):
    orm_meta = models.Region
    _default_order = ['-create_time']
    _primary_keys = 'id'


class HostResourceCapacityResource(ResourceBase):
    orm_meta = models.HostResourceCapacity
    _default_order = ['-f_date_time']
    _primary_keys = 'f_id'


class HostResourceCapacityWeekResource(ResourceBase):
    orm_meta = models.HostResourceCapacityWeek
    _default_order = ['-f_date_time']
    _primary_keys = 'f_id'


class HostResourceCapacityMonthResource(ResourceBase):
    orm_meta = models.HostResourceCapacityMonth
    _default_order = ['-f_date_time']
    _primary_keys = 'f_id'


class HostResourceCapacityLastDaysResource(ResourceBase):
    orm_meta = models.HostResourceCapacityLastDays
    _default_order = ['-f_date_time']
    _primary_keys = 'f_id'


class NetLineResourceCapacityResource(ResourceBase):
    orm_meta = models.NetLineResourceCapacity
    _default_order = ['-f_date_time', '-f_name']
    _primary_keys = 'f_id'


class NetLineResourceCapacityWeekResource(ResourceBase):
    orm_meta = models.NetLineResourceCapacityWeek
    _default_order = ['-f_date_time', '-f_name']
    _primary_keys = 'f_id'


class CapacityMetricResource(ResourceBase):
    orm_meta = models.CapacityMetric
    _default_order = ['-create_time']
    _primary_keys = 'f_id'


class CsapacityStrategyTreeRouteResource(ResourceBase):
    orm_meta = models.CsapacityStrategyTreeRoute
    _default_order = ['-id']
    _primary_keys = 'id'


class CapacityMetricFilterStrategyResource(ResourceBase):
    orm_meta = models.CapacityMetricFilterStrategy
    _default_order = ['-f_create_time']
    _primary_keys = 'f_id'


class ProjectResource(ResourceBase):
    orm_meta = models.Project
    _default_order = ['-name']
    _primary_keys = 'id'
    _soft_del_flag = {'is_deleted': 1}
    _soft_delete = True
    falcon_api = FalconApiService()

    def get_project_info(self, project_id):
        """
        根据project_id获取租户信息
        :param project_id:
        :return: dict
        """
        try:
            project_info = self.falcon_api.get_project_info(project_id)
            if not project_info:
                LOG.error("get project(%s) info is None" % project_id)
            return project_info
        except Exception as e:
            LOG.error("get project(%s) info failed(%s)" % (project_id, e))
            return {}

    def _addtional_create(self, session, resource, created):
        """
        创建默认项目模板
        :param session:
        :param resource:
        :param created:
        :return:
        """
        project_id = created.get("id")
        tenant_info = created.get("tenant") or {}
        tenant_id = tenant_info.get("uuid") or ""
        tenant_name = tenant_info.get("name")
        # 1.获取项目信息
        project_info = self.get_project_info(project_id)
        create_user = project_info.get("user") or {}
        user_id = create_user.get("id")
        project_name = project_info.get("name")
        # 2.获取服务目录信息
        asset_list = ServiceCatalogResource().list()
        asset_dict = {i.get("id"): i.get("name") for i in asset_list}
        tpl_resource = TPLManageResource()
        # 3.获取所有租户下所有租户级模板
        tenant_tpl_list = tpl_resource.list(filters={
            "tenant_id": tenant_id, "project_id": tenant_id, "asset_id": asset_dict.keys()
        })
        if not tenant_tpl_list:
            LOG.error("tenant_tpl tenant_id(%s) asset_id(%s) is None" % (tenant_id, asset_dict.keys()))
            return
        tenant_tpl_id = [(i.get("asset_id"), i.get("id")) for i in tenant_tpl_list]
        for i in tenant_tpl_id:
            try:
                asset_id = i[0]
                asset_name = asset_dict.get(asset_id)
                tpl_item = dict()
                tpl_item["create_user"] = user_id
                tpl_item["tenant_id"] = tenant_id
                tpl_item["project_id"] = project_id
                tpl_item["asset_id"] = asset_id
                tpl_item["parent_id"] = i[1]
                if not project_name:
                    project_name = project_id
                if not tenant_name:
                    tenant_name = tenant_id
                if not asset_name:
                    asset_name = asset_id
                tpl_item["tpl_name"] = "%s的%s项目模板" % (asset_name, project_name)
                # todo
                tpl_resource.create(tpl_item)
            except Exception as e:
                LOG.error("create asset_id(%s) tenant tpl failed(%s)" % (i, e))

    def _addtional_delete(self, session, resource):
        """
        删除默认租户模板
        :param session:
        :param resource:
        :return:
        """
        if not isinstance(resource, dict):
            return
        project_id = resource.get("id")
        # 获取服务目录信息
        asset_list = ServiceCatalogResource().list()
        asset_id_list = [i.get("id") for i in asset_list]
        tpl_resource = TPLManageResource()
        tpl_list = tpl_resource.list(filters={
            "asset_id": asset_id_list, "project_id": project_id
        })
        for i in tpl_list:
            # todo
            tpl_resource.delete(i.get("id"))


class TenantResource(ResourceBase):
    orm_meta = models.Tenant
    _default_order = ['-name']
    _primary_keys = 'uuid'
    falcon_api = FalconApiService()

    def get_tenant_info(self, tenant_id):
        """
        根据tenant_id获取租户信息
        :param tenant_id:
        :return: dict
        """
        try:
            tenant_info = self.falcon_api.get_tenant_info(tenant_id)
            if not tenant_info:
                LOG.error("get tenant(%s) info is None" % tenant_id)
            return tenant_info
        except Exception as e:
            LOG.error("get tenant(%s) info failed(%s)" % (tenant_id, e))
            return {}

    def _addtional_create(self, session, resource, created):
        """
        创建默认租户模板
        :param session:
        :param resource:
        :param created:
        :return:
        """
        tenant_id = resource.get("uuid")
        # 1.获取租户信息
        tenant_info = self.get_tenant_info(tenant_id)
        create_user = tenant_info.get("create_user_id")
        tenant_name = tenant_info.get("name")
        # 2.获取服务目录信息
        asset_list = ServiceCatalogResource().list()
        asset_dict = {i.get("id"): i.get("name") for i in asset_list}
        tpl_resource = TPLManageResource()
        # 3.获取所有产品级模板
        asset_tpl_list = tpl_resource.list(filters={
            "tenant_id": "*", "project_id": "*", "asset_id": asset_dict.keys()
        })
        if not asset_tpl_list:
            LOG.error("asset_tpl asset_id(%s) is None" % asset_dict.keys())
            return
        asset_tpl_id = [(i.get("asset_id"), i.get("id")) for i in asset_tpl_list]
        for i in asset_tpl_id:
            try:
                asset_id = i[0]
                asset_name = asset_dict.get(asset_id)
                tpl_item = dict()
                tpl_item["create_user"] = create_user
                tpl_item["tenant_id"] = tenant_id
                tpl_item["project_id"] = tenant_id
                tpl_item["asset_id"] = asset_id
                tpl_item["parent_id"] = i[1]
                if not tenant_name:
                    tenant_name = tenant_id
                if not asset_name:
                    asset_name = asset_id
                tpl_item["tpl_name"] = "%s的%s租户模板" % (asset_name, tenant_name)
                # todo
                tpl_resource.create(tpl_item)
            except Exception as e:
                LOG.error("create asset_id(%s) tenant tpl failed(%s)" % (i, e))

    def _addtional_delete(self, session, resource):
        """
        删除默认租户模板
        :param session:
        :param resource:
        :return:
        """
        if not isinstance(resource, dict):
            return
        tenant_id = resource.get("uuid")
        # 获取服务目录信息
        asset_list = ServiceCatalogResource().list()
        asset_id_list = [i.get("id") for i in asset_list]
        tpl_resource = TPLManageResource()
        tpl_list = tpl_resource.list(filters={
            "asset_id": asset_id_list, "tenant_id": tenant_id, "project_id": tenant_id
        })
        for i in tpl_list:
            # todo
            tpl_resource.delete(i.get("id"))


class DatabaseResourceCapacityResource(ResourceBase):
    orm_meta = models.DatabaseResourceCapacity
    _default_order = ['-f_date_time']
    _primary_keys = 'f_id'


class DatabaseResourceCapacityWeekResource(ResourceBase):
    orm_meta = models.DatabaseResourceWeekCapacity
    _default_order = ['-f_date_time']
    _primary_keys = 'f_id'


class DatabaseResourceCapacityMonthResource(ResourceBase):
    orm_meta = models.DatabaseResourceMonthCapacity
    _default_order = ['-f_date_time']
    _primary_keys = 'f_id'


class DiskResourceCapacityResource(ResourceBase):
    orm_meta = models.DiskResourceCapacity
    orm_pool = pool.POOLS.capacity
    _default_order = ['-timestamp']
    _primary_keys = 'id'

    def select_stat_statistic(self, filters):
        category = filters.pop("category")
        timestamp_lte = filters.pop("timestamp_lte")
        timestamp_gte = filters.pop("timestamp_gte")
        if not all([category, timestamp_lte, timestamp_gte]):
            where_sql = " AND 1!=1"
        else:
            where_sql = " AND t1.category = '%s'" % category
            for key, value in filters.items():
                if key == "$or" and isinstance(value, list):
                    tmp = []
                    for item in value:
                        if isinstance(item,dict):
                            for k,v in item.items():
                                k = k.replace("cmdb_cbs", "t2")
                                if len(value) == 1:
                                    tmp.append(k + " = '%s'" % str(value[0]))
                                else:
                                    tmp.append(key + " in " + str(value))
                    if tmp:
                        or_str_sql = " OR ".join(tmp)
                        where_sql += " (" + or_str_sql + ")"
                    continue
                if isinstance(value, list):
                    value = tuple(value)
                    if not value:
                        where_sql += " AND 1!=1"
                        break
                    else:
                        # 判断长度
                        key = key.replace("cmdb_cbs", "t2")
                        if len(value) == 1:
                            where_sql += " AND " + key + " = '%s'" % str(value[0])
                        else:
                            where_sql += " AND " + key + " in " + str(value)
                else:
                    where_sql += " AND t1." + key + " = '%s' " % value
            where_sql += " AND t1.datetime >= STR_TO_DATE('" + timestamp_gte + "','%Y-%m-%d')" + \
                         " AND t1.datetime < STR_TO_DATE('" + timestamp_lte + "','%Y-%m-%d')"
        execute_sql = r"""SELECT disk_io_util_p95,
        disk_io_write_requests_p95, 
        disk_io_read_requests_p95 
        FROM capacity.cbs AS t1 JOIN falcon_portal.cmdb_cbs AS t2 ON t1.cbs_id = t2.id 
        WHERE 1 = 1 %s;""" % where_sql
        try:
            with self.transaction() as session:
                ret = session.execute(execute_sql)
                return ret
        except Exception as e:
            logging.error("disk select failed: %s", e)
            return []

    def select_stat_with_tenant_project(self, filters, offset, limit, orders, filters_dict):
        with self.get_session() as session:
            datetime = filters["datetime"]
            query = session.query(self.orm_meta).join(CmdbCbs, CmdbCbs.id == DiskResourceCapacity.cbs_id).filter \
                (and_(DiskResourceCapacity.datetime >= datetime["gte"],
                      DiskResourceCapacity.datetime <= datetime["lte"],
                      DiskResourceCapacity.category == filters["category"]))
            if filters.get("tenant_id", None) is not None:
                query = query.filter(CmdbCbs.tenant_id.in_(filters["tenant_id"]))
            if filters.get("project_id", None) is not None:
                query = query.filter(CmdbCbs.project_id.in_(filters["project_id"]))
            if filters.get("cmdb_cbs.name", None):
                cbs_name = filters["cmdb_cbs.name"].get("ilike")
                if cbs_name:
                    query = query.filter(CmdbCbs.name.ilike(cbs_name))
            if filters.get("t_if_region", None) is not None:
                query = query.join(CapacityAvailableZone, CmdbCbs.az_id == CapacityAvailableZone.id)
                query = query.filter(CapacityAvailableZone.region_id.in_(filters["t_if_region"]))
            if filters.get("az_id"):
                query = query.filter(CmdbCbs.az_id.in_(filters["az_id"]))
            if filters.get("cmdb_cbs.status"):
                query = query.filter(CmdbCbs.status.__eq__(filters.get("cmdb_cbs.status")))
            count = self._apply_filters(query, DiskResourceCapacity, filters=filters_dict).count()
            query = self._apply_filters(query, DiskResourceCapacity, filters=filters_dict, orders=orders).offset(
                offset).limit(limit)
            results = [rec.to_dict() for rec in query]
            return count, results


class CephResourceCapacityResource(ResourceBase):
    orm_meta = models.CephResourceCapacity
    orm_pool = pool.POOLS.capacity
    _default_order = ['-timestamp']
    _primary_keys = 'id'
