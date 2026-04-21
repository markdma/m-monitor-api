# coding: utf-8
from __future__ import absolute_import

import datetime
from monitor.db.crud import ResourceBase
from monitor.db.models import AuditStatistics, AuditHost, AuditDatabase, AuditNetwork, AuditNetline
import logging

LOG = logging.getLogger(__name__)


class AuditStatisticsResource(ResourceBase):
    orm_meta = AuditStatistics
    _primary_keys = 'type,date_time'


class AuditBaseResource(ResourceBase):

    def list(self, filters=None, orders=None, offset=None, limit=None, hooks=None):
        result = super(AuditBaseResource, self).list(filters, orders, offset, limit, hooks)
        # 如果没有数据 尝试获取前一天的
        if not result:
            now_time = datetime.datetime.now()
            yesterday_date = (now_time + datetime.timedelta(days=-1)).strftime("%Y-%m-%d")
            filters["date_time"] = yesterday_date
            result = super(AuditBaseResource, self).list(filters, orders, offset, limit, hooks)
        return result

    def get_datas_by_keys(self, table_name, where_fields, key_value):
        """
        根据获取主键key获取对应表中的数据
        :param table_name: 表名
        :param where_fields: 返回字段 list
        :param key_value: 过滤条件 dict
        :return: list
        """
        with self.get_session() as session:
            base_sql = "SELECT %s FROM %s WHERE " % (",".join(where_fields), table_name)
            key = key_value.keys()[0]  # todo
            keys_data = key_value.values()[0]
            keys_count = len(keys_data)
            where_sql = ""
            if keys_count == 1:
                where_sql = "%s = '%s'" % (key, keys_data[0])
            elif keys_count > 1:
                where_sql = "%s IN %s" % (key, str(tuple(keys_data)))
            if where_sql:
                sql = base_sql + where_sql
                result = session.execute(sql)
                return result
            return []

    @staticmethod
    def audit_statistics_list(audit_type, date_time, pop_fields=None):
        """
        获取对应资源类型的审计异常统计数据
        :param audit_type: 资源类型
        :param date_time: 当天日期
        :param pop_fields: 去除字段
        :return: list
        """
        res_list = AuditStatisticsResource().list(filters={"type": audit_type, "date_time": date_time})
        # 如果此时没有当天的审计统计数据 获取前一天的
        if not res_list:
            now_time = datetime.datetime.now()
            yesterday_date = (now_time + datetime.timedelta(days=-1)).strftime("%Y-%m-%d")
            res_list = AuditStatisticsResource().list(filters={"type": audit_type, "date_time": yesterday_date})
        if pop_fields:
            for i in res_list:
                for k in pop_fields:
                    i.pop(k, None)
        return res_list


class AuditHostResource(AuditBaseResource):
    orm_meta = AuditHost
    _primary_keys = 'uuid,date_time,status'

    def list(self, filters=None, orders=None, offset=None, limit=None, hooks=None):
        result = super(AuditHostResource, self).list(filters, orders, offset, limit, hooks)
        where_fields = ["uuid", "hostname", "ip", "env_type", "os_platform", "os", "enabled", "state", "os_type"]
        cmdb_host_uuid = {"uuid": [i["uuid"] for i in result]}
        cmdb_host_result = self.get_datas_by_keys("falcon_portal.cmdb_host", where_fields, cmdb_host_uuid)
        cmdb_host_dict = {i[0]: i for i in cmdb_host_result}
        for i in result:
            uuid = i["uuid"]
            info = cmdb_host_dict.get(uuid)
            if not info:
                for index, field in enumerate(where_fields):
                    i[field] = info[index]
            else:
                for index, field in enumerate(where_fields):
                    i[field] = ""
        return result


class AuditDatabaseResource(AuditBaseResource):
    orm_meta = AuditDatabase
    _primary_keys = 'id,date_time,status'

    def list(self, filters=None, orders=None, offset=None, limit=None, hooks=None):
        result = super(AuditDatabaseResource, self).list(filters, orders, offset, limit, hooks)
        cmdb_db_node_where_fields = ["id", "state", "server_ip", "server_port", "role", "enabled"]  # 节点
        tmp_list1 = tmp_list2 = tmp_list3 = []
        for i in result:
            # todo 此处暂时使用id作为cmdb_db_instance唯一键 后续使用node_id
            tmp_list1.append(i["id"])
            tmp_list2.append(i["db_uuid"])
            tmp_list3.append(i["host_uuid"])
        cmdb_db_instance_id = {"id": tmp_list1}
        cmdb_db_instance_result = self.get_datas_by_keys("falcon_portal.cmdb_db_instance",
                                                         cmdb_db_node_where_fields, cmdb_db_instance_id)

        cmdb_db_where_fields = ["uuid", "name", "type", "state"]  # 数据库
        cmdb_db_uuid = {"uuid": tmp_list2}
        cmdb_db_result = self.get_datas_by_keys("falcon_portal.cmdb_db", cmdb_db_where_fields, cmdb_db_uuid)

        cmdb_host_where_fields = ["uuid", "env_type", "state"]  # 主机
        cmdb_host_uuid = {"uuid": tmp_list3}
        cmdb_host_result = self.get_datas_by_keys("falcon_portal.cmdb_host", cmdb_host_where_fields, cmdb_host_uuid)

        cmdb_db_node_dict = {i[0]: i for i in cmdb_db_instance_result}
        cmdb_db_dict = {i[0]: i for i in cmdb_db_result}
        cmdb_host_dict = {i[0]: i for i in cmdb_host_result}
        for i in result:
            id_ = i["id"]
            info = cmdb_db_node_dict.get(id_)
            for index, field in enumerate(cmdb_db_node_where_fields):
                i[field] = info[index]
            db_uuid = i["db_uuid"]
            db_info = cmdb_db_dict.get(db_uuid)
            if db_info:
                i["name"] = db_info[1]
                i["type"] = db_info[2]
                i["db_instance_state"] = db_info[3]
            else:
                i["name"] = ""
                i["type"] = ""
                i["db_instance_state"] = ""
            host_uuid = i["host_uuid"]
            host_info = cmdb_host_dict.get(host_uuid)
            if host_info:
                i["env_type"] = host_info[1]
                i["host_state"] = host_info[2]
            else:
                i["env_type"] = ""
                i["host_state"] = ""
        return result


class AuditNetworkResource(AuditBaseResource):
    orm_meta = AuditNetwork
    _primary_keys = 'serial_num,date_time,status'

    def list(self, filters=None, orders=None, offset=None, limit=None, hooks=None):
        result = super(AuditNetworkResource, self).list(filters, orders, offset, limit, hooks)
        where_fields = ["serial_num", "iprange", "env", "mc", "model", "catalog", "enabled",
                        "community", "snmp_port", "state"]
        serial_nums = {"serial_num": [i["serial_num"] for i in result]}
        network_result = self.get_datas_by_keys("falcon_portal.sw_iprange", where_fields, serial_nums)
        network_dict = {i[0]: i for i in network_result}
        for i in result:
            serial_num = i["serial_num"]
            info = network_dict.get(serial_num)
            if info:
                for index, field in enumerate(where_fields):
                    i[field] = info[index]
            else:
                for index, field in enumerate(where_fields):
                    i[field] = ""
        return result


class AuditNetlineResource(AuditBaseResource):
    orm_meta = AuditNetline
    _primary_keys = 'id,date_time,status'

    def list(self, filters=None, orders=None, offset=None, limit=None, hooks=None):
        result = super(AuditNetlineResource, self).list(filters, orders, offset, limit, hooks)
        where_fields = ["id", "name", "remote_address", "local_hardware_interface_name", "enabled"]
        netline_id = {"id": [i["id"] for i in result]}
        netline_result = self.get_datas_by_keys("falcon_portal.if_wan", where_fields, netline_id)
        netline_dict = {i[0]: i for i in netline_result}

        serial_nums = {"serial_num": [i["serial_num"] for i in result]}
        network_result = self.get_datas_by_keys("falcon_portal.sw_iprange", ["serial_num", "env"], serial_nums)
        network_dict = {i[0]: i for i in network_result}

        for i in result:
            id_ = i["id"]
            info = netline_dict.get(id_)
            if info:
                for index, field in enumerate(where_fields):
                    i[field] = info[index]
            else:
                for index, field in enumerate(where_fields):
                    i[field] = ""
            serial_num = i["serial_num"]
            network_info = network_dict.get(serial_num)
            if network_info:
                i["env"] = network_info[1]
            else:
                i["env"] = ""
        return result
