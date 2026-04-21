# coding=utf-8
"""
本模块提供各类装饰器

"""

from __future__ import absolute_import

import functools
import logging
import re
import time

import requests
from limits.storage import storage_from_string
from limits.strategies import STRATEGIES
from limits.util import parse_many

from monitor.common import limitwrapper
from monitor.core import config
from monitor.lib.redis_lib import RedisForCommon

LIMITEDS = {}
LIMITEDS_EXEMPT = {}
FLIMITEDS = {}
FLIMITEDS_SINGLETON = {}


def limit(limit_value, key_function=None, scope=None, per_method=True, strategy=None, message=None, hit_func=None):
    """
    用于装饰一个controller表示其受限于此调用频率
    :param limit_value: limits的调用频率字符串或一个能返回限制器的函数.
    :param function key_func: 一个返回唯一标识字符串的函数，用于标识一个limiter,比如远端IP.
    :param function scope: 调用频率限制范围的命名空间.
    :param strategy: 频率限制算法策略.
    :param message: 错误提示信息可接受3个格式化（limit，remaining，reset）内容.
    :param hit_func: 使用自定义hit计算，并非每次访问都触发hit，而由用户自定定义
    """

    def _inner(fn):
        @functools.wraps(fn)
        def __inner(*args, **kwargs):
            instance = fn(*args, **kwargs)
            LIMITEDS.setdefault(instance, []).append(
                limitwrapper.LimitWrapper(limit_value, key_function, scope, per_method=per_method,
                                          strategy=strategy, message=message, hit_func=hit_func)
            )
            return instance

        return __inner

    return _inner


def limit_exempt(fn):
    """
    标识一个controller不受限与调用频率限制(当有全局limit时).
    """

    @functools.wraps(fn)
    def __inner(*args, **kwargs):
        instance = fn(*args, **kwargs)
        LIMITEDS_EXEMPT[instance] = None
        return instance

    return __inner


def flimit(limit_value, scope=None, key_func=None, strategy='fixed-window', message=None, storage=None, hit_func=None,
           delay_hit=False):
    """
    用于装饰一个函数、类函数表示其受限于此调用频率
    当装饰类成员函数时，频率限制范围是类级别的，意味着类的不同实例共享相同的频率限制，
    如果需要实例级隔离的频率限制，需要手动指定key_func，并使用返回实例标识作为限制参数
    
    :param limit_value: 频率设置：格式[count] [per|/] [n (optional)] [second|minute|hour|day|month|year]
    :param scope: 限制范围空间：默认python类/函数完整路径.
    :param key_func: 关键限制参数：默认为空字符串，自定义函数：def key_func(*args, **kwargs) -> string
    :param strategy: 算法：支持fixed-window、fixed-window-elastic-expiry、moving-window
    :param message: 错误提示信息：错误提示信息可接受3个格式化（limit，remaining，reset）内容
    :param storage: 频率限制后端存储数据，如: memory://, redis://:pass@localhost:6379
    :param hit_func: 函数定义为def hit(result) -> bool，为True时则触发频率限制器hit，否则忽略
    :param delay_hit: 默认在函数执行前测试频率hit，可以设置为True将频率测试hit放置在函数执行后，搭配hit_func
                       使用，可以获取到函数执行结果来控制是否执行hit

    """

    def special_singleton(cls):

        def _singleton(*args, **kwargs):
            fullkey = str((tuple(args), tuple(kwargs.items())))
            if fullkey not in FLIMITEDS_SINGLETON:
                FLIMITEDS_SINGLETON[fullkey] = cls(*args, **kwargs)
            return FLIMITEDS_SINGLETON[fullkey]

        return _singleton

    @special_singleton
    class _storage_agent(object):

        def __init__(self, s):
            self.storage = storage_from_string(s)

    def _default_key_func(*args, **kwargs):
        return ''

    def _default_hit_func(x):
        return True

    key_func = key_func or _default_key_func
    hit_func = hit_func or _default_hit_func

    def _inner(fn):

        @functools.wraps(fn)
        def __inner(*args, **kwargs):

            def _test_limit(user_result):
                for grp_limit in FLIMITEDS[__inner]:
                    cur_limits, cur_key_func, cur_scope, cur_message, cur_hit_func = grp_limit
                    cur_scope = cur_scope or (fn.__module__ + '.' + fn.__class__.__name__ + ':' + fn.__name__)
                    storage_a = _storage_agent(storage or config.CONF.rate_limit.storage_url).storage
                    limiter = STRATEGIES[strategy](storage_a)
                    for cur_limit in cur_limits:
                        plimit = (cur_limit, cur_key_func(*args, **kwargs), cur_scope)
                        if cur_hit_func(user_result) and not limiter.hit(*plimit):
                            if cur_message:
                                window_stats = limiter.get_window_stats(*plimit)
                                cur_message = cur_message % {
                                    'limit': cur_limit.amount, 'remaining': window_stats[1],
                                    'reset': int(window_stats[0] - time.time())}
                                raise limitwrapper.RateLimitExceeded(message=cur_message)
                            raise limitwrapper.RateLimitExceeded(limit=cur_limit)

            # 如果是多级flimit装饰器，会保留最后一个__inner->[所有limits]的映射关系
            if __inner in FLIMITEDS:
                if not delay_hit:
                    _test_limit(None)
                result = fn(*args, **kwargs)
                if delay_hit:
                    _test_limit(result)
            # 如果是已经被合并的__inner只需要执行并获取结果即可
            else:
                result = fn(*args, **kwargs)
            return result

        # 处理重复的装饰器
        # @flimit(...)
        # @flimit(...)
        # def host_report():
        #     pass
        if fn in FLIMITEDS:
            FLIMITEDS.setdefault(__inner, FLIMITEDS.pop(fn))
        FLIMITEDS.setdefault(__inner, []).append((parse_many(limit_value), key_func, scope, message, hit_func))
        return __inner

    return _inner


def tenant_project_func(project_flag=True, tenant_field="tenant_id", project_field="project_id", all_flag=True):
    """
    数据隔离是否到项目级别
    :param project_flag: 默认细化到项目 告警列表细化的租户级别
    :param tenant_field: 租户过滤默认字段 不同表可自定义不同的字段
    :param project_field: 项目过滤默认字段
    :param all_flag: 用户门户使用权限隔离False 管理门户不使用权限隔离 为了用户门户的容量平台列表后续会去掉
    :return:
    """

    def decorate_split_project_id(func):
        def wrapper(*args, **kwargs):
            val = func(*args, **kwargs)
            # logging.info('result: %s', val)
            project_id = project_field #'project_id'
            if isinstance(val, dict) and 'filters' in val \
                    and isinstance(val['filters'], dict) and project_id in val['filters'] \
                    and isinstance(val['filters'][project_id], str) \
                    and val['filters'][project_id].find(',') + 1:
                val['filters'][project_id] = re.split(', ?', val['filters'][project_id])
            return val

        return wrapper

    def tenant_project_func_inner(func):
        """
        用户所授权租户和项目装饰器
        :param func:
        :return:
        """

        @functools.wraps(func)
        @decorate_split_project_id
        def inner(*args, **kwargs):
            criteria = func(*args, **kwargs)
            filters = criteria.get('filters', {})
            # req.headers
            headers = args[1].headers  # 转为全小写
            # logging.info('headers: %s', headers)
            # 如果是监控服务内部调用 不做权限处理
            if headers.get("X-AUTH-TOKEN") == 'default-token-used-in-server-side':
                return criteria
            redis_key = headers.get("X-AUTH-UID", None)
            if not redis_key:
                redis_key = headers.get("X-AUTH-USER", None)
            # 如果uid不存在 则没有租户和项目权限 返回空项目和租户
            if not redis_key:
                logging.error('X-AUTH-UID/USER not found in headers')
                filters[tenant_field] = filters[project_field] = []
                return criteria
            redis_conn = RedisForCommon.get_instance_for_common_1()
            operating_dict = redis_conn.hgetall("operating_%s" % redis_key) or {}
            #logging.info("test_用户鉴权查询 - redis_key: %s, 返回结果: %s", redis_key, operating_dict)
            if not operating_dict:
                logging.error("未能获取到用户%s的租户和项目权限", redis_key)
                # 重新加载权限
                from monitor.core import config
                # header: -H 'Content-Type: application/json' -H 'Apitoken: {"name": "api-plugs", "sig": "default-token-used-in-server-side"}'
                headers_ = {'Content-Type': 'application/json',
                            'Apitoken': '{"name": "api-plugs", "sig": "default-token-used-in-server-side"}'}
                url = config.CONF.cloud_api.addr + "/cloud/v1/users/%s/policies/tenants" % redis_key
                resp = requests.request("GET", url, headers=headers_)
                print(resp.text)
                operating_dict = redis_conn.hgetall("operating_%s" % redis_key) or {}
                if not operating_dict:
                    logging.error("重试获取用户%s的租户和项目权限也无", redis_key)
                else:
                    logging.warning("已加载到用户%s的租户和项目权限", redis_key)

            # from monitor.apps.host_report.api.tenant_api import TenantApi
            # 判断是否是用户门户
            if "X-AUTH-TENANT" in headers or "X-AUTH-PROJECT" in headers:
                admin_flag = False
                filters["admin_flag"] = admin_flag
            else:
                admin_flag = True
                filters["admin_flag"] = admin_flag
                # 是管理门户请求 且 不需要数据隔离
                if all_flag is False:
                    # if tenant_field in filters:
                    #     filters[tenant_field] = TenantApi().get_cmdb_uuid(filters[tenant_field])
                    return criteria

            filters["admin"] = operating_dict.get("admin")
            # 判断是否是超管 是超管不做数据隔离
            if operating_dict.get("admin") == "1":
                # 用户门户添加租户项目过滤
                if admin_flag is False:
                    # param中有tenant_id和project_id 则忽略Header
                    if tenant_field in filters or project_field in filters:
                        pass
                    else:
                        if "X-AUTH-TENANT" in headers:
                            tenant_id = headers["X-AUTH-TENANT"]
                            filters[tenant_field] = tenant_id
                        if "X-AUTH-PROJECT" in headers:
                            project_id = headers["X-AUTH-PROJECT"]
                            filters[project_field] = project_id
                return criteria

            # redis中的租户和项目
            authored_tenant_ids = operating_dict.get("tenant_id").split(",") \
                if operating_dict.get("tenant_id") else []
            authored_project_ids = operating_dict.get("project_id").split(",") \
                if operating_dict.get("project_id", ) else []

            # 如果param中有tenant_id和project_id 则忽略Header
            tenant_id = filters.get(tenant_field, None) or headers.get("X-AUTH-TENANT", None)
            project_id = filters.get(project_field, None) or headers.get("X-AUTH-PROJECT", None)  # 支持逗号分隔的多个id
            if tenant_id:
                if isinstance(tenant_id, str):
                    if tenant_id == "*":
                        tenant_admin = operating_dict.get("tenant_admin")
                        filters["tenant_admin"] = tenant_admin.split(",") if tenant_admin else []
                        authored_tenant_ids = tenant_id
                    else:
                        authored_tenant_ids = tenant_id if tenant_id in authored_tenant_ids else []
                elif isinstance(tenant_id, list):
                    authored_tenant_ids = [i for i in tenant_id if i in authored_tenant_ids]

                if project_id:
                    if isinstance(project_id, str) and project_id.find(',')>=0:
                        project_id = re.split(', ?', project_id)
                    if isinstance(project_id, str):
                        if project_id == "*":
                            tenant_admin = operating_dict.get("tenant_admin")
                            filters["tenant_admin"] = tenant_admin.split(",") if tenant_admin else []

                            authored_project_ids = project_id  #
                        else:
                            authored_project_ids = project_id if project_id in authored_project_ids else []
                    elif isinstance(project_id, list):
                        authored_project_ids = [i for i in project_id if i in authored_project_ids]

            # 统一tenant_id
            # if not authored_tenant_ids or (project_id and project_flag):  # 有项目并且细化到项目则忽略租户
            #     pass
            # elif isinstance(authored_tenant_ids, str):
            #     authored_tenant_ids = TenantApi().get_cmdb_uuid(authored_tenant_ids)
            # elif isinstance(authored_tenant_ids, list):
            #     authored_tenant_ids = TenantApi().get_cmdb_uuid_by_list(authored_tenant_ids)

            # 为了优化 如果有项目参数 忽略租户过滤
            filters[tenant_field] = authored_tenant_ids
            # if project_id and project_flag:
            #     filters.pop(tenant_field, None)
            # 隔离级别是否细化到项目级别
            if project_flag:
                filters[project_field] = authored_project_ids

            if not authored_tenant_ids:  # 租户为空时 项目也置为空
                filters[project_field] = []

            return criteria

        return inner

    return tenant_project_func_inner


def set_operate_user_func(user_field=None):
    """
    将Header中的X-Auth-UID传入resource中,用于增删改的权限操作
    :param user_field: 需要修改的字段
    :return:
    """

    def operate_user_inner(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            req = args[1]
            uid = req.headers.get("X-AUTH-UID")
            if func.__name__ == "delete":
                if user_field:
                    kwargs.update({user_field: uid})
                else:
                    kwargs.update({"delete_user": uid, "operate_flag": True})
                return func(*args, **kwargs)
            elif func.__name__ == "get":
                kwargs.update({"uid": uid, "operate_flag": True})
                return func(*args, **kwargs)
            if not isinstance(args[2], dict):
                return func(*args, **kwargs)
            if func.__name__ in ["create", "update"]:
                if user_field:
                    args[2][user_field] = uid
                else:
                    args[2]["%s_user" % func.__name__] = uid
            return func(*args, **kwargs)

        return inner

    return operate_user_inner
