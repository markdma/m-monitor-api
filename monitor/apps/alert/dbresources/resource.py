# coding: utf-8
from __future__ import absolute_import

import copy
import datetime
import logging
import time
from uuid import uuid4

from sqlalchemy import and_

from monitor.apps.auth.dbresources.resource import UserManageResource
from monitor.apps.database_server.dbresources.resource import AlarmOtherManageResource, CustomAlertManageResource
from monitor.core import exceptions
from monitor.core.exceptions import DBError, ValidationError, NotFoundError
from monitor.core.falcon_api_service import FalconApiService
from monitor.core.i18n import _
from monitor.core.utils import get_diff_time
from monitor.db import models, pool, validator, converter
from monitor.db.crud import ResourceBase, ColumnValidator, CustomQuery
from monitor.db.models import EventCasesManage, Host, AlarmNoteManage, EventsManage, TPLManage

LOG = logging.getLogger(__name__)


class EventCasesManageResource(ResourceBase):
    orm_meta = models.EventCasesManage
    orm_pool = pool.POOLS.alarms
    _default_order = ['-timestamp']
    _primary_keys = 'id'


class MaintainCounterManageResource(ResourceBase):
    orm_meta = models.MaintainCounterManage
    _default_order = ['-id']
    _primary_keys = 'id'


class AlarmScheManageResource(ResourceBase):
    orm_meta = models.AlarmScheManage
    _default_order = ['-id']
    _primary_keys = 'id'
    _soft_del_flag = {'isenable': 1}
    _soft_delete = True

    def _before_update(self, rid, resource, validate):
        resource["optime"] = datetime.datetime.now()

    def _before_create(self, resource, validate):
        resource["optime"] = datetime.datetime.now()


class EventBaseResource(ResourceBase):

    @staticmethod
    def _get_alarm_note_info(alarm_note, status, timestamp, event_case_id):
        """
        :param alarm_note:
        :param status:
        :param timestamp:
        :param event_case_id:
        :return:
        """
        if status == 'PROBLEM':
            alarm_note_list = alarm_note.list(filters={'timestamp': {'gt': timestamp}, 'event_case_id': event_case_id})
        else:
            alarm_note_list = alarm_note.list(filters={'timestamp': {'lt': timestamp}, 'event_case_id': event_case_id})
        return alarm_note_list

    def count(self, filters=None, offset=None, limit=None, hooks=None):
        """
        获取符合条件的记录数量

        :param filters: 过滤条件
        :type filters: dict
        :param offset: 起始偏移量
        :type offset: int
        :param limit: 数量限制
        :type limit: int
        :param hooks: 钩子函数列表，函数形式为func(query, filters)
        :type hooks: list
        :returns: 数量
        :rtype: int
        """
        offset = offset or 0
        orders = []
        query = self._custom_query(filters, orders, offset, limit, hooks)
        return query.count()

    def _custom_query(self, filters=None, orders=None, offset=None, limit=None, hooks=None):
        pass


class EventCasesResource(ResourceBase):  #
    orm_meta = EventCasesManage
    _default_order = ['-update_at']
    _primary_keys = 'id'
    custom_alert = CustomAlertManageResource()

    def count(self, filters=None, offset=None, limit=None, hooks=None):
        """
        获取符合条件的记录数量

        :param filters: 过滤条件
        :type filters: dict
        :param offset: 起始偏移量
        :type offset: int
        :param limit: 数量限制
        :type limit: int
        :param hooks: 钩子函数列表，函数形式为func(query, filters)
        :type hooks: list
        :returns: 数量
        :rtype: int
        """
        offset = offset or 0
        orders = []
        query = self._custom_query(filters, orders, offset, limit, hooks)
        return query.count()

    @staticmethod
    def _get_alarm_note_info(alarm_note, status, timestamp, event_case_id):
        """
        :param alarm_note:
        :param status:
        :param timestamp:
        :param event_case_id:
        :return:
        """
        if status == 'PROBLEM':
            alarm_note_list = alarm_note.list(filters={'timestamp': {'gt': timestamp}, 'event_case_id': event_case_id})
        else:
            alarm_note_list = alarm_note.list(filters={'timestamp': {'lt': timestamp}, 'event_case_id': event_case_id})
        return alarm_note_list

    def _custom_query(self, filters=None, orders=None, offset=None, limit=None, hooks=None):
        """
        自定query查询语句
        :param filters:
        :param orders:
        :param offset:
        :param limit:
        :param hooks:
        :return:
        """
        with self.get_session() as session:
            start_time = filters.get('start_time', '')
            end_time = filters.get('end_time', '')
            query = self._get_query(session, filters=filters, orders=orders)

            # 自定义过滤条件
            if start_time and end_time:
                query = query.filter(self.orm_meta.endpoint == Host.hostname,
                                     self.orm_meta.update_at.between(start_time, end_time))
            else:
                query = query.filter(self.orm_meta.endpoint == Host.hostname)

            if hooks:
                for h in hooks:
                    query = h(query, filters)
            query = self._addtional_list(query, filters)
            if offset:
                query = query.offset(offset)
            if limit is not None:
                query = query.limit(limit)
            return query

    def list(self, filters=None, orders=None, offset=None, limit=None, hooks=None):
        offset = offset or 0
        query = self._custom_query(filters, orders, offset, limit, hooks)
        results = []
        alarm_other_list = AlarmOtherManageResource().list()
        alarm_note = AlarmNoteResource()
        now = datetime.datetime.now()
        for rec in query:
            item = rec.to_dict()
            res = {}
            try:
                # 发生时间取update_at
                update_at = item.get('update_at')
                res['update_at'] = update_at
                res['last_time'] = get_diff_time(update_at, now)
                item.pop('timestamp', None)
                # 级别
                priority = int(item.pop('priority', 2))
                if priority == 0:
                    res['priority'] = "高"
                elif priority == 1:
                    res['priority'] = "中"
                else:
                    res['priority'] = "低"
                # 主机信息
                host_info = item.pop('host_info', None)
                # host不存在处理
                res['ip'] = host_info.get('ip') if host_info else ''
                res['exthostname'] = host_info.get('exthostname') if host_info else ''
                # 应用
                cmdb_sys = item.pop('cmdb_sys', None)
                res['app'] = res['stack'] = res['system'] = ''
                if cmdb_sys:
                    cmdb_sys = cmdb_sys[0]
                    res['app'] = cmdb_sys.get('app')
                    res['stack'] = cmdb_sys.get('stack')
                    res['system'] = cmdb_sys.get('system')
                # 指标
                metric = item.get('metric', '')
                metrict = metric.split("/")[0]
                note = item.get('note', '')
                metricm = metrict
                # 指标信息 othermsg
                tags = metric.replace(metricm + "/", "")
                if tags == metricm:
                    tags = ""
                for c in alarm_other_list:
                    c_metric = c.get('metric', '')
                    if not c_metric or c_metric != metricm:
                        continue
                    v_key = c.get('s_tag')
                    v_value = ""
                    for cc in tags.split(','):
                        if v_key in cc and v_key:
                            v_value = cc.replace(v_key + "=", "")

                    tags = c.get('s_name') + ":" + v_value
                if note != "":
                    metricm = note + "(" + metricm + ")"
                # 指标
                res['metric_display'] = metricm
                res['metrict'] = metrict
                res['othermsg'] = tags
                res['max_step'] = item.get('max_step', '')  # 用于删除告警
                res['cond'] = item.get('cond', '')
                # 告警值 1 > 1
                cond = item.get('cond', '')
                cond_list = cond.split(' ')
                current_value = cond_list[0]
                set_value = cond_list[2]
                if '.' in current_value:
                    res['current_value'] = '%.2f' % float(current_value)
                else:
                    res['current_value'] = current_value
                if '.' in current_value:
                    res['set_value'] = cond_list[1] + '%.2f' % float(set_value)
                else:
                    res['set_value'] = cond_list[1] + set_value
                # 可用区
                res['az'] = item.get('az', None)
                res['project'] = item.get('project', None)
                res['tenant'] = item.get('tenant', None)
                res['endpoint'] = item.get('endpoint', '')
                res['source_type'] = item.get('source_type', '')
                res['id'] = item.get('id', '')
                # 处理
                operation = self._get_alarm_note_info(alarm_note, filters.get('status'), update_at, res['id'])
                res['operation'] = 0
                if operation:
                    res['operation'] = 1
                results.append(res)
            except AttributeError or KeyError or ValueError as e:
                LOG.error("get event cases data(%s) error(%s)" % (item, e))
                continue
            except TypeError as e:
                LOG.error("get event cases data(%s) error(%s)" % (item, e))
                continue

        return results

    def delete_alarm(self, resource):
        """
        删除告警
        :param resource:
        :return:
        """
        no_exist = 0
        failed_count = 0
        check_flag = False  # 是否权限验证
        ids = resource.get("ids") or []
        msg = resource.get("msg")
        create_user = resource.get("create_user")

        alarm_ids = [alarm_id for alarm_id in ids if "custom_" not in alarm_id]
        alarm_info = custom_info = {}
        custom_ids = [custom_id.split("_")[1] for custom_id in ids
                      if "custom_" in custom_id and custom_id.split("_")[1] != ""]
        if alarm_ids:
            alarm_list = self.list(filters={"id": {"in": alarm_ids}})
            alarm_info = {item.get("id"): item for item in alarm_list}
            # 只有一条时 会直接抛出403 批量操作时 没有权限的告警只加入到失败msg
            if len(alarm_list) == 1:
                project = alarm_list[0].get("project") or {}
                tenant = alarm_list[0].get("tenant") or {}
                self.check_user_operate(create_user, project.get("id"), tenant.get("uuid"))
                check_flag = True
        if custom_ids:
            custom_list = self.custom_alert.list(filters={"id": {"in": custom_ids}})
            custom_info = {item.get("id"): item for item in custom_list}

        timestamp = datetime.datetime.now()
        for event_id in ids:  # 为保持原有业务 此处是循环执行insert插入
            # 获取session 此session已经开启事物 会自动commit rollback
            try:
                with self.transaction() as session:
                    # session.begin()
                    # 自定义告警
                    if "custom_" in event_id:
                        # id-> custom_id查找custom_alert表是否存在告警
                        custom_alert_id = event_id.split("_")[1]
                        if not event_id:
                            no_exist += 1
                            continue
                        custom_one = custom_info.get(custom_alert_id)
                        if not custom_one:
                            no_exist += 1
                            continue
                        # insert alarms.event_cases
                        alert_msg = custom_one.get("alert_msg") or ""
                        al_level = custom_one.get("al_level") or 0
                        event_cases_sql = r"""
                        INSERT INTO alarms.event_cases(id,endpoint,metric,cond,status,`timestamp`,priority) 
                        values ("%s", "", "%s", "0 == 0", "OK", "%s", %d);
                        """ % (event_id, alert_msg, timestamp, al_level)
                        session.execute(event_cases_sql)
                        # insert alarms.events
                        events_sql = r"""
                        INSERT INTO alarms.events(event_caseId,step,cond,status,`timestamp`) 
                        values ("%s", 0, "0 == 0", 2, "%s"); 
                        """ % (event_id, timestamp)
                        session.execute(events_sql)
                        # insert alarms.alarm_note
                        alarm_note_sql = r"""
                        INSERT INTO alarms.alarm_note(event_case_id,`timestamp`,creator,alarm_note) 
                        values ("%s", "%s", "%s", "%s");
                        """ % (event_id, timestamp, create_user, msg)
                        session.execute(alarm_note_sql)
                        # update falcon_portal.custom_alert SET is_close=TRUE
                        custome_alert_sql = r"""
                        UPDATE falcon_portal.custom_alert SET is_close=TRUE WHERE id="%s";
                        """ % event_id
                        session.execute(custome_alert_sql)
                    else:
                        # 查找event_case是否存在id
                        event_case = alarm_info.get(event_id)
                        if not event_case:
                            no_exist += 1
                            continue
                        # 权限判断
                        if not check_flag:
                            try:
                                project = event_case.get("project") or {}
                                tenant = event_case.get("tenant") or {}
                                self.check_user_operate(create_user, project.get("id"), tenant.get("uuid"))
                            except exceptions.ForbiddenError:
                                failed_count += 1
                                continue
                        else:
                            check_flag = False
                        max_step = event_case.get("max_step") or 0
                        cond = event_case.get("cond") or ""
                        # update alarms.event_cases
                        event_cases_sql = r"""
                        UPDATE alarms.event_cases set status="%s",`timestamp`="%s",update_at="%s" 
                        WHERE id="%s";
                        """ % ("DEL", timestamp, timestamp, event_id)
                        session.execute(event_cases_sql)
                        # insert alarms.events
                        events_sql = r"""
                        INSERT INTO alarms.events(event_caseId,step,cond,status,`timestamp`) 
                        values ("%s", %d, "%s", 2, "%s");
                        """ % (event_id, max_step, cond, timestamp)
                        session.execute(events_sql)
                        # insert alarms.alarm_note
                        alarm_note_sql = r"""
                        INSERT INTO alarms.alarm_note(event_case_id,`timestamp`,creator,alarm_note) 
                        values ("%s", "%s", "%s", "%s");
                        """ % (event_id, timestamp, create_user, msg)
                        session.execute(alarm_note_sql)
            except Exception as e:
                failed_count += 1
                LOG.error("delete alarm error(%s)" % e)
        success_count = len(ids) - failed_count
        if failed_count + no_exist == len(ids):
            raise exceptions.ValidationError(message=_("删除失败,请检查是否有租户项目权限!"))
        if no_exist <= 0:
            return_msg = {"msg": _("删除完成,成功%d条,失败%d条" % (success_count, failed_count))}
        else:
            return_msg = {"msg": _("删除完成,成功%d条,失败%d条,其中%d为不存在数据") %
                                 (success_count, failed_count, no_exist)}
        return return_msg


class AlarmCountResource(ResourceBase):
    orm_meta = EventCasesManage
    _default_order = ['-id']
    _primary_keys = 'id'

    @staticmethod
    def _get_event_cases_count(session, event_cases_sql, base_result):
        """
        正在告警主机个数
        :param session:
        :param event_cases_sql:
        :param base_result:
        :return: 返回正在告警的主机
        """
        result = session.execute(event_cases_sql)
        tmp_list = []
        for item in result:
            endpoint = item[0].upper()
            last_alarm_time = item[1]
            alarm_count = item[2]
            base_result[endpoint]["last_alarm_time"] = last_alarm_time
            base_result[endpoint]["alarm_count"] = alarm_count
            tmp_list.append(endpoint)
        return tmp_list

    @staticmethod
    def _get_event_count(session, event_sql, tmp_event_endpoints, base_result):
        """
        如果无正在告警 则查历史event 获取最近告警时间
        :param session:
        :param event_sql:
        :param tmp_event_endpoints:
        :param base_result:
        :return:
        """
        event_where_sql = ""
        if len(tmp_event_endpoints) == 1:
            event_where_sql = "='%s'" % tmp_event_endpoints[0]
        elif len(tmp_event_endpoints) > 1:
            event_where_sql = "IN %s" % str(tuple(tmp_event_endpoints))
        if event_where_sql:
            event_result = session.execute(event_sql % event_where_sql)
            for item in event_result:
                endpoint = item[0].upper()
                base_result[endpoint]["last_alarm_time"] = item[1]

    @staticmethod
    def _get_cmdb_host_uuid(session):
        """
        避免与云管uuid大小写不一致
        以cmdb_host表的uuid为准
        :return:
        """
        sql = "SELECT t1.uuid, t2.hostname FROM falcon_portal.cmdb_host t1 " \
              "JOIN host t2 ON t1.uuid = t2.hostname;"
        result = session.execute(sql)
        return {i[1]: i[0] for i in result}

    @staticmethod
    def _get_problem_data(session):
        sql = "SELECT endpoint FROM alarms.event_cases WHERE status = 'PROBLEM' GROUP BY endpoint;"
        result = session.execute(sql)
        return {i[0]: "" for i in result}

    def _get_alarm_count_list(self, session, event_sql, export_flag, alarm_flag=True):
        """
        查询返回有序过滤后id列表
        导出返回查询结果数据
        :param session:
        :param event_sql:
        :param export_flag: 导出标志 导出返回全部数据
        :param alarm_flag: 正在告警 和 已恢复告警
        :return:
        """
        result = session.execute(event_sql).fetchall()
        if alarm_flag:
            ids = [i[0] for i in result]
        else:
            # 再查一次 获取真正恢复的主机
            problem_dict = self._get_problem_data(session)
            ids = [i[0] for i in result if not problem_dict.get(i[0])]
        if not ids:
            return []
        ids_dict = self._get_cmdb_host_uuid(session)
        if not ids_dict:
            return []
        # 导出
        if export_flag:
            export_data = []
            if alarm_flag:
                for i in result:
                    uuid = ids_dict.get(i[0], i[0])
                    export_data.append({"id": uuid, "last_alarm_time": i[1], "alarm_count": i[2]})
                return export_data
            # 获取已恢复最后一次告警时间
            events_sql = "SELECT t1.endpoint, MAX(t2.timestamp) last_alarm_time FROM alarms.events t2 " \
                         "JOIN alarms.event_cases t1 ON t2.event_caseId = t1.id " \
                         "WHERE t2.status = 0 GROUP BY endpoint ORDER BY NULL;"
            events_result = session.execute(events_sql)
            events_dict = {i[0]: i[1] for i in events_result}
            for i in result:
                uuid = ids_dict.get(i[0], i[0])
                last_alarm_time = events_dict.get(i[0], "")
                export_data.append({"id": uuid, "last_alarm_time": last_alarm_time, "alarm_count": 0})
            return export_data

        uuids = []
        for i in ids:
            uuid = ids_dict.get(i, i)
            uuids.append(uuid)
        return uuids

    def _query_alarm_count(self, session, endpoints, event_cases_sql):
        """
        普通查询 获取告警个数和告警时间
        :param session:
        :param endpoints:
        :param event_cases_sql:
        :return:
        """
        where_sql = ""
        if isinstance(endpoints, list):
            if len(endpoints) == 1:
                where_sql = "='%s'" % endpoints[0]
            elif len(endpoints) > 1:
                where_sql = "IN %s" % str(tuple(endpoints))
        elif isinstance(endpoints, str):
            where_sql = "='%s'" % endpoints
            endpoints = [endpoints]
        if not where_sql:
            return {}
        and_endpoint = " AND endpoint "
        group_by = " GROUP BY endpoint ORDER BY NULL;"
        event_cases_sql = event_cases_sql + and_endpoint + where_sql + group_by
        # 初始化返回结果
        base_result = {i.upper(): {"id": i, "alarm_count": 0, "last_alarm_time": ""} for i in endpoints}
        # 正在告警
        tmp_list = self._get_event_cases_count(session, event_cases_sql, base_result)
        tmp_event_endpoints = [endpoint for endpoint in base_result.keys() if endpoint not in tmp_list]
        # 历史告警 时间为最后一次告警时间
        if tmp_event_endpoints:
            event_sql = "SELECT t1.endpoint, MAX(t2.timestamp) last_alarm_time FROM alarms.events t2 " \
                        "JOIN alarms.event_cases t1 ON t2.event_caseId = t1.id " \
                        "WHERE t2.status = 0 AND endpoint %s"
            event_sql = event_sql + group_by
            self._get_event_count(session, event_sql, tmp_event_endpoints, base_result)
        return {i.pop("id"): i for i in base_result.values()}

    def _query_alarm_count_slow(self, session, filters, orders, event_cases_sql, export_flag):
        """
        复杂场景 查询告警计数和告警时间
        :param session:
        :param filters:
        :param orders:
        :param event_cases_sql:
        :param export_flag:
        :return:
        """
        alarm_count = filters.get("alarm_count")
        if alarm_count:
            try:
                alarm_count = int(alarm_count)
            except ValueError as e:
                LOG.error("alarm_count: %s" % e)
                return []
        else:
            alarm_count = 1
        # 告警时间
        start_time = filters.get("last_alarm_time_start")
        end_time = filters.get("last_alarm_time_end")
        group_by = " GROUP BY endpoint"

        if start_time and end_time:
            time_sql = " HAVING last_alarm_time >= '%s' AND last_alarm_time <= '%s'" % (start_time, end_time)
            group_by += time_sql
        order_sql = ""
        if orders:
            order_dict = {
                "-alarm_count": " alarm_count DESC",
                "+alarm_count": " alarm_count ASC",
                "alarm_count": " alarm_count ASC",
                "-last_alarm_time": " last_alarm_time DESC",
                "+last_alarm_time": " last_alarm_time ASC",
                "last_alarm_time": " last_alarm_time ASC"
            }
            for field in orders:
                # 是未恢复告警 告警个数排序才有意义
                if "alarm_count" in field and not alarm_count:
                    continue
                if order_sql:
                    if order_dict.get(field):
                        order_sql = order_sql + "," + order_dict.get(field)
                else:
                    if order_dict.get(field):
                        order_sql = order_dict.get(field)
        if order_sql:
            group_by = group_by + " ORDER BY" + order_sql
        else:
            group_by += " ORDER BY NULL"
        # 是未恢复告警
        if alarm_count:
            event_cases_sql = event_cases_sql + group_by + ";"
            return self._get_alarm_count_list(session, event_cases_sql, export_flag)
        else:
            event_sql = "SELECT endpoint FROM alarms.event_cases " \
                        "WHERE status IN ('OK', 'DEL') AND endpoint <> '' GROUP BY endpoint ORDER BY NULL;"
            return self._get_alarm_count_list(session, event_sql, export_flag, False)

    def list(self, filters=None, orders=None, offset=None, limit=None, hooks=None):
        event_cases_sql = "SELECT endpoint, MAX(timestamp) last_alarm_time, COUNT(1) alarm_count " \
                          "FROM alarms.event_cases " \
                          "WHERE status = 'PROBLEM'"
        with self.get_session() as session:
            # 传入ids 是普通查询 只返回限制ids数据
            endpoints = filters.get("ids")
            export_flag = filters.get("export_bff_data")
            if endpoints:
                return self._query_alarm_count(session, endpoints, event_cases_sql)
            else:
                # 导出需返回全部数据
                data = self._query_alarm_count_slow(session, filters, orders, event_cases_sql, export_flag)
                return {"data": data}


class EventsManageResource(EventBaseResource, CustomQuery):
    orm_meta = EventsManage
    _default_order = ['-id']
    _primary_keys = 'id'
    _tenant_field = "event_cases.tenant_id"
    _project_field = "event_cases.project_id"

    @staticmethod
    def _get_alarm_note_info(alarm_note, status, timestamp, event_case_id):
        """
        :param alarm_note:
        :param status:
        :param timestamp:
        :param event_case_id:
        :return:
        """
        if status == 'PROBLEM':
            alarm_note_list = alarm_note.list(filters={'timestamp': {'gt': timestamp}, 'event_case_id': event_case_id})
        else:
            alarm_note_list = alarm_note.list(filters={'timestamp': {'lt': timestamp}, 'event_case_id': event_case_id})
        return alarm_note_list

    def count(self, filters=None, offset=None, limit=None, hooks=None):
        """
        获取符合条件的记录数量

        :param filters: 过滤条件
        :type filters: dict
        :param offset: 起始偏移量
        :type offset: int
        :param limit: 数量限制
        :type limit: int
        :param hooks: 钩子函数列表，函数形式为func(query, filters)
        :type hooks: list
        :returns: 数量
        :rtype: int
        """
        offset = offset or 0
        orders = []
        if filters.get('single', False):
            filters.setdefault('query_count', True)
            query = self._custom_query(filters, orders, offset, limit, hooks)
            return query
        query = self._custom_query(filters, orders, offset, limit, hooks)
        return query.count()

    def _custom_query(self, filters=None, orders=None, offset=None, limit=None, hooks=None):
        """
        自定query查询语句
        :param filters:
        :param orders:
        :param offset:
        :param limit:
        :param hooks:
        :return:
        """
        # 按照id排序
        orders = [i.replace("id", "timestamp") if "id" in i else i for i in orders]
        with self.get_session() as session:
            filters_c = copy.deepcopy(filters)
            if filters_c.pop('single', False):

                fields = ["events.id", "events.event_caseId", "events.step", "events.cond", "events.status",
                          "events.timestamp",
                          "event_cases.id", "event_cases.timestamp", "event_cases.priority", "event_cases.metric",
                          "event_cases.note",
                          "event_cases.endpoint", "event_cases.source_type", "host.ip", "host.exthostname",
                          "cmdb_sys.app", "cmdb_sys.stack", "cmdb_sys.system", "if_project.name", "iam_tenant.name",
                          "available_zone.name"]
                if filters_c.pop('query_count', None):
                    fields = ["count(*)"]
                master_table = 'alarms.events'
                sql = self.build_sql(table=master_table, join_tables=["alarms.event_cases", "falcon_portal.host",
                                                                      "falcon_portal.cmdb_sys",
                                                                      "falcon_portal.if_project",
                                                                      "falcon_portal.available_zone",
                                                                      "falcon_portal.iam_tenant"],
                                     join_tables_on={
                                         "alarms.event_cases": 'event_cases.id = events.event_caseId',
                                         "falcon_portal.host": 'event_cases.endpoint = host.hostname',
                                         "falcon_portal.if_project": 'if_project.id = event_cases.project_id',
                                         "falcon_portal.available_zone": 'available_zone.id = event_cases.az_id',
                                         "falcon_portal.iam_tenant": 'iam_tenant.uuid = event_cases.tenant_id',
                                         "falcon_portal.cmdb_sys": 'cmdb_sys.uuid = host.hostname',
                                     }, fields=fields, offset=offset, limit=limit, orders=orders, filters=filters_c)
                ret = session.execute(sql)
                refs = ret.fetchall()
                result = self.get_results(refs, fields, master_table.split('.')[1])
                return result
            start_time = filters_c.get('start_time', '')
            end_time = filters_c.get('end_time', '')
            host_ip = filters_c.get('host_info.ip', '')
            # query = self._get_query(session, filters=filters, orders=orders)
            # 自定义过滤条件
            if start_time and end_time and host_ip:
                event_caseid_list = self._get_event_cases_id_by_ip(host_ip)
                query = session.query(self.orm_meta).filter(self.orm_meta.timestamp.between(start_time, end_time),
                                                            self.orm_meta.event_caseId.in_(event_caseid_list))
                query = self._apply_filters(query, self.orm_meta, filters, orders)
            elif start_time and end_time:
                query = session.query(self.orm_meta).filter(self.orm_meta.timestamp.between(start_time, end_time))
                query = self._apply_filters(query, self.orm_meta, filters, orders)
            elif host_ip:
                event_caseid_list = self._get_event_cases_id_by_ip(host_ip)
                query = session.query(self.orm_meta).filter(self.orm_meta.event_caseId.in_(event_caseid_list))
                query = self._apply_filters(query, self.orm_meta, filters, orders)
            else:
                query = self._get_query(session, filters=filters, orders=orders)

            # query = self._apply_filters(query, self.orm_meta, filters, orders)
            if hooks:
                for h in hooks:
                    query = h(query, filters)
            query = self._addtional_list(query, filters)
            if offset:
                query = query.offset(offset)
            if limit is not None:
                query = query.limit(limit)
            return query

    def _get_event_cases_id_by_ip(self, ip):
        """
        根据ip获取id
        :param ip:
        :return: id list
        """

        with self.get_session() as session:
            query = session.query(EventCasesManage.id).join(Host, Host.hostname == EventCasesManage.endpoint). \
                filter(Host.ip.contains(ip))
            result = self._apply_filters(query, EventCasesManage).all()
            return [item[0] for item in result]
        #     execute_sql = "select t1.id from alarms.event_cases t1 join falcon_portal.host t2 " \
        #                   "on t1.endpoint=t2.hostname where t2.ip like '%s'" % ip
        #     ret = session.execute(execute_sql)
        #     refs = ret.fetchall()
        #     if refs:
        #         return [i[0] for i in refs]
        # return []

    def base_list(self, filters=None, orders=None, offset=None, limit=None, hooks=None):
        """
        获取符合条件的记录

        :param filters: 过滤条件
        :type filters: dict
        :param orders: 排序
        :type orders: list
        :param offset: 起始偏移量
        :type offset: int
        :param limit: 数量限制
        :type limit: int
        :param hooks: 钩子函数列表，函数形式为func(query, filters)
        :type hooks: list
        :returns: 记录列表
        :rtype: list
        """
        offset = offset or 0
        with self.get_session() as session:
            query = self._get_query(session, filters=filters, orders=orders)
            if hooks:
                for h in hooks:
                    query = h(query, filters)
            query = self._addtional_list(query, filters)
            if offset:
                query = query.offset(offset)
            if limit is not None:
                query = query.limit(limit)
            results = [rec.to_dict() for rec in query]
            return results

    def _get_last_event_data(self, event_case_id, event_id):
        """
        根据event_case id 和 event id以时间降序获取最近一次problem的时间，用于计算持续时间
        :param event_case_id:
        :param event_id:
        :return: [id,event_caseId,timestamp]
        """
        data = self.base_list(filters={"event_caseId": event_case_id,"id": {"lt": event_id}}, limit=1)
        if data:
            return data[0]
        return {}
        # with self.get_session() as session:
        #     execute_sql = "select id,event_caseId,`timestamp` from alarms.events " \
        #                   "where event_caseId = '%s' and id < %d and status = 0 ORDER BY `timestamp` DESC" \
        #                   % (event_case_id, event_id)
        #     ret = session.execute(execute_sql)
        #     refs = ret.fetchall()
        #     # query = self._get_query(session)
        #     # query = query.filter(and_(self.orm_meta.event_caseId == event_case_id, self.orm_meta.id < event_id)).\
        #         # order_by(self.orm_meta.timestamp)
        #     if refs:
        #         return refs[0]
        # return {}

    @staticmethod
    def _get_last_time(problem_time, timestamp):
        """
        返回持续时间
        :param problem_time:
        :param timestamp:
        :return:
        """
        return get_diff_time(problem_time, timestamp)

    def list(self, filters=None, orders=None, offset=None, limit=None, hooks=None):
        offset = offset or 0
        query = self._custom_query(filters, orders, offset, limit, hooks)
        results = []
        alarm_other_list = AlarmOtherManageResource().list()
        alarm_note = AlarmNoteResource()
        for event_data in query:
            if not filters.get('single', False):
                event_data = event_data.to_dict()
            item = event_data.get('event_cases')
            event_id = event_data.get('id')
            timestamp = event_data.get('timestamp')
            res = {}
            try:
                # 获取event数据
                event_case_id = item.get('id', '')
                res['id'] = event_case_id
                last_event_data = self._get_last_event_data(event_case_id, event_id)
                # 发生时间取update_at
                res['timestamp'] = timestamp
                res['last_time'] = self._get_last_time(last_event_data.get('timestamp'), timestamp)
                item.pop('timestamp', None)
                # 级别
                priority = int(item.pop('priority', 2))
                if priority == 0:
                    res['priority'] = "高"
                elif priority == 1:
                    res['priority'] = "中"
                else:
                    res['priority'] = "低"
                # 主机信息
                host_info = item.pop('host_info', None) or event_data.pop('host', None)
                # host不存在处理
                res['ip'] = host_info.get('ip') if host_info else ''
                res['exthostname'] = host_info.get('exthostname') if host_info else ''
                # 应用
                cmdb_sys = item.pop('cmdb_sys', None) or event_data.pop('cmdb_sys', None)
                res['app'] = res['stack'] = res['system'] = ''
                if cmdb_sys:
                    if isinstance(cmdb_sys, list):
                        cmdb_sys = cmdb_sys[0]
                    res['app'] = cmdb_sys.get('app')
                    res['stack'] = cmdb_sys.get('stack')
                    res['system'] = cmdb_sys.get('system')
                # 指标
                metric = item.get('metric', '')
                metrict = metric.split("/")[0]
                note = item.get('note', '')
                metricm = metrict
                # 指标信息 othermsg
                tags = metric.replace(metricm + "/", "")
                if tags == metricm:
                    tags = ""
                for c in alarm_other_list:
                    c_metric = c.get('metric', '')
                    if not c_metric or c_metric != metricm:
                        continue
                    v_key = c.get('s_tag')
                    v_value = ""
                    for cc in tags.split(','):
                        if v_key in cc and v_key:
                            v_value = cc.replace(v_key + "=", "")

                    tags = c.get('s_name') + ":" + v_value
                if note != "":
                    metricm = note + "(" + metricm + ")"
                # 指标
                res['metric_display'] = metricm
                res['metrict'] = metrict
                res['othermsg'] = tags
                # 告警值 1 > 1
                cond = event_data.get('cond', '')
                cond_list = cond.split(' ')
                current_value = cond_list[0]
                set_value = cond_list[2]
                if '.' in current_value:
                    res['current_value'] = '%.2f' % float(current_value)
                else:
                    res['current_value'] = current_value
                if '.' in current_value:
                    res['set_value'] = cond_list[1] + '%.2f' % float(set_value)
                else:
                    res['set_value'] = cond_list[1] + set_value
                # 可用区
                res['az'] = item.get('az', None) or event_data.get('available_zone', None)
                res['project'] = item.get('project', None) or event_data.get('if_project', None)
                res['tenant'] = item.get('tenant', None) or event_data.get('iam_tenant', None)
                res['endpoint'] = item.get('endpoint', '')
                res['source_type'] = item.get('source_type', '')
                # 处理
                operation = self._get_alarm_note_info(alarm_note, filters.get('status'), timestamp, res['id'])
                res['operation'] = 0
                if operation:
                    res['operation'] = 1
                results.append(res)
            except (AttributeError, KeyError, ValueError) as e:
                LOG.error("get event cases data(%s) error(%s)" % (item, e))
                continue
        return results


class AlarmNoteResource(ResourceBase):
    orm_meta = AlarmNoteManage
    _default_order = ['-id']
    _primary_keys = 'id'
    _validate = [
        ColumnValidator(field='event_case_id',
                        validate_on=['create:M', 'update:O']),
        ColumnValidator(field='alarm_note',
                        rule_type='length',
                        rule='1,200',
                        validate_on=['create:M', 'update:O']),
        ColumnValidator(field='creator',
                        validate_on=['create:M']),
        ColumnValidator(field='timestamp',
                        validate_on=['create:M'])
    ]
    custom_alert = CustomAlertManageResource()
    event_cases = EventCasesResource()

    def list(self, filters=None, orders=None, offset=None, limit=None, hooks=None, uid_flag=None):
        """
        获取符合条件的记录

        :param filters: 过滤条件
        :type filters: dict
        :param orders: 排序
        :type orders: list
        :param offset: 起始偏移量
        :type offset: int
        :param limit: 数量限制
        :type limit: int
        :param hooks: 钩子函数列表，函数形式为func(query, filters)
        :type hooks:
        :param uid_flag: 其他地方调用list方法时不需要进行数据隔离
        :type uid_flag: None/uid
        :returns: 记录列表
        :rtype: list
        """
        offset = offset or 0
        if uid_flag is None:
            pass
        else:
            event_case_id = filters.get("event_case_id")
            # 权限验证
            if not event_case_id:
                return []
            elif "custom_" in event_case_id and event_case_id.split("_")[1] != "":
                alarm_info = self.custom_alert.get(event_case_id.split("_")[1])
            else:
                alarm_info = self.event_cases.get(event_case_id)
            if not alarm_info:
                return []
            try:
                self.check_user_operate(uid_flag,
                                        alarm_info.get("project_id"),
                                        alarm_info.get("tenant_id"))
            except exceptions.ForbiddenError:
                return []

        with self.get_session() as session:
            query = self._get_query(session, filters=filters, orders=orders)
            if hooks:
                for h in hooks:
                    query = h(query, filters)
            query = self._addtional_list(query, filters)
            if offset:
                query = query.offset(offset)
            if limit is not None:
                query = query.limit(limit)
            user = UserManageResource()

            results = []
            uids = [i.to_dict().get('creator') for i in query if i.to_dict().get('creator')]
            user_list = user.list(filters={"uid": {"in": uids}})
            user_dict = {u.get("uid"): u.get("name") for u in user_list if u.get("uid")}
            for rec in query:
                res = {}
                item = rec.to_dict()
                res['timestamp'] = item.get('timestamp')
                uid = item.get('creator')
                res['creator'] = user_dict.get(uid) or uid
                res['note'] = item.get('alarm_note')
                results.append(res)
            return results

    def _before_create(self, resource, validate):
        resource["timestamp"] = datetime.datetime.now()
        event_case_id = resource.get("event_case_id")
        if "custom_" in event_case_id:
            custom_alert = CustomAlertManageResource()
            custom_alert_id = event_case_id.split("_")[1]
            if not custom_alert_id:
                raise exceptions.NotFoundError("rid:%s不存在" % event_case_id)
            custom_alert_item = custom_alert.get(custom_alert_id)
            if not custom_alert_item:
                raise exceptions.NotFoundError("rid:%s不存在" % event_case_id)
        else:
            event_case = EventCasesResource()
            event_case_item = event_case.get(event_case_id)
            if not event_case_item:
                raise exceptions.NotFoundError("rid:%s不存在" % event_case_id)
            # 判断权限
            self.check_user_operate(resource.get("creator"), event_case_item.get("project_id"),
                                    event_case_item.get("tenant_id"))


class ServiceCatalogResource(ResourceBase):
    orm_meta = models.ServiceCatalogManage
    _default_order = ['-id']
    _primary_keys = 'id'
    _validate = [
        ColumnValidator(field='id',
                        rule_type='integer',
                        validate_on=['create:M']),
        ColumnValidator(field='name',
                        rule_type='length',
                        rule='1,128',
                        validate_on=['create:M', 'update:O'])
    ]


# 告警组模板
class TPLManageResource(ResourceBase):
    orm_meta = models.TPLManage
    _default_order = ['-create_at']
    _primary_keys = 'id'
    _validate = [
        ColumnValidator(field='tpl_name',
                        rule_type='length',
                        rule='1,255',
                        validate_on=['create:M', 'update:O']),
        ColumnValidator(field='parent_id',
                        rule_type='integer',
                        nullable=True,
                        validate_on=['create:O', 'update:O']),
        ColumnValidator(field='action_id',
                        rule_type='integer',
                        validate_on=['create:M', 'update:O']),  # todo是否支持编辑
        ColumnValidator(field='tenant_id',
                        rule_type='length',
                        rule='1,32',
                        validate_on=['create:O']),
        ColumnValidator(field='project_id',
                        rule_type='length',
                        rule='1,32',
                        validate_on=['create:O']),
        ColumnValidator(field='create_user',
                        validate_on=['create:M']),
        ColumnValidator(field='create_at',
                        validate_on=['create:M']),
        ColumnValidator(field='update_user',
                        validate_on=['update:M']),
        ColumnValidator(field='update_at',
                        validate_on=['update:M']),
        ColumnValidator(field='asset_id',
                        rule_type='integer',
                        validate_on=['create:O'])
    ]

    def get_host_data(self, host_id):
        """
        自定义模板新增 查询host是否存在 返回租户、项目
        :param host_id:
        :return:
        """
        if not host_id:
            raise ValidationError("资源(%s)不存在" % host_id)
        sql_select = """
                    SELECT h.exthostname, se.tenant_id, se.project_id 
                    FROM search_endpoint AS se JOIN host AS h 
                    ON se.hostname = h.hostname AND h.id = %s
                    """ % host_id
        with self.get_session() as session:
            host_item = session.execute(sql_select).fetchone()
            if not host_item:
                raise ValidationError("资源(%s)不存在" % host_id)
            return host_item[0], host_item[1], host_item[2]

    def list(self, filters=None, orders=None, offset=None, limit=None, hooks=None):
        refs = super(TPLManageResource, self).list(filters, orders, offset, limit, hooks)
        return self.add_info(refs)

    def get_quick_list(self):
        with self.get_session() as session:
            sql_select = """SELECT id, tpl_name FROM tpl"""
            refs = session.execute(sql_select).fetchall()
            tpl_list = [{"id": i[0], "tpl_name": i[1]} for i in refs]
            return len(tpl_list), tpl_list

    def add_info(self, refs):
        # 获取update_user和create_user
        user_list = []
        parent_id_list = []
        for u in refs:
            update_user = u.get("update_user")
            create_user = u.get("create_user")
            if update_user and update_user not in user_list:
                user_list.append(update_user)
            if create_user and create_user not in user_list:
                user_list.append(create_user)
            parent_id = u.get("parent_id")
            if parent_id:
                parent_id_list.append(parent_id)
        user_dict = {}
        if user_list:
            user = UserManageResource()
            user_list = user.list(filters={"uid": {"in": user_list}})
            user_dict = {u.get("uid"): u for u in user_list if u.get("uid")}
        parent_tpl_dict = {}
        if parent_id_list:
            parent_tpl_list = super(TPLManageResource, self).list(filters={"id": {"in": parent_id_list}})
            parent_tpl_dict = {u.get("id"): u.get("tpl_name") for u in parent_tpl_list if u.get("id")}

        for item in refs:
            create_user = item.get("create_user")
            if create_user:
                item["create_user_id"] = create_user
                item["create_user"] = user_dict.get(create_user, None)
            else:
                item["create_user_id"] = ""
                item["create_user"] = None
            parent_id = item.get("parent_id")
            if parent_id:
                item["parent_name"] = parent_tpl_dict.get(parent_id)
            else:
                item["parent_name"] = None
            update_user = item.get("update_user")
            if update_user:
                item["update_user_id"] = update_user
                item["update_user"] = user_dict.get(update_user, None)
            else:
                item["update_user_id"] = None
                item["update_user"] = None
        return refs

    def _check_parent_id(self, resource, uid, operate_flag, old_id=None):
        parent_id = resource.pop("parentId", None)
        if old_id and parent_id == old_id:
            raise NotFoundError("父模板(%s)不能为自身" % parent_id)
        if parent_id and parent_id != "0":
            # 判断模板是否存在
            parent_id = int(parent_id)
            resource["parent_id"] = parent_id
            if not self.get(parent_id, uid, operate_flag):
                raise NotFoundError("父模板(%s)不存在" % parent_id)
        elif parent_id == "0":
            parent_id = int(parent_id)
            resource["parent_id"] = parent_id

    def _before_create(self, resource, validate):
        resource["create_at"] = datetime.datetime.now()
        tenant_id = resource.get("tenant_id")
        project_id = resource.get("project_id")
        if not tenant_id:
            resource.pop("tenant_id", None)
        if not project_id:
            resource.pop("project_id", None)
        tpl_name = resource.get("tpl_name")
        if not resource.get("tpl_name"):
            # 生成模板名称
            name = "自定义_" + str(int(time.time()))
            if resource.get("exthostname"):
                name = "自定义_" + resource.get("exthostname") + "_" + str(int(time.time()))
            resource["tpl_name"] = name
        # 同一租户下模板名不能重复
        res = super(TPLManageResource, self).list(filters={"tpl_name": tpl_name, "tenant_id": tenant_id})
        if res:
            raise ValidationError("当前租户中已存在该模板，请修改模板名称或重新选择租户")

    def create(self, resource, validate=True, detail=True, operate_flag=False):
        # 校验parent_id
        create_user = resource.get("create_user")
        self._check_parent_id(resource, create_user, operate_flag)

        tenant_id = resource.get("tenant_id")
        project_id = resource.get("project_id")
        with self.transaction() as session:
            # 克隆时会传入action_id
            action_id = resource.get("action_id")
            if not action_id:
                # 新增action 这里不处理权限 在tpl中校验权限
                action_resource = {}
                if project_id and tenant_id:
                    action_resource = {
                        "project_id": project_id, "tenant_id": tenant_id
                    }
                action_item = ActionManageResource(transaction=session).create(action_resource, insert_flag=True)
                action_id = action_item.get("id")
                resource.update({"action_id": action_id})
            return super(TPLManageResource, self).create(resource, validate, detail, operate_flag)

    def _before_update(self, rid, resource, validate):
        resource['update_at'] = datetime.datetime.now()
        tpl_name = resource.get("tpl_name")
        # 同一租户下模板名不能重复
        tpl_item = self.get(rid)
        tenant_id = tpl_item.get("tenant_id")
        res = super(TPLManageResource, self).list(filters={"tpl_name": tpl_name, "tenant_id": tenant_id})
        if res:
            for i in res:
                if i.get("id") != int(rid):
                    raise ValidationError("当前租户中已存在该模板，请修改模板名称")

    def update(self, rid, resource, filters=None, validate=True, detail=True, operate_flag=False):
        # 校验parent_id
        update_user = resource.get("update_user")
        self._check_parent_id(resource, update_user, operate_flag)
        return super(TPLManageResource, self).update(rid, resource, filters, validate, detail, operate_flag)

    def _addtional_delete(self, session, resource):
        # 1.删除策略
        StrategyManageResource(transaction=session).delete_all({"tpl_id": resource.get("id")})
        # 2.删除模板时 删除action action会级联删除对应的rel_action_user记录
        action_id = resource.get("action_id")
        ActionManageResource(transaction=session).delete_all({"id": action_id})
        RelActionUserManageResource(transaction=session).delete_all({"action_id": action_id})

    def clone_tpl(self, resource, operate_flag=False):
        # 1.校验被克隆模板id是否存在
        old_tpl_id = resource.get("id")
        create_user = resource.get("create_user")
        old_tpl = self.get(old_tpl_id, create_user, operate_flag)  # 这里权限验证 后续不需要处理了
        if not old_tpl:
            raise NotFoundError("克隆模板(%s)不存在" % str(old_tpl_id))
        # 2.生成克隆的模板名
        tpl_name = "copy_of_" + old_tpl.get("tpl_name", "")
        with self.transaction() as session:
            tenant_id = old_tpl.get("tenant_id")
            project_id = old_tpl.get("project_id")
            # 3.克隆action和rel_action_user
            new_action_id = self._clone_action(session, old_tpl, tenant_id, project_id)
            # 4.克隆模板tpl
            new_tpl = {
                "action_id": new_action_id,
                "create_user": create_user,
                "tenant_id": tenant_id,
                "project_id": project_id,
                "tpl_name": tpl_name
            }
            old_parent_id = old_tpl.get("parent_id")
            if old_parent_id:
                new_tpl.update({"parentId": old_parent_id})
            new_tpl = self.create(new_tpl)
            new_tpl_id = new_tpl.get("id")
            # 5.克隆strategy策略 并insert
            self._clone_strategy(session, old_tpl_id, new_tpl_id)
            return new_tpl

    @staticmethod
    def _clone_action(session, old_tpl, tenant_id, project_id):
        """
        克隆action和rel_action_user
        :param session:
        :param old_tpl:
        :return: new_action_id int
        """
        # 1.获取action 并insert
        old_action_id = old_tpl.get("action_id")
        action_manage = ActionManageResource(transaction=session)
        old_action = action_manage.get(old_action_id)
        if old_action:
            old_action.pop("id", None)
            old_action.pop("project", None)
            old_action.pop("tenant", None)
            new_action = {k: v for k, v in old_action.items() if v}
            new_action_item = action_manage.create(new_action, insert_flag=True)
            new_action_id = new_action_item.get("id")
            # 2.insert rel_action_user
            rel_action_manange = RelActionUserManageResource(transaction=session)
            old_rel_action = rel_action_manange.list(filters={"action_id": old_action_id})
            rel_action_user_sql = "INSERT INTO uic.rel_action_user(action_id, uic_id) VALUE "
            action_user_sql = ""
            for i in old_rel_action:
                if not i.get("uic_id"):
                    continue
                action_user_sql += "(%d, '%s')," % (new_action_id, i.get("uic_id"))
            # 新增rel_action_user
            if action_user_sql:
                rel_action_user_sql = rel_action_user_sql + action_user_sql[:-1] + ";"
                session.execute(rel_action_user_sql)
        else:
            new_action_resource = {}
            if tenant_id and project_id:
                new_action_resource = {
                    "tenant_id": tenant_id,
                    "project_id": project_id
                }
            new_action_item = action_manage.create(new_action_resource)
            new_action_id = new_action_item.get("id")
        return new_action_id

    @staticmethod
    def _clone_strategy(session, old_tpl_id, new_tpl_id):
        """
        克隆strategy
        :param session:
        :param old_tpl_id:
        :param new_tpl_id:
        :return:
        """
        strategy_manage = StrategyManageResource(transaction=session)
        old_strategy_list = strategy_manage.list(filters={'tpl_id': old_tpl_id})
        for strategy in old_strategy_list:
            strategy.pop("id", None)
            strategy.pop("project", None)
            strategy.pop("tenant", None)
            priority = strategy.pop("priority")
            new_strategy = {k: v for k, v in strategy.items() if v != ''}
            new_strategy["tpl_id"] = new_tpl_id
            new_strategy["priority"] = priority
            strategy_manage.create(new_strategy)  # 待优化

    def get_tenant_tpl(self, filters, offset, limit):
        with self.get_session() as session:
            if filters.get("tenant_id") == "*":
                return 0, []
            if filters.get("project_id"):
                filters.pop("project_id")
                query = session.query(self.orm_meta).filter(and_(TPLManage.tenant_id == TPLManage.project_id,
                                                                 TPLManage.tenant_id.in_(filters.get("tenant_admin"))))
                count = self._apply_filters(query, TPLManage, filters=filters).count()
                query = self._apply_filters(query, TPLManage, filters=filters).offset(offset).limit(limit)
            result = [rec.to_dict() for rec in query]
            result = self.add_info(result)
            return count, result

    def get_produce_tpl(self, filters, offset, limit):
        with self.get_session() as session:
            if filters.get("tenant_id") == "*":
                filters.pop("tenant_id")
                query = session.query(self.orm_meta).filter(TPLManage.tenant_id == "*")
            elif filters.get("project_id") == "*":
                filters.pop("project_id")
                query = session.query(self.orm_meta).filter(and_(TPLManage.tenant_id == TPLManage.project_id))
            count = self._apply_filters(query, TPLManage, filters=filters).count()
            query = self._apply_filters(query, TPLManage, filters=filters).offset(offset).limit(limit)
            result = [rec.to_dict() for rec in query]
            result = self.add_info(result)
            return count, result


# 资源绑定模板
class AssetTPLResource(ResourceBase):
    orm_meta = models.AssetTPLManage  # tpl
    _default_order = ['-id']
    _primary_keys = 'id'

    def relation_list(self, filters=None, orders=None, offset=None, limit=None, hooks=None):
        host_id = filters.pop("id", None)
        if not host_id:
            raise ValidationError("资源id(%s)为空" % host_id)
        # 判断获取模板状态
        binded = filters.pop("binded", None)
        with self.get_session() as session:
            offset = offset or 0
            tpl_host_list = TPLHostManageResource(transaction=session).list(filters={"host_id": host_id})
            select_tpl_ids = [i.get("tpl_id") for i in tpl_host_list]
            # 获取已绑定模板
            if binded:
                if select_tpl_ids:
                    filters.update({"id": {"in": select_tpl_ids}})
                    binded_tpl = self.list(filters=filters, orders=orders, offset=offset, limit=limit)
                    binded_result = [{"id": i["id"], "tpl_name": i["tpl_name"]} for i in binded_tpl]
                    binded_count = self.count(filters=filters)
                    return {"data": binded_result, "count": binded_count}
                else:
                    return {"data": [], "count": 0}
            if select_tpl_ids:
                filters["id"] = {"nin": select_tpl_ids}

            query = self._get_query(session, filters=filters)
            if offset:
                query = query.offset(offset)
            if limit is not None:
                query = query.limit(limit)

            results = []
            for rec in query:
                item = rec.to_dict()
                res_dict = {
                    "id": item["id"],
                    "tpl_name": item["tpl_name"],
                }
                results.append(res_dict)
            count = self.count(filters=filters)
            return {"data": results, "count": count}

    def _check_host_id(self, session, host_id, uid, operate_flag):
        """
        校验host是否存在与权限
        :param session:
        :param host_id:
        :param uid:
        :param operate_flag:
        :return:
        """
        sql_select = """
                    SELECT h.id, se.tenant_id, se.project_id FROM search_endpoint AS se 
                    JOIN host AS h ON se.hostname = h.hostname 
                    WHERE h.id = %s;""" % host_id
        host_item = session.execute(sql_select).fetchone()
        if not host_item:
            raise exceptions.NotFoundError(resource=HostResource.__name__)
        if operate_flag:
            tenant_id = host_item[1]
            project_id = host_item[2]
            # 资源权限校验
            self.check_user_operate(uid, project_id, tenant_id)

    def _check_tpl_ids(self, tpl_ids, uid, operate_flag):
        """
        校验模板是否存在和权限校验，返回有权限的模板id
        :param tpl_ids:
        :param uid:
        :param operate_flag:
        :return: tpl_ids list
        """
        tpl_ids_tmp = []
        if not tpl_ids:
            return tpl_ids_tmp
        tpl_list = self.list(filters={"id": {"in": tpl_ids.split(",")}})
        for i in tpl_list:
            tpl_id = i.get("id")
            if not tpl_id:
                continue
            tpl_ids_tmp.append(str(tpl_id))
            # todo 待优化 模板权限验证
            if not operate_flag:
                continue
            tenant_id = i.get("tenant_id")
            project_id = i.get("project_id")
            try:
                self.check_user_operate(uid, project_id, tenant_id)
            except exceptions.ForbiddenError:
                LOG.info("uid(%s) has no tpl(%s) permission" % (uid, i.get("tpl_name")))
        return tpl_ids_tmp

    def create(self, resource, validate=True, detail=True, operate_flag=False):
        # 1.校验id和ids
        host_id = resource.get("id")
        tpl_ids = resource.get("ids")
        uid = resource.get("create_user")
        binded = resource.pop("binded", None)
        if not host_id:
            raise ValidationError("资源id(%s)为空" % host_id)
        with self.transaction() as session:
            self._check_host_id(session, host_id, uid, operate_flag)
            tpl_ids_tmp = self._check_tpl_ids(tpl_ids, uid, operate_flag)
            tpl_host_resource = TPLHostManageResource(transaction=session)
            if not binded:
                # 删除有权限的模板中的数据
                tpl_host_resource.delete_all(filters={"host_id": host_id, "tpl_id": {"in": tpl_ids_tmp}})
            else:
                # insert tpl_host
                insert_tpl_host_sql = "INSERT IGNORE INTO falcon_portal.tpl_host(tpl_id, host_id) VALUE "
                value_sql = ""
                for i in tpl_ids_tmp:
                    value_sql += "(%s, %d)," % (i, host_id)
                if value_sql:
                    insert_tpl_host_sql = insert_tpl_host_sql + value_sql[:-1] + ";"
                    session.execute(insert_tpl_host_sql)
            result = {
                "CreateUser": uid,
                "id": host_id,
                "ids": ",".join(tpl_ids_tmp),
                "type": "host"
            }
            return result


class CounterManageResource(ResourceBase):
    orm_meta = models.CounterManage
    _default_order = ['-counter']
    _primary_keys = 'counter'


# 告警策略
class StrategyManageResource(ResourceBase):
    orm_meta = models.StrategyManage
    _default_order = ['-id']
    _primary_keys = 'id'
    _validate = [
        ColumnValidator(field='metric',
                        rule_type='length',
                        rule='1,128',
                        validate_on=['create:M', 'update:M']),
        ColumnValidator(field='tags',
                        rule_type='length',
                        rule='0,256',
                        nullable=True,
                        validate_on=['create:O', 'update:O']),
        ColumnValidator(field='max_step',
                        rule_type='integer',
                        validate_on=['create:M', 'update:M']),
        ColumnValidator(field='priority',
                        rule_type='integer',
                        validate_on=['create:M', 'update:M']),
        ColumnValidator(field='func',
                        rule_type='length',
                        rule='1,16',
                        validate_on=['create:M', 'update:M']),
        ColumnValidator(field='op',
                        rule_type='length',
                        rule='1,8',
                        validate_on=['create:M', 'update:M']),
        ColumnValidator(field='right_value',
                        rule_type='length',
                        rule='1,64',
                        validate_on=['create:M', 'update:M']),
        ColumnValidator(field='note',
                        rule_type='length',
                        rule='0,128',
                        nullable=True,
                        validate_on=['create:O', 'update:O']),
        ColumnValidator(field='run_begin',
                        rule=validator.MinSecdValidator(),
                        nullable=True,
                        validate_on=['create:O', 'update:O']),
        ColumnValidator(field='run_end',
                        rule=validator.MinSecdValidator(),
                        nullable=True,
                        validate_on=['create:O', 'update:O']),
        ColumnValidator(field='tpl_id',
                        rule=validator.IntZeorValidator(),
                        validate_on=['create:M']),
        ColumnValidator(field='tenant_id',
                        rule_type='length',
                        rule='1,32',
                        validate_on=['create:O']),
        ColumnValidator(field='project_id',
                        rule_type='length',
                        rule='1,32',
                        validate_on=['create:O']),
        ColumnValidator(field='envs',
                        rule_type='length',
                        rule='0,256',
                        nullable=True,
                        validate_on=['create:O', 'update:O'])
    ]

    counter_cache = counter_cache_time = None  # 指标缓存

    def _addtional_delete(self, session, resource):
        StrategyCallbackManageResource(transaction=session).delete(resource.get("id"))

    @staticmethod
    def check_lookup(num, func):
        # 整数判断
        try:
            num = int(num)
            func = int(func)
        except ValueError:
            raise ValidationError("num(%s) func(%s) 类型错误" % (num, func))

        # 大于0
        if num < 0 or num > func:
            raise ValidationError("num(%d) should in (0, %d)" % (num, func))

    @staticmethod
    def _init_counter():
        counter_list = CounterManageResource().list()
        return {i.get("counter"): i.get("right_value") for i in counter_list}

    @staticmethod
    def _check_run_time(resource):
        # 校验begin、end
        run_begin = resource.get("run_begin")
        run_end = resource.get("run_end")
        begin_flag = 1 if run_begin else 0
        end_flag = 1 if run_end else 0
        # 传的话两个必须都传 不传两个都不传
        if begin_flag ^ end_flag != 0:  # 为0都传或者都不传
            raise ValidationError("生效时间要么全为空,要么开始结束都要填写")

    def _check_right_value(self, resource):
        """
        校验阈值是否在设置范围内
        :param resource:
        :return:
        """
        if self.counter_cache is None:
            self.counter_cache = self._init_counter()
            self.counter_cache_time = int(time.time())
        elif self.counter_cache_time <= (int(time.time()) - (60 * 10)):
            # 10分钟重新加载一次指标
            self.counter_cache = self._init_counter()
            self.counter_cache_time = int(time.time())

        target_right_value = resource.get("right_value")
        metric = resource.get("metric")
        if not metric:
            return
        right_value_range = self.counter_cache.get(metric)
        if not right_value_range:
            return
        right_value = right_value_range.split("_")
        if len(right_value) != 2:
            return
        try:
            target_right_value = int(target_right_value)
            min_value = int(right_value[0])
            max_value = int(right_value[1])
        except ValueError:
            return
        if min_value <= target_right_value <= max_value:
            return
        else:
            return False, right_value_range

    @staticmethod
    def _insert_tpl(session, resource, asset_id, asset_name, tpl_type, tpl_manage, operate_flag):
        """
        新增默认模板 tpl_name
        ecs资源模板
        ft-ecs租户模板
        ft(cloud-monitor)-ecs项目模板
        :param session:
        :param resource:
        :param asset_id: 资源类型
        :param asset_name: 资源名
        :param tpl_type: 模板类型
        :param tpl_manage:
        :param operate_flag:
        :return: tpl_id / False
        """
        if not asset_id or not tpl_type:
            return False
        # 获取资源类型
        service_item = ServiceCatalogResource(transaction=session).get(asset_id)
        if not service_item:  # 没有找到添加资源类型
            if not asset_name:
                return False
            ServiceCatalogResource(transaction=session).create({
                "id": asset_id,
                "name": asset_name
            })
        else:
            asset_name = service_item.get("name")
        tenant_id = resource.get("tenant_id")
        project_id = resource.get("project_id")

        tpl_resource = {
            "create_user": resource.get("create_user"),
            "asset_id": asset_id
        }
        if tpl_type == "asset":  # 资源模板
            resource["tenant_id"] = tenant_id = "*"
            resource["project_id"] = project_id = "*"
            tpl_name = "%s资源模板" % asset_name

        elif tpl_type == "tenant":  # 租户模板
            # 继承资源模板
            asset_tpl = tpl_manage.list(filters={"asset_id": asset_id, "project_id": "*", "tenant_id": "*"})
            if not asset_tpl:
                raise ValidationError("租户无对应的产品模板(%s)，请先添加产品模板" % asset_name)
            asset_tpl_id = asset_tpl[0].get("id")
            tpl_resource.update({
                "parent_id": asset_tpl_id
            })
            # 2.获取租户
            tenant_item = TenantResource(transaction=session).get(tenant_id)
            tenant_name = tenant_item.get("name") if tenant_item else tenant_id
            resource["tenant_id"] = tenant_id
            resource["project_id"] = project_id = tenant_id
            tpl_name = "%s的%s租户模板" % (asset_name, tenant_name)
        elif tpl_type == "project":  # 项目模板
            # 1.继承租户模板
            tenant_tpl = tpl_manage.list(filters={
                "asset_id": asset_id, "project_id": tenant_id, "tenant_id": tenant_id
            })
            # 2.获取租户
            tenant_item = TenantResource(transaction=session).get(tenant_id)
            tenant_name = tenant_item.get("name") if tenant_item else tenant_id
            if not tenant_tpl:
                raise ValidationError("项目无对应产品(%s)租户模板(%s)，请先添加租户模板" %
                                      (asset_name, tenant_name))
            tenant_tpl_id = tenant_tpl[0].get("id")
            tpl_resource.update({
                "parent_id": tenant_tpl_id
            })
            # 3.获取项目
            project_item = ProjectResource(transaction=session).get(project_id)
            project_name = project_item.get("name") if project_item else project_id
            resource["tenant_id"] = tenant_id
            resource["project_id"] = project_id
            tpl_name = "%s的%s项目模板" % (asset_name, project_name)

        else:
            return False
        tpl_resource.update({
            "tpl_name": tpl_name,
            "tenant_id": tenant_id,
            "project_id": project_id
        })
        tpl_item = TPLManageResource(transaction=session).create(tpl_resource, operate_flag=operate_flag)
        return tpl_item.get("id")

    def create(self, resource, validate=True, detail=True, operate_flag=False):
        with self.transaction() as session:
            try:
                tpl_id = int(resource.get("tpl_id"))
            except ValueError:
                raise ValidationError("模板id(%s)参数错误" % tpl_id)
            tpl_manage = TPLManageResource(transaction=session)
            # 模板为0 新增模板 再新增策略
            asset_id = resource.pop("asset_id", None)
            asset_name = resource.pop("asset_name", None)
            tpl_type = resource.pop("tpl_type", None)
            if tpl_id == 0:
                tpl_id = self._insert_tpl(session, resource, asset_id, asset_name, tpl_type, tpl_manage, operate_flag)
                if tpl_id is False:
                    raise ValidationError("模板类型(%s)和资源类型(%s)错误" % (tpl_type, asset_id))
                resource["tpl_id"] = tpl_id
            else:
                if not tpl_manage.get(tpl_id):
                    raise ValidationError("模板(%s)不存在" % tpl_id)
            return super(StrategyManageResource, self).create(resource, validate, detail, operate_flag)

    def _before_create(self, resource, validate):
        self._check_run_time(resource)
        check_result = self._check_right_value(resource)
        if check_result is not None:
            raise ValidationError("阈值(%s)范围(%s)错误" % (resource.get("right_value"), check_result[1]))

    def _before_update(self, rid, resource, validate):
        self._check_run_time(resource)
        tmp_list = ["tags", "note", "run_begin", "run_end"]
        for i in tmp_list:
            if not resource.get(i):
                resource[i] = ""

    def cover_strategy(self, parent_id):
        datas = []
        if parent_id:
            # 1. 查询是否有父模板
            parent_tpl = TPLManageResource().get(parent_id)
            if not parent_tpl:
                return self.list(filters={"tpl_id": parent_id})
            tpl_id = parent_id
            parent_id = parent_tpl["parent_id"]
            strategies = self.cover_strategy(parent_id)
            sub_strategies = self.list(filters={"tpl_id": tpl_id})
            strategies = self.count_strategy(strategies, sub_strategies)
            datas.extend(strategies)
            return datas
        else:
            return []

    def count_strategy(self, parent_strategies, sub_strategies):
        strategies = []
        if not parent_strategies:
            [strategy.update({"source": "Current"}) for strategy in sub_strategies]
            return sub_strategies
        for parent_strategy in parent_strategies:
            flag = False
            for sub_strategy in sub_strategies:
                if (parent_strategy["metric"] == sub_strategy["metric"] and parent_strategy["tags"] ==
                        sub_strategy["tags"] and parent_strategy["priority"] == sub_strategy["priority"]):
                    flag = True
                sub_strategy.update({"source": "Current"})
            if flag:
                continue
            parent_strategy["source"] = "Parent"
            strategies.append(parent_strategy)
        sub_strategies.extend(strategies)
        return sub_strategies


# 告警行动
class ActionManageResource(ResourceBase):
    orm_meta = models.ActionManage
    _default_order = ['-id']
    _primary_keys = 'id'
    _validate = [
        ColumnValidator(field='url',
                        rule_type='length',
                        rule='0,255',
                        validate_on=['create:O', 'update:O']),
        ColumnValidator(field='callback',
                        rule_type='integer',
                        validate_on=['create:O', 'update:O']),
        ColumnValidator(field='before_callback_sms',
                        rule_type='integer',
                        validate_on=['create:O', 'update:O']),
        ColumnValidator(field='before_callback_mail',
                        rule_type='integer',
                        validate_on=['create:O', 'update:O']),
        ColumnValidator(field='after_callback_sms',
                        rule_type='integer',
                        validate_on=['create:O', 'update:O']),
        ColumnValidator(field='after_callback_mail',
                        rule_type='integer',
                        validate_on=['create:O', 'update:O']),
        ColumnValidator(field='sms_alarm',
                        rule_type='integer',
                        validate_on=['create:O', 'update:O']),
        ColumnValidator(field='tenant_id',
                        rule_type='length',
                        rule='1,32',
                        validate_on=['create:O']),
        ColumnValidator(field='project_id',
                        rule_type='length',
                        rule='1,32',
                        validate_on=['create:O'])
    ]

    @staticmethod
    def _deal_params(resource):
        # 1.处理CallBackURl url callback
        call_back_url = resource.pop("CallBackURL", None)
        if call_back_url:
            resource.update({
                "url": call_back_url,
                "callback": 1
            })
        else:
            resource.update({
                "url": '',
                "callback": 1
            })
        # 2.smsAlarm -1
        sms_alarm = resource.pop("smsAlarm", None)
        if sms_alarm != 1:
            resource.update({
                "sms_alarm": 0
            })
        else:
            resource.update({
                "sms_alarm": 1
            })

    def get_parent_action_url_by_tpl(self, tpl_id):
        with self.get_session() as session:
            result = session.execute(
                """SELECT t3.url ,t2.tpl_name FROM (
                SELECT    @r AS _id,  (SELECT @r := parent_id FROM tpl WHERE id = _id) AS parent_id, @l := @l + 1 AS lvl
                FROM    (SELECT @r := %s, @l:=0) vars,tpl h WHERE @r <> 0) T1 JOIN tpl T2 ON T1._id = T2.id 
                Join action t3 on t2.action_id = t3.id where t3.callback = 1 ORDER BY T1.lvl asc""" % tpl_id).fetchall()

            if result and isinstance(result, list) and len(result) > 0:
                return result[0][0], result[0][1]
            return None, None

    def create(self, resource, validate=True, detail=True, operate_flag=False, insert_flag=False):
        """
        创建action
        :param resource:
        :param validate:
        :param detail:
        :param operate_flag:
        :param insert_flag: 1.True新增模板是默认会创建一个空的action 2.False页面更新action
        :return:
        """
        if insert_flag:
            return super(ActionManageResource, self).create(resource)
        # 1.判断tplId是否存在
        tpl_id = resource.pop("tplId", None)
        create_user = resource.pop("create_user", None)
        uid = resource.pop("uid", "")
        # 数据隔离
        tpl_info = TPLManageResource().get(tpl_id, create_user, operate_flag)
        if not tpl_info:
            raise NotFoundError("模板(%s)不存在" % str(tpl_id))

        self._deal_params(resource)
        with self.transaction() as session:
            tenant_id = tpl_info.get("tenant_id")
            project_id = tpl_info.get("project_id")
            action_id = tpl_info.get("action_id")
            # 2.判断action_id是否为0
            if not action_id:
                # 2.1 为0新增action
                if tenant_id and project_id:
                    resource.update({
                        "tenant_id": tenant_id,
                        "project_id": project_id
                    })
                action_item = super(ActionManageResource, self).create(resource)
                action_id = action_item.get("id")
                TPLManageResource(transaction=session).update(tpl_id, {"action_id": action_id})
            else:
                # 2.2 更新action
                self.update(action_id, resource)

            # 4.删除rel_action_user
            rel_action_manange = RelActionUserManageResource(transaction=session)
            rel_action_manange.delete_all({"action_id": action_id})
            # 5.新增rel_action_user
            if uid:
                uids = uid.split(",")
                falcon_api = FalconApiService()
                try:
                    exits_user = UserManageResource(transaction=session).list(filters={"uid": {"in": uids}})
                    exits_user_arr = [i.get("uid") for i in exits_user]
                    need_query_uid = []
                    for uid in uids:
                        if uid not in exits_user_arr:
                            need_query_uid.append(uid)
                    if need_query_uid:
                        res = falcon_api.get_falcon_api_common("/cloud/v1/auth/users", params={"id": need_query_uid})
                        user_datas = res.get('data', [])
                        if user_datas:
                            add_user_sql = ""
                            for user in user_datas:
                                add_user_sql += "INSERT INTO uic.user(name,cnname,email,phone,uid) VALUES ('%s','%s','%s','%s'," \
                                                "'%s') ON DUPLICATE KEY UPDATE name = '%s',cnname = '%s',email = '%s'," \
                                                " phone = '%s', uid = '%s';" % (
                                                    user.get("name"), user.get("nickname") or '',
                                                    user.get("email") or '',
                                                    user.get("phone") or '', user.get("id"), user.get("name"),
                                                    user.get("nickname") or '', user.get("email") or '',
                                                    user.get("phone") or '', user.get("id"))
                            if add_user_sql:
                                session.execute(add_user_sql)
                except Exception as e:
                    LOG.error("get user data error %s" % e)
                rel_action_user_sql = "INSERT INTO uic.rel_action_user(action_id, uic_id) VALUE "
                action_user_sql = ""
                for i in uids:
                    if not i:
                        continue
                    action_user_sql += "(%d, '%s')," % (action_id, i)
                # 新增rel_action_user
                if action_user_sql:
                    rel_action_user_sql = rel_action_user_sql + action_user_sql[:-1] + ";"
                    session.execute(rel_action_user_sql)
            # 返回数据
            resp_data = dict()
            resp_data['tplId'] = tpl_id
            resp_data['callBackUrl'] = resource.get("url") or ""
            resp_data['smsAlarm'] = resource.get("sms_alarm")
            resp_data['uid'] = uid
            return resp_data


# 主机组
class GRPManageResource(ResourceBase):
    orm_meta = models.GRPManage
    _default_order = ['-id']
    _primary_keys = 'id'
    _validate = [
        ColumnValidator(field='grp_name',
                        rule_type='length',
                        rule='1,64',
                        validate_on=['create:M', 'update:O']),
        ColumnValidator(field='come_from',
                        rule_type='integer',
                        validate_on=['create:O', 'update:O']),
        ColumnValidator(field='tenant_id',
                        rule_type='length',
                        rule='1,32',
                        validate_on=['create:M']),
        ColumnValidator(field='project_id',
                        rule_type='length',
                        rule='1,32',
                        validate_on=['create:M']),
        ColumnValidator(field='create_user',
                        validate_on=['create:M']),
        ColumnValidator(field='create_at',
                        validate_on=['create:M']),
        ColumnValidator(field='update_user',
                        validate_on=['update:M']),
        ColumnValidator(field='update_at',
                        validate_on=['update:M'])
    ]

    def _before_create(self, resource, validate):
        resource['create_at'] = datetime.datetime.now()

    def _before_update(self, rid, resource, validate):
        resource['update_at'] = datetime.datetime.now()


# 主机组和模板关系
class GRPTplManageResource(ResourceBase):
    orm_meta = models.GRPTplManage
    _primary_keys = 'grp_id, tpl_id'



# 主机组里的主机
class GRPHostManageResource(ResourceBase):
    orm_meta = models.GRPHostManage
    _primary_keys = 'grp_id, host_id'


# 模板中的主机
class TPLHostManageResource(ResourceBase):
    orm_meta = models.TPLHostManage
    _primary_keys = 'tpl_id, host_id'


# 告警action和接收个人 关联
class RelActionUserManageResource(ResourceBase):
    orm_meta = models.RelActionUserManage
    orm_pool = pool.POOLS.uic
    _default_order = ['-id']
    _primary_keys = 'id'


# 租户
class TenantResource(ResourceBase):
    orm_meta = models.Tenant
    _default_order = ['-name']
    _primary_keys = 'uuid'

    def get_id_by_name(self, tenant_names):
        if isinstance(tenant_names, str):
            tenant_names = [tenant_names]
        with self.get_session() as session:
            refs = []
            for name in tenant_names:
                query = session.query(models.Tenant.uuid).filter(models.Tenant.name == name)
                result = self._apply_filters(query, models.Tenant).all()
                ref = [item[0] for item in result]
                refs.extend(ref)
            return refs


# 项目
class ProjectResource(ResourceBase):
    orm_meta = models.Project
    _default_order = ['-name']
    _primary_keys = 'id'
    _soft_del_flag = {'is_deleted': 1}
    _soft_delete = True

    def get_id_by_name(self, project_names):
        if isinstance(project_names, str):
            project_names = [project_names]
        with self.get_session() as session:
            refs = []
            for name in project_names:
                query = session.query(models.Project.id).filter(models.Project.name == name)
                result = self._apply_filters(query, models.Project).all()
                ref = [item[0] for item in result]
                refs.extend(ref)
            return refs


# 策略回调
class StrategyCallbackManageResource(ResourceBase):
    orm_meta = models.StrategyCallbackManage
    _default_order = ['-strategy_id']
    _primary_keys = 'strategy_id'

    def _before_update(self, rid, resource, validate):
        resource['update_at'] = datetime.datetime.now()


# TODO 自定义上报指标
class CustomCounterManageResource(ResourceBase):
    orm_meta = models.CustomCounterManage
    _default_order = ['-id']
    _primary_keys = 'id'

    def _before_update(self, rid, resource, validate):
        resource['t_modify'] = datetime.datetime.now()


# 自定义上报
class CustomManageResource(ResourceBase):
    orm_meta = models.CustomManage
    _default_order = ['uuid']
    _primary_keys = 'uuid'
    _validate = [
        ColumnValidator(field='uuid',
                        validate_on=['create:M']),
        ColumnValidator(field='env_type',
                        rule_type='length',
                        rule='0,32',
                        validate_on=['create:M', 'update:M']),
        ColumnValidator(field='tenant_id',
                        rule_type='length',
                        rule='1,32',
                        validate_on=['create:M']),
        ColumnValidator(field='provider'),
        ColumnValidator(field='region_id'),
        ColumnValidator(field='az_id'),
        ColumnValidator(field='project_id',
                        rule_type='length',
                        rule='1,32',
                        validate_on=['create:M']),
        ColumnValidator(field='create_user',
                        validate_on=['create:M']),
        ColumnValidator(field='create_at',
                        validate_on=['create:M']),
        ColumnValidator(field='update_user',
                        validate_on=['update:M']),
        ColumnValidator(field='update_at',
                        validate_on=['update:M'])
    ]

    def _before_update(self, rid, resource, validate):
        resource["update_at"] = datetime.datetime.now()

    def list(self, filters=None, orders=None, offset=None, limit=None, hooks=None):
        result = super(CustomManageResource, self).list(filters, orders, offset, limit, hooks)
        host_id_list = []
        update_user_list = []
        # 获取host_id 用于查询自定义指标信息
        # 获取update_user 用于展示name
        for i in result:
            host_info = i.get("host_info") or {}
            host_id = host_info.get("id")
            if host_id:
                host_id_list.append(host_id)
            update_user = i.get("update_user")
            if update_user:
                update_user_list.append(update_user)

        # 获取自定义指标信息
        if host_id_list:
            custom_counters = CustomCounterManageResource().list(filters={"host_id": {"in": host_id_list}})
        else:
            custom_counters = []
        custom_counters_dict = {}
        for i in custom_counters:
            host_id = i.get("host_id")
            if not host_id:
                continue
            custom_counter = {
                "id": i.get("id"),
                "counter": i.get("counter"),
                "type": i.get("type")
            }

            if host_id in custom_counters_dict:
                custom_counters_dict[host_id].append(custom_counter)
            else:
                custom_counters_dict[host_id] = [custom_counter]
        if update_user_list:
            update_user_info = UserManageResource().list(filters={"uid": {"in": update_user_list}})
            update_user_dict = {u.get("uid"): u.get("cnname") for u in update_user_info if u.get("uid")}
        else:
            update_user_dict = {}

        for item in result:
            environment_info = item.pop("environment", None) or {}
            env = item.pop("env_type", "")
            item["env"] = env
            item["EnvName"] = environment_info.get("name") or env
            item.pop("uuid", None)
            host_info = item.pop("host_info", None) or {}
            user_info = item.pop("user_info", None) or {}
            item["create_user"] = user_info.get("cnname")
            update_user = item.get("update_user")
            if not update_user:
                item["update_user"] = None
            else:
                item["update_user"] = update_user_dict.get(update_user, None)
            item["exthostname"] = host_info.get("exthostname", "")
            item["hostname"] = host_info.get("hostname", "")
            host_id = host_info.get("id", "")
            item["id"] = host_id
            custom_counters = custom_counters_dict.get(host_id, [])
            if host_id and custom_counters:
                item["custom_counters"] = custom_counters
            else:
                item["custom_counters"] = []
            item["ip"] = host_info.get("ip", "")
            item["type"] = host_info.get("type", "")
        return result

    def _before_create(self, resource, validate):
        resource.update({"create_at": datetime.datetime.now()})

    def create(self, resource, validate=True, detail=True, operate_flag=False):
        with self.transaction() as session:
            ip = resource.pop("ip", None)
            env_type = resource.pop("env", None) or resource.pop("env_type", None)
            if env_type:
                resource["env_type"] = env_type
            counter_type = resource.pop("counter_type", None)
            counters = resource.pop("counters", None)
            exthostname = resource.pop("exthostname", None)

            hostname = str(uuid4()).lower()
            host_resource = {
                "hostname": hostname,
                "type": "custom"
            }
            host_resource.update({"ip": ip})
            host_resource.update({"exthostname": exthostname})
            host_result = HostResource(transaction=session).create(host_resource)

            resource["uuid"] = hostname
            custome_result = super(CustomManageResource, self).create(resource, validate, detail, operate_flag)

            u_modify = resource.get("create_user")
            host_id = host_result.get("id")
            custom_counter_m = CustomCounterManageResource(transaction=session)
            custom_counter_resource = {
                "host_id": host_id,
                "u_modify": u_modify
            }
            for i, counter in enumerate(counters):
                custom_counter_resource["counter"] = counter
                custom_counter_resource["type"] = counter_type[i]
                custom_counter_m.create(custom_counter_resource)

            custome_result["counter_type"] = counter_type
            custome_result["counters"] = counters
            custome_result.pop("env_type", None)
            custome_result["env"] = env_type
            custome_result["exthostname"] = exthostname
            custome_result["id"] = host_id
            custome_result["ip"] = ip
            custome_result.pop("uuid", None)
            custome_result.pop("update_user", None)
            custome_result.pop("update_at", None)
            custome_result.pop("host_info", None)
            custome_result.pop("environment", None)
            user_info = custome_result.pop("user_info", None) or {}
            custome_result["create_user"] = user_info.get("cnname") or ""
            return custome_result

    def update(self, rid, resource, filters=None, validate=True, detail=True, operate_flag=False):
        # rid是host的id
        exthostname = resource.pop("exthostname", None)
        ip = resource.pop("ip", None)
        env_type = resource.pop("env", None) or resource.pop("env_type", None)
        if env_type:
            resource["env_type"] = env_type
        counter_type = resource.pop("counter_type", None)
        counters = resource.pop("counters", None)
        # update_user
        u_modify = resource.get("update_user")
        with self.transaction() as session:
            # 1.更新host表
            h_before_update, h_after_update = HostResource(transaction=session).update(
                rid,
                {"exthostname": exthostname, "ip": ip})
            # 判断rid和host是否有数据
            if not h_after_update:
                raise exceptions.NotFoundError(resource=HostResource.__name__)

            uuid = h_after_update.get("hostname")
            # 2.更新custom
            before_update, after_update = super(CustomManageResource, self).update(
                uuid, resource, filters, validate, detail, operate_flag)
            if not after_update:
                raise exceptions.NotFoundError(resource=CustomManageResource.__name__)

            # 3.删除custom_counter再insert
            custom_counter_m = CustomCounterManageResource(transaction=session)
            custom_counter_m.delete_all(filters={"host_id": rid})
            custom_counter_resource = {
                "host_id": rid,
                "u_modify": u_modify
            }
            for i, counter in enumerate(counters or []):
                custom_counter_resource["counter"] = counter
                custom_counter_resource["type"] = counter_type[i]
                custom_counter_m.create(custom_counter_resource)

            update_user_info = UserManageResource(transaction=session).list(filters={"uid": u_modify})
            update_user = ""
            for i in update_user_info:
                update_user = i.get("cnname") or ""
                break

            after_update["counter_type"] = counter_type
            after_update["counters"] = counters
            after_update.pop("env_type", None)
            after_update["env"] = env_type
            after_update["exthostname"] = exthostname
            after_update["id"] = rid
            after_update["ip"] = ip
            after_update.pop("uuid", None)
            after_update.pop("create_at", None)
            after_update.pop("create_user", None)
            after_update.pop("host_info", None)
            after_update.pop("environment", None)
            after_update.pop("user_info", None) or {}
            after_update["update_user"] = update_user
            return after_update, after_update

    def delete(self, rid, filters=None, operate_flag=False, delete_user=None):
        with self.transaction() as session:
            # 1.删除host
            h_count, h_resource_list = HostResource(transaction=session).delete(rid)
            if not h_count:
                raise exceptions.NotFoundError(resource=HostResource.__name__)
            # 2.删除custom_counter
            custom_counter_m = CustomCounterManageResource(transaction=session)
            custom_counter_m.orm_meta.attributes = ['id', 'counter', 'type']
            _, custom_counters = custom_counter_m.delete_all(filters={"host_id": rid})
            # 4.删除custom 原有逻辑没有删除custom表
            uuid = h_resource_list[0].get("hostname")
            ip = h_resource_list[0].get("ip")
            count, resource_list = super(CustomManageResource, self).delete(uuid, filters, operate_flag, delete_user)
            if not count:
                raise exceptions.NotFoundError(resource=CustomManageResource.__name__)
            # 5.删除tpl_host相关记录
            TPLHostManageResource(transaction=session).delete_all(filters={"host_id": rid})
            env = resource_list[0].get("env_type")
            result_list = [{
                "custom_counters": custom_counters,
                "exthostname": uuid,
                "host_id": rid,
                "ip": ip,
                "env": env
            }]
            custom_counter_m.orm_meta.attributes = ['id', 'host_id', 'counter', 'step', 'type', 't_modify', 'u_modify']
            return h_count, result_list


# 自定义告警策略
class CustomStrategyManageResource(ResourceBase):
    orm_meta = models.StrategyManage
    _default_order = ['-id']
    _primary_keys = 'id'
    _validate = [
        ColumnValidator(field='metric',
                        rule_type='length',
                        rule='1,128',
                        validate_on=['create:M', 'update:O']),
        ColumnValidator(field='max_step',
                        rule_type='length',
                        rule='1,11',
                        validate_on=['create:M', 'update:O']),
        ColumnValidator(field='tenant_id',
                        rule_type='length',
                        rule='1,32',
                        validate_on=['create:M']),
        ColumnValidator(field='project_id',
                        rule_type='length',
                        rule='1,32',
                        validate_on=['create:M']),
        ColumnValidator(field='priority',
                        rule_type='length',
                        rule='1,4',
                        nullable=True,
                        validate_on=['create:O', 'update:O']),
        ColumnValidator(field='func',
                        rule_type='length',
                        rule='1,16',
                        validate_on=['create:M', 'update:O']),
        ColumnValidator(field='op',
                        rule_type='length',
                        rule='1,8',
                        validate_on=['create:M', 'update:O']),
        ColumnValidator(field='right_value',
                        rule_type='length',
                        rule='1,64',
                        validate_on=['create:M', 'update:O']),
        ColumnValidator(field='tpl_id',
                        rule_type='integer',
                        validate_on=['create:M'])
    ]

    @staticmethod
    def _get_strategy_list(alarms):
        """
        根据alarm获取策略列表
        :return: list
        """
        strategy_list = []
        for i in alarms:
            alarm = i.split("^")
            if len(alarm) < 4:
                raise exceptions.ValidationError("告警策略校验失败!")
            strategy_list.append({
                "metric": alarm[0],
                "func": alarm[1],
                "op": alarm[2],
                "right_value": alarm[3],
                "max_step": alarm[4]
            })
        return strategy_list

    @staticmethod
    def _get_tpl_and_action_id(session, rid):
        # 查询host 获取 tpl_id actoin_id 判断host数据是否存在
        host_sql = r"""
                    SELECT t1.id, t1.exthostname, t3.tpl_name tpl_name, 
                    CONCAT('_',t1.exthostname,'_',SUBSTR(t1.hostname,1,8)) custom_tpl_name, 
                    t3.id tpl_id, t3.action_id 
                    FROM falcon_portal.host t1
                    LEFT JOIN falcon_portal.tpl_host t2 ON t2.host_id=t1.id
                    LEFT JOIN falcon_portal.tpl t3 ON t2.tpl_id=t3.id WHERE t1.id=%s
                    """ % rid
        info = session.execute(host_sql)
        tpl_id = ""  # int
        action_id = ""
        for i in info:
            # tpl_name == "自定义_exthostname_hostname" 表明存在自定义模板策略
            tpl_name = i[2]
            if tpl_name == "自定义" + i[3]:
                tpl_id = i[4]
                action_id = i[5]
                break
        return tpl_id, action_id

    def update(self, rid, resource, filters=None, validate=True, detail=True, operate_flag=False):
        alarms = resource.get("alarms") or []
        strategy_list = self._get_strategy_list(alarms)
        with self.transaction() as session:
            # 判断host是否存在
            host_info = HostResource(transaction=session).get(rid)
            if not host_info:
                raise exceptions.NotFoundError(resource=HostResource.__name__)
            else:
                exthostname = host_info.get("exthostname") or ""
                hostname = host_info.get("hostname") or ""
                if not exthostname or len(hostname) < 8:
                    raise exceptions.ValidationError("主机名%s(%s)校验失败!" % (exthostname, hostname))
            # 查询host 获取 grp_id tpl_id actoin_id 判断host数据是否存在
            tpl_id, action_id = self._get_tpl_and_action_id(session, rid)

            custom_item = CustomManageResource(transaction=session).get(hostname)
            if not custom_item:
                raise exceptions.NotFoundError(resource=CustomManageResource.__name__)
            # 租户和项目
            tenant_id = custom_item.get("tenant_id")
            project_id = custom_item.get("project_id")
            create_user = resource["update_user"]

            operate_flag_times = 0  # 权限验证次数 为了节省时间 验证过一次后后续操作不用验证
            # 新增
            if not action_id or not tpl_id:
                tpl_name = "自定义_%s_%s" % (exthostname, hostname[:8])
                # 2.新增action
                # 3.新增tpl 会自动新增action 这里需要权限控制 后续的操作可以不添加权限控制
                tpl_id, action_id = self._insert_tpl(session, tpl_name, create_user, tenant_id, project_id,
                                                     operate_flag)
                operate_flag_times += 1
                # 6.新增tpl_host
                self._insert_tpl_host(session, tpl_id, rid)
            # 处理rel_action_user
            actions = resource.get("action") or ""
            self._deal_rel_action_user(session, actions, action_id)
            # 删除strategy 自定义上报没有配置回调
            self.delete_all(filters={"tpl_id": tpl_id})
            # 新增strategy 后续优化
            for strategy in strategy_list:
                strategy.update({"tenant_id": tenant_id, "project_id": project_id, "tpl_id": tpl_id})
                if operate_flag_times < 1:  # 权限操作只验证一次 后续不用
                    strategy.update({"create_user": create_user})
                    self.create(strategy, operate_flag=operate_flag)
                    operate_flag_times += 1
                else:
                    self.create(strategy)
            reslut = {"action": actions, "alarms": alarms, "id": rid}
            return reslut, reslut

    @staticmethod
    def _insert_action(session, tenant_id, project_id):
        """
        新增action 返回action_id
        :param session:
        :param tenant_id:
        :param project_id:
        :return:
        """
        action_item = ActionManageResource(transaction=session).create(
            {"tenant_id": tenant_id, "project_id": project_id}, insert_flag=True)
        return action_item.get("id")

    @staticmethod
    def _insert_tpl(session, tpl_name, create_user, tenant_id, project_id, operate_flag):
        """
        新增tpl 返回tpl_id
        :param session:
        :param tpl_name:
        :param create_user:
        :param tenant_id:
        :param project_id:
        :return:
        """
        tpl_resource = {
            "tpl_name": tpl_name,
            "create_user": create_user,
            "tenant_id": tenant_id,
            "project_id": project_id
        }
        tpl_item = TPLManageResource(transaction=session).create(tpl_resource, operate_flag=operate_flag)
        return tpl_item.get("id"), tpl_item.get("action_id")

    @staticmethod
    def _insert_tpl_host(session, tpl_id, host_id):
        TPLHostManageResource(transaction=session).create(
            {"tpl_id": tpl_id, "host_id": host_id})

    @staticmethod
    def _deal_rel_action_user(session, actions, action_id):
        # 删除rel_action_user
        RelActionUserManageResource(transaction=session).delete_all(filters={"action_id": action_id})
        rel_action_user_sql = "INSERT INTO uic.rel_action_user(action_id, uic_id) VALUE "
        action_user_sql = ""
        for i in actions.split(","):
            if not i:
                continue
            action_user_sql += "(%d, '%s')," % (action_id, i)
        # 新增rel_action_user
        if action_user_sql:
            rel_action_user_sql = rel_action_user_sql + action_user_sql[:-1] + ";"
            session.execute(rel_action_user_sql)


# TODO 自定义上报环境
class EnvironmentManageResource(ResourceBase):
    orm_meta = models.EnvironmentManage
    _default_order = ['-ctime']
    _primary_keys = 'id'

    def _before_create(self, resource, validate):
        resource["ctime"] = datetime.datetime.now()

    def _before_update(self, rid, resource, validate):
        resource["mtime"] = datetime.datetime.now()


class HostResource(ResourceBase):
    orm_meta = models.Host
    _default_order = ['-id']
    _primary_keys = 'id'
    _validate = [
        ColumnValidator(field='hostname',
                        rule_type='length',
                        rule='1,255',
                        validate_on=['create:M', 'update:O']),
        ColumnValidator(field='ip',
                        rule=validator.IpValidator(), converter=converter.IPv6AddressConverter(),
                        validate_on=['create:M', 'update:O']),
        ColumnValidator(field='agent_version',
                        nullable=True),
        ColumnValidator(field='plugin_version',
                        nullable=True),
        ColumnValidator(field='maintain_begin',
                        nullable=True),
        ColumnValidator(field='maintain_end',
                        nullable=True),
        ColumnValidator(field='update_at',
                        validate_on=['create:M', 'update:M']),
        ColumnValidator(field='uuid',
                        nullable=True,
                        rule_type='length',
                        rule='1,64',
                        validate_on=['create:O', 'update:O']),
        ColumnValidator(field='exthostname',
                        rule_type='length',
                        rule='1,255',
                        validate_on=['create:O', 'update:O']),
        ColumnValidator(field='type',
                        validate_on=['create:O', 'update:O']),
        ColumnValidator(field='maintain_owner',
                        nullable=True),
        ColumnValidator(field='maintain_owner_old',
                        nullable=True)
    ]

    def _before_create(self, resource, validate):
        resource["update_at"] = datetime.datetime.now()

    def _before_update(self, rid, resource, validate):
        resource["update_at"] = datetime.datetime.now()


class AlarmAssetResource(ResourceBase):
    def get_assets(self, params):
        with self.get_session() as session:
            sql_select = """
            FROM search_endpoint AS se JOIN host AS h 
            ON se.hostname = h.hostname AND se.ip = h.ip
            """
            filters = params['filters']
            tpl_id = filters.get('tplId')
            tenant_id = filters.get('tenant_id')
            project_id = filters.get('project_id')
            search = filters.get('search')
            filter_type = filters.get('type')

            if tpl_id:
                sql_select += """ JOIN tpl_host AS t ON t.host_id = h.id WHERE t.tpl_id = %d """ % (int(tpl_id))

            where_sql = ""
            flag = True
            if isinstance(tenant_id, list) and isinstance(project_id, list):
                p_in_tmp = "se.project_id IN " + str(tuple(project_id))
                t_in_tmp = "se.tenant_id IN" + str(tuple(tenant_id))
                # 判断是否是空数组
                if tenant_id and project_id:
                    if len(tenant_id) == 1 and len(project_id) == 1:
                        where_sql += " AND se.project_id = '%s' AND se.tenant_id = '%s'" % \
                                     (str(project_id[0]), str(tenant_id[0]))
                    elif len(project_id) == 1:
                        where_sql += " AND se.project_id = '%s' AND %s" % (str(project_id[0]), t_in_tmp)
                    elif len(tenant_id) == 1:
                        where_sql += " AND %s AND se.tenant_id = '%s'" % (p_in_tmp, str(tenant_id[0]))
                    else:
                        where_sql += " AND %s AND %s" % (p_in_tmp, t_in_tmp)
                else:
                    where_sql += " AND 1!=1"
                    flag = False
            # todo 待优化
            else:
                if isinstance(tenant_id, str):
                    where_sql += " AND se.tenant_id = '%s'" % tenant_id
                elif isinstance(tenant_id, list):
                    t_in_tmp = "se.tenant_id IN" + str(tuple(tenant_id))
                    if tenant_id:
                        if len(tenant_id) == 1:
                            where_sql += " AND se.tenant_id = '%s'" % str(tenant_id[0])
                        else:
                            where_sql += " AND %s" % t_in_tmp
                    else:
                        where_sql += " AND 1!=1"
                        flag = False
                if isinstance(project_id, str):
                    where_sql += " AND se.project_id = '%s'" % project_id
                elif isinstance(project_id, list):
                    p_in_tmp = "se.project_id IN " + str(tuple(project_id))
                    if project_id:
                        if len(project_id) == 1:
                            where_sql += " AND se.project_id = '%s'" % str(project_id[0])
                        else:
                            where_sql += " AND %s" % p_in_tmp
                    else:
                        where_sql += " AND 1!=1"
                        flag = False

            if flag and search:
                where_sql += " AND (se.hostname = '%s' or se.exthostname LIKE '%s%%' OR se.ip LIKE '%s%%')" % (search, search, search)
            if flag and filter_type:
                where_sql += " AND h.type = '%s'" % filter_type

            sql_page = """ LIMIT %d OFFSET %d""" % \
                       (int(params.get('limit', 10)), int(params.get('offset', 0)))

            if where_sql:
                sql_select = sql_select + where_sql
            count = session.execute("SELECT COUNT(*) " + sql_select).fetchall()[0][0]
            fields_sql = "SELECT h.id, h.uuid, se.hostname, se.exthostname, se.ip, se.source, se.type, se.tenant_id, " \
                         "se.project_id, h.type "
            refs_raw = session.execute(fields_sql + sql_select + sql_page)
            return refs_raw, count

    def asset_result(self, params):
        refs_raw, count = self.get_assets(params)
        refs = []
        resource_tenant = TenantResource()
        tenant_id_list = []
        resource_project = ProjectResource()
        project_id_list = []
        for ref_raw in refs_raw:
            host = dict()
            host['id'] = ref_raw[0]
            host['uuid'] = ref_raw[1]
            host['hostname'] = ref_raw[2]
            host['exthostname'] = ref_raw[3]
            host['ip'] = ref_raw[4]
            host['source'] = ref_raw[5]
            host['type'] = ref_raw[9]
            tenant_id = ref_raw[7]
            host['tenant_id'] = tenant_id
            if tenant_id and tenant_id not in tenant_id_list:
                tenant_id_list.append(tenant_id)
            project_id = ref_raw[8]
            host['project_id'] = project_id
            if project_id and project_id not in project_id_list:
                project_id_list.append(project_id)
            refs.append(host)
        # 获取关联的租户项目信息
        tenant_list = resource_tenant.list(filters={'uuid': {"in": tenant_id_list}})
        tenant_dict = {i["uuid"]: i for i in tenant_list if i.get("uuid")}
        project_list = resource_project.list(filters={'id': {"in": project_id_list}})
        project_dict = {i["id"]: i for i in project_list if i.get("id")}
        for ref in refs:
            tenant_id = ref["tenant_id"]
            if tenant_id:
                ref['tenant'] = tenant_dict.get(tenant_id)
            else:
                ref['tenant'] = None
            project_id = ref["project_id"]
            if tenant_id:
                ref['project'] = project_dict.get(project_id)
            else:
                ref['project'] = None
        return refs, count

    def add_assets(self, tpl_id, ip_list, uid, operate_flag=False):
        """
        给模板添加资源
        :param tpl_id: 模板id
        :param ip_list: 资源ip
        :param uid: 操作用户id
        :param operate_flag: 是否权限控制
        :return:
        """
        # 权限验证 只判断用户有无该模板的权限 并判断有无该模板
        tpl_item = TPLManageResource().get(tpl_id, uid, operate_flag)
        if not tpl_item:
            raise exceptions.NotFoundError(resource=TPLManageResource.__name__)
        sql_select = """
        SELECT h.id, h.ip, se.tenant_id, se.project_id FROM search_endpoint AS se 
        JOIN host AS h ON se.hostname = h.hostname 
        WHERE h.ip """
        if len(ip_list) == 1:
            where_sql = "='%s'" % ip_list[0]
        else:
            where_sql = "in " + str(tuple(ip_list))
        sql_select += where_sql
        insert_sql = """INSERT IGNORE INTO tpl_host (tpl_id, host_id) VALUES """

        all_ip = []
        try:
            with self.get_session() as session:
                all_ip_list = session.execute(sql_select)
                values_sql = ""
                check_host_id = []
                for i in all_ip_list:
                    if operate_flag:
                        # 资源权限验证
                        tenant_id = i[2]
                        project_id = i[3]
                        try:
                            self.check_user_operate(uid, project_id, tenant_id)
                        except exceptions.ForbiddenError:
                            continue
                    host_id = i[0]
                    check_host_id.append(host_id)
                    all_ip.append(i[1])
                un_validate_ip = TPLHostManageResource().list(
                    filters={'tpl_id': int(tpl_id), 'host_id': {'in': check_host_id}})
                un_validata_id_list = {i.get('host_id'): "" for i in un_validate_ip}
                for validate_id in set(check_host_id):
                    if validate_id not in un_validata_id_list:
                        values_sql += "%s," % str((tpl_id, validate_id))
                if values_sql:
                    values_sql = values_sql[:-1] + ";"
                    insert_sql += values_sql
                    session.execute(insert_sql)
            illegal_host = [i for i in ip_list if i not in all_ip]
            if len(illegal_host) == len(ip_list):
                msg = "所填资源找不到相应信息,无法添加"
            elif len(illegal_host) > 0:
                msg = "新增部分资源成功，这些资源找不到相应信息或无权限:%s" % ",".join(illegal_host)
            else:
                msg = "新增资源成功"
        except Exception as e:
            LOG.error("insert host failed(%s)" % e)
            raise DBError(message="新增资源失败")

        return msg

    @staticmethod
    def delete_assets(tpl_id, host_ids, uid, operate_flag=False):
        """
        删除模板绑定资源
        :param tpl_id: 模板id
        :param host_ids: 资源id
        :param uid: 操作用户id
        :param operate_flag: 是否权限控制
        :return:
        """
        tpl_item = TPLManageResource().get(tpl_id, uid, operate_flag)
        if not tpl_item:
            raise exceptions.NotFoundError(resource=TPLManageResource.__name__)
        return TPLHostManageResource().delete_all({'tpl_id': int(tpl_id), 'host_id': {'in': host_ids}})
