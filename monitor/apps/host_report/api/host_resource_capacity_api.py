# coding: utf-8
from __future__ import absolute_import

from monitor.apps.host_report.dbresources import resource


class HostResourceCapacityApi(resource.HostResourceCapacityResource):

    def _base_select_sql(self, sql, params):
        """
        根据params返回查询数据
        :param params: type list
        :return: type dict
        """
        with self.get_session() as session:
            where_sql = ""
            params = list(set(params))  # 去重
            if len(params) == 1:
                where_sql = "='%s'" % params[0]
            elif len(params) > 1:
                where_sql = "IN %s" % str(tuple(params))
            if where_sql:
                sql_result = session.execute(sql % where_sql)
                return {i[0]: i[1] for i in sql_result if i[1]}
            else:
                return {}

    def get_hostname_by_uuid(self, uuids):
        """
        根据uuid返回的hostname
        :param uuids: type list
        :return: type dict
        """
        if not uuids:
            return {}
        sql = "SELECT uuid, hostname FROM falcon_portal.cmdb_host WHERE uuid %s;"
        return self._base_select_sql(sql, uuids)


class HostResourceCapacityWeekApi(resource.HostResourceCapacityWeekResource):
    pass


class HostResourceCapacityMonthApi(resource.HostResourceCapacityMonthResource):

    def select_host_data(self, select_fields=None, filters=None):
        where_sql = ""
        if filters and isinstance(filters, dict):
            for key, value in filters.items():
                where_sql += " AND " + key + " = '%s' " % value
        sql_select_fields = '*'
        if isinstance(select_fields, list):
            sql_select_fields = ','.join(select_fields)

        execute_sql = r"""SELECT %s 
        FROM host_resource_capacity_last_days
        WHERE 1 = 1 %s;""" % (sql_select_fields, where_sql)
        with self.get_session() as session:
            ret = session.execute(execute_sql)
        return ret


class HostResourceCapacityLastDaysApi(resource.HostResourceCapacityLastDaysResource):
    def select_host_data(self, select_fields=None, filters=None, admin=True):
        where_sql = ""
        flag = False
        if "f_project_id" in filters and "f_tenant_id" in filters and admin:  # 管理门户
            # 租户和项目都在 则取并集
            f_project_id = filters.pop("f_project_id")
            f_tenant_id = filters.pop("f_tenant_id")
            if isinstance(f_project_id, list) and isinstance(f_tenant_id, list):
                p_in_tmp = "f_project_id IN " + str(tuple(f_project_id))
                t_in_tmp = "f_tenant_id IN" + str(tuple(f_tenant_id))
                # 判断是否是空数组
                if f_tenant_id and f_project_id:
                    if len(f_tenant_id) == 1 and len(f_project_id) == 1:
                        where_sql += " AND " + "(%s OR %s)" % ("f_project_id = '%s'" % str(f_project_id[0]),
                                                               "f_tenant_id = '%s'" % str(f_tenant_id[0]))
                    elif len(f_project_id) == 1:
                        where_sql += " AND " + "(%s OR %s)" % ("f_project_id = '%s'" % str(f_project_id[0]), t_in_tmp)
                    elif len(f_tenant_id) == 1:
                        where_sql += " AND " + "(%s OR %s)" % (p_in_tmp, "f_tenant_id = '%s'" % str(f_tenant_id[0]))
                    else:
                        where_sql += " AND " + "(%s OR %s)" % (p_in_tmp, t_in_tmp)
                elif not f_tenant_id:
                    if len(f_project_id) == 1:
                        where_sql += " AND " + "f_project_id = '%s'" % str(f_project_id[0])
                    elif f_project_id:
                        where_sql += " AND " + p_in_tmp
                    elif not f_project_id:
                        where_sql += " AND 1!=1"
                        flag = True
                elif not f_project_id:
                    if len(f_tenant_id) == 1:
                        where_sql += " AND " + "f_tenant_id = '%s'" % str(f_tenant_id[0])
                    else:
                        where_sql += " AND " + t_in_tmp
                else:
                    where_sql += " AND 1!=1"
                    flag = True

        # 如果已经1!=1 则不用继续拼接sql
        if not flag:
            for key, value in filters.items():
                if isinstance(value, list):
                    value = tuple(value)
                    if not value:
                        where_sql += " AND 1!=1"
                        break
                    else:
                        # 判断长度
                        if len(value) == 1:
                            where_sql += " AND " + key + " = '%s'" % str(value[0])
                        else:
                            where_sql += " AND " + key + " in " + str(value)
                else:
                    where_sql += " AND " + key + " = '%s' " % value
        sql_select_fields = '*'
        if isinstance(select_fields, list):
            sql_select_fields = ','.join(select_fields)

        execute_sql = r"""SELECT %s 
                FROM host_resource_capacity_last_days
                WHERE 1 = 1 %s;""" % (sql_select_fields, where_sql)
        with self.get_session() as session:
            ret = session.execute(execute_sql)
        return ret
