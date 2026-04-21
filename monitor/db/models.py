# coding=utf-8
"""
本模块包含数据库模型

"""
from __future__ import absolute_import

import datetime

from sqlalchemy import Column, String, DateTime, Boolean, INT, ForeignKey, FLOAT, Integer, Text, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from monitor.db.dictbase import DictBase

Base = declarative_base()
metadata = Base.metadata


def get_names():
    """
    获取所有Model类名
    """
    return Base._decl_class_registry.keys()


def get_class_by_name(name):
    """
    根据Model类名获取类

    :param name: Model类名
    :type name: str
    :returns: Model类
    :rtype: class
    """
    return Base._decl_class_registry.get(name, None)


def get_class_by_tablename(tablename):
    """
    根据表名获取类

    :param tablename: 表名
    :type tablename: str
    :returns: Model类
    :rtype: class
    """
    for c in Base._decl_class_registry.values():
        if hasattr(c, '__tablename__') and c.__tablename__ == tablename:
            return c


def get_tablename_by_name(name):
    """
    根据Model类名获取表名

    :param name: Model类名
    :type name: str
    :returns: 表名
    :rtype: str
    """
    return Base._decl_class_registry.get(name, None).__tablename__


def get_name_by_class(modelclass):
    """
    根据Model类获取类名

    :param modelclass: Model类
    :type modelclass: class
    :returns: 类名
    :rtype: str
    """
    for n, c in Base._decl_class_registry.items():
        if c == modelclass:
            return n


# 默认为falcon_portal数据库的表结构
class HostReport(Base, DictBase):
    __tablename__ = 'host_report'
    attributes = ['id', 'uuid', 'hostname', 'platform', 'cpu_count', 'memory_gb', 'tenant_id', 'project_id',
                  'region_id', 'az_id', 'vm_type', 'cpu_busy_top_p95_day',
                  'cpu_busy_top_p95_week', 'cpu_busy_top_p95_month', 'mem_use_percent_top_p95_day',
                  'mem_use_percent_top_p95_week', 'mem_use_percent_top_p95_month',
                  'cpu_busy_top_day', 'cpu_busy_top_week', 'cpu_busy_top_month', 'mem_use_percent_top_day',
                  'mem_use_percent_top_week', 'mem_use_percent_top_month',
                  'created_date', 'day_str', 'tenant', 'project', 'region', 'available_zone', 'day_date', 'ip_address']
    detail_attributes = attributes

    id = Column(INT, primary_key=True)
    uuid = Column(String(30), nullable=False)
    hostname = Column(String(64), nullable=False)
    platform = Column(String(32), nullable=False)
    ip_address = Column(String(32), nullable=False)
    cpu_count = Column(INT)
    memory_gb = Column(INT)
    tenant_id = Column(ForeignKey('iam_tenant.uuid'), nullable=False)
    project_id = Column(ForeignKey('if_project.id'), nullable=False)
    region_id = Column(ForeignKey('if_region.id'), nullable=False)
    az_id = Column(ForeignKey('available_zone.id'), nullable=False)
    vm_type = Column(String(32))
    cpu_busy_top_p95_day = Column(FLOAT)
    cpu_busy_top_p95_week = Column(FLOAT)
    cpu_busy_top_p95_month = Column(FLOAT)
    mem_use_percent_top_p95_day = Column(FLOAT)
    mem_use_percent_top_p95_week = Column(FLOAT)
    mem_use_percent_top_p95_month = Column(FLOAT)
    cpu_busy_top_day = Column(FLOAT)
    cpu_busy_top_week = Column(FLOAT)
    cpu_busy_top_month = Column(FLOAT)
    mem_use_percent_top_day = Column(FLOAT)
    mem_use_percent_top_week = Column(FLOAT)
    mem_use_percent_top_month = Column(FLOAT)
    created_date = Column(DateTime)
    day_str = Column(String(10), nullable=False)
    day_date = Column(DateTime)

    tenant = relationship('Tenant', lazy='select')
    project = relationship('Project', lazy='select')
    region = relationship('Region', lazy='select')
    available_zone = relationship('AvailableZone', lazy='select')


# class Tenant(Base, DictBase):
#     __tablename__ = 'tenant'
#     attributes = ['id', 'name', 'created_date', 'updated_date', 'enabled', 'desc', 'cmdb_tenant_id', 'is_deleted']
#     detail_attributes = attributes
#     table_column = attributes
#
#     id = Column(String(32), primary_key=True)
#     name = Column(String(64))
#     created_date = Column(DateTime)
#     updated_date = Column(DateTime)
#     enabled = Column(Boolean, nullable=True, default=True)
#     desc = Column(String(64))
#     cmdb_tenant_id = Column(String(32))
#     is_deleted = Column(Integer(), default=0)
#     # az_ids = Column(Text)
#     # firewall_approval_manager = Column(Text)


class Tenant(Base, DictBase):
    __tablename__ = 'iam_tenant'
    attributes = ['uuid', 'name', 'description', 'state', 'admin_uuid']
    detail_attributes = attributes
    table_column = attributes

    uuid = Column(String(36), primary_key=True)
    name = Column(String(63), nullable=False)
    description = Column(String(255), default='')
    state = Column(Boolean, nullable=False)
    admin_uuid = Column(String(36), nullable=True)


# class Project(Base, DictBase):
#     __tablename__ = 'project'
#     attributes = ['id', 'name', 'created_date', 'updated_date', 'deleted_date', 'enabled', 'desc', 'tenant_id',
#                   'status', 'is_deleted', 'tenant']
#     detail_attributes = attributes
#     table_column = ['id', 'name', 'created_date', 'updated_date', 'deleted_date', 'enabled', 'desc', 'tenant_id',
#                     'status', 'is_deleted']
#
#     id = Column(String(32), primary_key=True)
#     name = Column(String(64))
#     created_date = Column(DateTime)
#     updated_date = Column(DateTime)
#     enabled = Column(Boolean, nullable=True, default=True)
#     desc = Column(String(64))
#     tenant_id = Column(ForeignKey("tenant.id"))
#     # create_openstack_flag = Column(Boolean, nullable=True, default=False)
#     # update_openstack_flag = Column(Integer())
#     # create_security_group_flag = Column(Boolean, nullable=True, default=False)
#     is_deleted = Column(Integer(), default=0)
#     deleted_date = Column(DateTime)
#     status = Column(String(32))
#     # user_id = Column(String(32))
#
#     tenant = relationship('Tenant', lazy='select')


class Project(Base, DictBase):
    __tablename__ = 'if_project'
    attributes = ['id', 'name', 'desc', 'tenant_id', 'enabled', 'status', 'tenant', 'is_deleted']
    detail_attributes = attributes
    table_column = ['id', 'name', 'desc', 'tenant_id', 'enabled', 'status']
    summary_attributes = table_column

    id = Column(String(32), primary_key=True)
    name = Column(String(63))
    enabled = Column(Boolean, nullable=True, default=True)
    desc = Column(String(200))
    tenant_id = Column(ForeignKey("iam_tenant.uuid"))
    status = Column(String(32))
    is_deleted = Column(Integer, default=0)

    tenant = relationship('Tenant', lazy='select')


class Region(Base, DictBase):
    __tablename__ = 'if_region'
    attributes = ['id', 'name', 'create_time', 'update_time', 'is_using']
    detail_attributes = attributes
    table_column = attributes
    update_column = ['name']

    id = Column(String(36), primary_key=True)
    name = Column(String(36))
    create_time = Column(DateTime)
    update_time = Column(DateTime, default=datetime.datetime.now())
    is_using = Column(Integer, nullable=False, default=0)


class CapacityMetric(Base, DictBase):
    __tablename__ = 'capacity_metric'
    attributes = ['f_id', 'f_metric_type', 'f_metric_name', 'f_enabled', 'f_modify_time', 'f_store_metric_name']
    detail_attributes = attributes
    table_column = attributes

    f_id = Column(Integer, primary_key=True)
    f_metric_type = Column(Integer, nullable=False)
    f_metric_name = Column(String(255), default='', nullable=False)
    f_store_metric_name = Column(String(255), default='', nullable=False)
    f_enabled = Column(Integer, default=1)
    f_modify_time = Column(DateTime, nullable=False, default=datetime.datetime.now())


class CsapacityStrategyTreeRoute(Base, DictBase):
    __tablename__ = 'capacity_strategy_tree_route'
    attributes = ['id', 'strategy_id', 'tree_route', 'metric_type']
    detail_attributes = attributes
    table_column = attributes

    id = Column(Integer, primary_key=True)
    strategy_id = Column(Integer)
    tree_route = Column(String(2048), default='', nullable=False)
    metric_type = Column(Integer, nullable=False, default=1)


class CapacityMetricFilterStrategy(Base, DictBase):
    __tablename__ = 'capacity_metric_filter_strategy'
    attributes = ['f_id', 'f_object_type', 'f_name', 'f_region_id', 'f_az_id', 'f_tenant_id', 'f_project_id',
                  'f_metric_id', 'f_metric_type', 'f_math_operator', 'f_threshold_value', 'f_enabled', 'f_creator',
                  'f_modify_time',
                  'tenant', 'available_zone', 'project', 'region']
    detail_attributes = attributes
    table_column = ['f_id', 'f_object_type', 'f_name', 'f_region_id', 'f_az_id', 'f_tenant_id', 'f_project_id',
                    'f_metric_id', 'f_metric_type', 'f_math_operator', 'f_threshold_value', 'f_enabled', 'f_creator',
                    'f_modify_time']

    f_id = Column(Integer, primary_key=True)
    f_object_type = Column(Integer, nullable=False, default=1)
    f_name = Column(String(255), nullable=False, default='')
    f_region_id = Column(String(36), ForeignKey('if_region.id'), nullable=False, default='')
    f_az_id = Column(String(36), ForeignKey('available_zone.id'), nullable=False, default='')
    f_tenant_id = Column(String(32), ForeignKey('iam_tenant.uuid'), nullable=False, default='')
    f_project_id = Column(String(32), ForeignKey('if_project.id'), nullable=False, default='')
    f_metric_id = Column(String(255), nullable=False, default=1)
    f_metric_type = Column(Integer, nullable=False, default=1)
    f_math_operator = Column(String(255), nullable=False, default='')
    f_threshold_value = Column(String(255), nullable=False, default='')
    f_enabled = Column(Integer, default=1)
    f_creator = Column(String(64), nullable=False, default='')
    f_modify_time = Column(DateTime, default=datetime.datetime.now(), nullable=False)

    tenant = relationship('Tenant', lazy='select')
    available_zone = relationship('AvailableZone', lazy='select')
    project = relationship('Project', lazy='select')
    region = relationship('Region', lazy='select')
    # user = relationship('UserManage', lazy='select')


class HostResourceCapacity(Base, DictBase):
    __tablename__ = 'host_resource_capacity'
    attributes = ['f_id', 'f_date_time', 'f_uuid', 'f_hostname', 'f_ip', 'f_region_id', 'f_az_id', 'f_tenant_id',
                  'f_project_id', 'f_host_type', 'f_belong_to_host', 'f_compute_node', 'f_platform', 'f_state',
                  'f_collect_flag', 'f_cpu_count', 'f_memory_gb', 'f_mem_use_percent_p100', 'f_mem_use_percent_p95',
                  'f_cpu_busy_p95', 'f_cpu_busy_p100',
                  'f_net_in_p95', 'f_net_out_p95', 'f_disk_read_p95', 'f_disk_write_p95', 'f_modify_time', 'env_type',
                  'tenant', 'available_zone', 'project', 'region']
    detail_attributes = attributes
    table_column = attributes

    f_id = Column(Integer, primary_key=True)
    f_date_time = Column(String(10), nullable=False, default='0000-00-00')
    f_uuid = Column(String(50), nullable=False, default='')
    f_hostname = Column(String(64), nullable=False, default='')
    f_ip = Column(String(32), nullable=False, default='')
    f_region_id = Column(String(36), ForeignKey('if_region.id'), nullable=False, default='')
    f_az_id = Column(String(36), ForeignKey('available_zone.id'), nullable=False, default='')
    f_tenant_id = Column(String(32), ForeignKey('iam_tenant.uuid'), nullable=False, default='')
    f_project_id = Column(String(32), ForeignKey('if_project.id'), nullable=False, default='')
    f_host_type = Column(String(32), nullable=False, default='')
    f_belong_to_host = Column(String(32), nullable=False, default='')
    f_compute_node = Column(Integer, nullable=False, default=0)
    f_platform = Column(String(32), nullable=False, default='')
    f_state = Column(String(32), nullable=False, default='')
    env_type = Column(String(32), nullable=False, default='')
    f_collect_flag = Column(Integer, nullable=False, default=0)
    f_cpu_count = Column(Integer, nullable=False, default=0)
    f_memory_gb = Column(Integer, nullable=False, default=0)
    f_mem_use_percent_p100 = Column(FLOAT, nullable=False, default=0)
    f_mem_use_percent_p95 = Column(FLOAT, nullable=False, default=0)
    f_cpu_busy_p95 = Column(FLOAT, nullable=False, default=0)
    f_cpu_busy_p100 = Column(FLOAT, nullable=False, default=0)  # CPU使用率峰值
    f_net_in_p95 = Column(String(255), nullable=False, default='0')
    f_net_out_p95 = Column(String(255), nullable=False, default='0')
    f_disk_read_p95 = Column(String(255), nullable=False, default='0')
    f_disk_write_p95 = Column(String(255), nullable=False, default='0')
    f_modify_time = Column(DateTime, default=datetime.datetime.now())

    tenant = relationship('Tenant', lazy='select')
    available_zone = relationship('AvailableZone', lazy='select')
    project = relationship('Project', lazy='select')
    region = relationship('Region', lazy='select')


class HostResourceCapacityWeek(Base, DictBase):
    __tablename__ = 'host_resource_capacity_week'
    attributes = ['f_id', 'f_date_time', 'f_uuid', 'f_hostname', 'f_ip', 'f_region_id', 'f_az_id', 'f_tenant_id',
                  'f_project_id', 'f_host_type', 'f_belong_to_host', 'f_compute_node', 'f_platform', 'f_state',
                  'f_collect_flag', 'f_cpu_count', 'f_memory_gb', 'f_mem_use_percent_p100', 'f_mem_use_percent_p95',
                  'f_cpu_busy_p95', 'f_cpu_busy_p100',
                  'f_net_in_p95', 'f_net_out_p95', 'f_disk_read_p95', 'f_disk_write_p95', 'f_modify_time', 'env_type',
                  'tenant', 'available_zone', 'project', 'region']
    detail_attributes = attributes
    table_column = attributes

    f_id = Column(Integer, primary_key=True)
    f_date_time = Column(String(10), nullable=False, default='0000-00-00')
    f_uuid = Column(String(50), nullable=False, default='')
    f_hostname = Column(String(64), nullable=False, default='')
    f_ip = Column(String(32), nullable=False, default='')
    f_region_id = Column(String(36), ForeignKey('if_region.id'), nullable=False, default='')
    f_az_id = Column(String(36), ForeignKey('available_zone.id'), nullable=False, default='')
    f_tenant_id = Column(String(32), ForeignKey('iam_tenant.uuid'), nullable=False, default='')
    f_project_id = Column(String(32), ForeignKey('if_project.id'), nullable=False, default='')
    f_host_type = Column(String(32), nullable=False, default='')
    f_belong_to_host = Column(String(32), nullable=False, default='')
    f_compute_node = Column(Integer, nullable=False, default=0)
    f_platform = Column(String(32), nullable=False, default='')
    f_state = Column(String(32), nullable=False, default='')
    env_type = Column(String(32), nullable=False, default='')
    f_collect_flag = Column(Integer, nullable=False, default=0)
    f_cpu_count = Column(Integer, nullable=False, default=0)
    f_memory_gb = Column(Integer, nullable=False, default=0)
    f_mem_use_percent_p100 = Column(FLOAT, nullable=False, default=0)
    f_mem_use_percent_p95 = Column(FLOAT, nullable=False, default=0)
    f_cpu_busy_p95 = Column(FLOAT, nullable=False, default=0)
    f_cpu_busy_p100 = Column(FLOAT, nullable=False, default=0)  # CPU使用率峰值
    f_net_in_p95 = Column(String(255), nullable=False, default='0')
    f_net_out_p95 = Column(String(255), nullable=False, default='0')
    f_disk_read_p95 = Column(String(255), nullable=False, default='0')
    f_disk_write_p95 = Column(String(255), nullable=False, default='0')
    f_modify_time = Column(DateTime, default=datetime.datetime.now())

    tenant = relationship('Tenant', lazy='select')
    available_zone = relationship('AvailableZone', lazy='select')
    project = relationship('Project', lazy='select')
    region = relationship('Region', lazy='select')


class HostResourceCapacityMonth(Base, DictBase):
    __tablename__ = 'host_resource_capacity_month'
    attributes = ['f_id', 'f_date_time', 'f_uuid', 'f_hostname', 'f_ip', 'f_region_id', 'f_az_id', 'f_tenant_id',
                  'f_project_id', 'f_host_type', 'f_belong_to_host', 'f_compute_node', 'f_platform', 'f_state',
                  'f_collect_flag', 'f_cpu_count', 'f_memory_gb', 'f_mem_use_percent_p100', 'f_mem_use_percent_p95',
                  'f_cpu_busy_p95', 'f_cpu_busy_p100',
                  'f_net_in_p95', 'f_net_out_p95', 'f_disk_read_p95', 'f_disk_write_p95', 'f_modify_time', 'env_type',
                  'tenant', 'available_zone', 'project', 'region']
    detail_attributes = attributes
    table_column = attributes

    f_id = Column(Integer, primary_key=True)
    f_date_time = Column(String(10), nullable=False, default='0000-00-00')
    f_uuid = Column(String(50), nullable=False, default='')
    f_hostname = Column(String(64), nullable=False, default='')
    f_ip = Column(String(32), nullable=False, default='')
    f_region_id = Column(String(36), ForeignKey('if_region.id'), nullable=False, default='')
    f_az_id = Column(String(36), ForeignKey('available_zone.id'), nullable=False, default='')
    f_tenant_id = Column(String(32), ForeignKey('iam_tenant.uuid'), nullable=False, default='')
    f_project_id = Column(String(32), ForeignKey('if_project.id'), nullable=False, default='')
    f_host_type = Column(String(32), nullable=False, default='')
    f_belong_to_host = Column(String(32), nullable=False, default='')
    f_compute_node = Column(Integer, nullable=False, default=0)
    f_platform = Column(String(32), nullable=False, default='')
    f_state = Column(String(32), nullable=False, default='')
    env_type = Column(String(32), nullable=False, default='')
    f_collect_flag = Column(Integer, nullable=False, default=0)
    f_cpu_count = Column(Integer, nullable=False, default=0)
    f_memory_gb = Column(Integer, nullable=False, default=0)
    f_mem_use_percent_p100 = Column(FLOAT, nullable=False, default=0)
    f_mem_use_percent_p95 = Column(FLOAT, nullable=False, default=0)
    f_cpu_busy_p95 = Column(FLOAT, nullable=False, default=0)
    f_cpu_busy_p100 = Column(FLOAT, nullable=False, default=0)  # CPU使用率峰值
    f_net_in_p95 = Column(String(255), nullable=False, default='0')
    f_net_out_p95 = Column(String(255), nullable=False, default='0')
    f_disk_read_p95 = Column(String(255), nullable=False, default='0')
    f_disk_write_p95 = Column(String(255), nullable=False, default='0')
    f_modify_time = Column(DateTime, default=datetime.datetime.now())

    tenant = relationship('Tenant', lazy='select')
    available_zone = relationship('AvailableZone', lazy='select')
    project = relationship('Project', lazy='select')
    region = relationship('Region', lazy='select')


class HostResourceCapacityLastDays(Base, DictBase):
    __tablename__ = 'host_resource_capacity_last_days'
    attributes = ['f_id', 'f_date_time', 'f_uuid', 'f_hostname', 'f_ip', 'f_region_id', 'f_az_id', 'f_tenant_id',
                  'f_project_id', 'f_host_type', 'f_belong_to_host', 'f_compute_node', 'f_platform', 'f_state',
                  'f_collect_flag', 'f_cpu_count', 'f_memory_gb', 'f_mem_use_percent_p100', 'f_mem_use_percent_p95',
                  'f_cpu_busy_p95', 'f_cpu_busy_p100',
                  'f_net_in_p95', 'f_net_out_p95', 'f_disk_read_p95', 'f_disk_write_p95', 'f_modify_time', 'env_type',
                  'tenant', 'available_zone', 'project', 'region']
    detail_attributes = attributes
    table_column = attributes

    f_id = Column(Integer, primary_key=True)
    f_date_time = Column(String(10), nullable=False, default='0000-00-00')
    f_uuid = Column(String(50), nullable=False, default='')
    f_hostname = Column(String(64), nullable=False, default='')
    f_ip = Column(String(32), nullable=False, default='')
    f_region_id = Column(String(36), ForeignKey('if_region.id'), nullable=False, default='')
    f_az_id = Column(String(36), ForeignKey('available_zone.id'), nullable=False, default='')
    f_tenant_id = Column(String(32), ForeignKey('iam_tenant.uuid'), nullable=False, default='')
    f_project_id = Column(String(32), ForeignKey('if_project.id'), nullable=False, default='')
    f_host_type = Column(String(32), nullable=False, default='')
    f_belong_to_host = Column(String(32), nullable=False, default='')
    f_compute_node = Column(Integer, nullable=False, default=0)
    f_platform = Column(String(32), nullable=False, default='')
    f_state = Column(String(32), nullable=False, default='')
    env_type = Column(String(32), nullable=False, default='')
    f_collect_flag = Column(Integer, nullable=False, default=0)
    f_cpu_count = Column(Integer, nullable=False, default=0)
    f_memory_gb = Column(Integer, nullable=False, default=0)
    f_mem_use_percent_p100 = Column(FLOAT, nullable=False, default=0)
    f_mem_use_percent_p95 = Column(FLOAT, nullable=False, default=0)
    f_cpu_busy_p95 = Column(FLOAT, nullable=False, default=0)
    f_cpu_busy_p100 = Column(FLOAT, nullable=False, default=0)  # CPU使用率峰值
    f_net_in_p95 = Column(String(255), nullable=False, default='0')
    f_net_out_p95 = Column(String(255), nullable=False, default='0')
    f_disk_read_p95 = Column(String(255), nullable=False, default='0')
    f_disk_write_p95 = Column(String(255), nullable=False, default='0')
    f_modify_time = Column(DateTime, default=datetime.datetime.now())

    tenant = relationship('Tenant', lazy='select')
    available_zone = relationship('AvailableZone', lazy='select')
    project = relationship('Project', lazy='select')
    region = relationship('Region', lazy='select')


class NetLineResourceCapacity(Base, DictBase):
    __tablename__ = 'netline_resource_capacity'
    attributes = ['f_id', 'f_wan_id', 'f_date_time', 'f_name', 'f_local_address', 'f_hardware_serial_num',
                  'f_upload_bandwidth_mb', 'f_download_bandwidth_mb', 'f_iprange', 'f_remote_address',
                  'f_remote_hardware_serial_num', 'f_local_hardware_interface_name', 'f_remote_hardware_interface_name',
                  'f_type', 'f_isp', 'f_net_in_octets', 'f_net_out_octets']
    detail_attributes = attributes
    table_column = ['f_id', 'f_wan_id', 'f_date_time', 'f_name', 'f_local_address', 'f_hardware_serial_num',
                    'f_upload_bandwidth_mb', 'f_download_bandwidth_mb', 'f_iprange', 'f_remote_address',
                    'f_remote_hardware_serial_num', 'f_local_hardware_interface_name',
                    'f_remote_hardware_interface_name',
                    'f_type', 'f_isp', 'f_net_in_octets', 'f_net_out_octets']

    f_id = Column(Integer, primary_key=True)
    f_wan_id = Column(String(100), nullable=False, default='')
    f_date_time = Column(String(10), nullable=False, default='0000-00-00')
    f_name = Column(String(50))
    f_local_address = Column(String(100))
    f_hardware_serial_num = Column(String(100))
    f_upload_bandwidth_mb = Column(String(50))
    f_download_bandwidth_mb = Column(String(50))
    f_iprange = Column(String(50), nullable=False, default='')
    f_remote_address = Column(String(100))
    f_remote_hardware_serial_num = Column(String(100))
    f_local_hardware_interface_name = Column(String(100))
    f_remote_hardware_interface_name = Column(String(1000))
    f_type = Column(String(50))
    f_isp = Column(String(50), default='')
    f_net_in_octets = Column(FLOAT, nullable=False, default=0)
    f_net_out_octets = Column(FLOAT, nullable=False, default=0)


class NetLineResourceCapacityWeek(Base, DictBase):
    __tablename__ = 'netline_resource_capacity_week'
    attributes = ['f_id', 'f_wan_id', 'f_date_time', 'f_name', 'f_local_address', 'f_hardware_serial_num',
                  'f_upload_bandwidth_mb', 'f_download_bandwidth_mb', 'f_iprange', 'f_remote_address',
                  'f_remote_hardware_serial_num', 'f_local_hardware_interface_name', 'f_remote_hardware_interface_name',
                  'f_type', 'f_isp', 'f_net_in_octets', 'f_net_out_octets']
    detail_attributes = attributes
    table_column = ['f_id', 'f_wan_id', 'f_date_time', 'f_name', 'f_local_address', 'f_hardware_serial_num',
                    'f_upload_bandwidth_mb', 'f_download_bandwidth_mb', 'f_iprange', 'f_remote_address',
                    'f_remote_hardware_serial_num', 'f_local_hardware_interface_name',
                    'f_remote_hardware_interface_name',
                    'f_type', 'f_isp', 'f_net_in_octets', 'f_net_out_octets']

    f_id = Column(Integer, primary_key=True)
    f_wan_id = Column(String(100), nullable=False, default='')
    f_date_time = Column(String(10), nullable=False, default='0000-00-00')
    f_name = Column(String(50))
    f_local_address = Column(String(100))
    f_hardware_serial_num = Column(String(100))
    f_upload_bandwidth_mb = Column(String(50))
    f_download_bandwidth_mb = Column(String(50))
    f_iprange = Column(String(50), nullable=False, default='')
    f_remote_address = Column(String(100))
    f_remote_hardware_serial_num = Column(String(100))
    f_local_hardware_interface_name = Column(String(100))
    f_remote_hardware_interface_name = Column(String(1000))
    f_type = Column(String(50))
    f_isp = Column(String(50), default='')
    f_net_in_octets = Column(FLOAT, nullable=False, default=0)
    f_net_out_octets = Column(FLOAT, nullable=False, default=0)


class AvailableZone(Base, DictBase):
    __tablename__ = 'available_zone'
    attributes = ['id', 'name', 'name_en', 'created_date', 'updated_date', 'enabled', 'location',
                  'city_code', 'module_code', 't_if_module', 'region',
                  'region_id', 'is_deleted', 'is_default_public', 'status', 'env', 't_if_env']
    summary_attributes = attributes
    detail_attributes = attributes
    table_column = ['id', 'name', 'name_en', 'created_date', 'updated_date', 'enabled', 'supported_products',
                    'sms_validate', 'city_code', 'status', 'module_code',
                    'region_id', 'is_deleted', 'is_default_public', 'status', 'extend_info', 'config', 'sold_out']

    id = Column(String(32), primary_key=True)
    name = Column(String(64), default='')
    name_en = Column(String(36), default='')
    env = Column(ForeignKey('environment.id'), nullable=False, default='')
    status = Column(String(30))
    created_date = Column(DateTime, default=datetime.datetime.now())
    updated_date = Column(DateTime, default=datetime.datetime.now())
    enabled = Column(Boolean, nullable=True, default=1)
    location = Column(String(64), default='')  # 地址
    extend_info = Column(String(255))  # 扩展信息
    region_id = Column(String(32), ForeignKey('if_region.id'), nullable=False, default='')
    is_deleted = Column(Integer(), default=0)
    supported_products = Column(Text)
    config = Column(Text)
    sold_out = Column(Boolean, default=False)
    city_code = Column(String(64), default='')
    module_code = Column(ForeignKey('module.id'), default='')
    sms_validate = Column(Integer(), default=0)
    is_default_public = Column(Integer(), default=0)

    t_if_env = relationship('EnvironmentManage', lazy='select')
    t_if_module = relationship('ModuleManage', lazy='select')
    region = relationship('Region', lazy=False)


class HostManage(Base, DictBase):
    __tablename__ = 'cmdb_host'
    attributes = ['uuid', 'hostname', 'ip', 'ipv6', 'os_type', 'os', 'env', 'host', 'env_type', 'environment',
                  'enabled', 'parentos', 'os_platform', 'state', 'cpu', 'mem', 'create_user', 'note',
                  'remote_manage_ip', 'region_id', 'az_id', 'tenant_id', 'project_id', 'tenant', 'project',
                  'is_computer_node', 'create_time', 'update_time', 'audited']
    detail_attributes = attributes
    summary_attributes = ['uuid', 'hostname', 'ip', 'ipv6', 'os_type', 'os', 'env_type', 'environment', 'enabled',
                          'parentos', 'os_platform', 'state', 'cpu', 'mem', 'create_user', 'note', 'remote_manage_ip',
                          'region_id', 'az_id', 'tenant_id', 'project_id', 'audited']

    uuid = Column(ForeignKey('falcon_portal.host.hostname'), primary_key=True)
    hostname = Column(String(100), default='')
    ip = Column(String(100), default='')
    ipv6 = Column(String(255), default='')
    os_type = Column(String(100), default='')
    os = Column(String(100), default='')
    env = Column(String(100), default='')
    enabled = Column(INT, nullable=False, default=1)
    create_time = Column(DateTime, default=datetime.datetime.now())
    update_time = Column(DateTime, default=datetime.datetime.now())
    env_type = Column(ForeignKey('environment.id'), default='')
    parentos = Column(String(255), default='')
    os_platform = Column(String(255), default='')
    state = Column(String(50), default='')
    cpu = Column(Integer)
    mem = Column(Integer)
    create_user = Column(String(100), default='')
    note = Column(String(255), default='')
    remote_manage_ip = Column(String(20), default='')
    region_id = Column(String(36))
    az_id = Column(String(36))
    tenant_id = Column(String(64), ForeignKey('iam_tenant.uuid'))
    project_id = Column(String(32), ForeignKey('if_project.id'))
    is_computer_node = Column(INT, nullable=False, default=0)
    audited = Column(Integer)
    host = relationship('Host', lazy='select')
    environment = relationship('EnvironmentManage', lazy='select')
    tenant = relationship('Tenant', lazy='select')
    project = relationship('Project', lazy='select')


class Host(Base, DictBase):
    __tablename__ = 'host'
    __table_args__ = {'schema': 'falcon_portal'}
    attributes = ['id', 'uuid', 'agent_version', 'hostname', 'ip', 'plugin_version', 'maintain_begin', 'maintain_end',
                  'update_at', 'exthostname', 'type', 'maintain_owner']

    id = Column(INT, primary_key=True)
    uuid = Column(String(64), nullable=False, default='')
    agent_version = Column(String(16), nullable=False, default='')
    hostname = Column(String(255), nullable=False, default='')
    ip = Column(String(16), nullable=False, default='')
    plugin_version = Column(String(128), nullable=False, default='')
    maintain_begin = Column(Integer, nullable=False, default=0)
    maintain_end = Column(Integer, nullable=False, default=0)
    update_at = Column(DateTime, nullable=True, default=None)
    exthostname = Column(String(255), default='')
    type = Column(String(20), default='')
    maintain_owner = Column(String(50))
    cmdb_sys = relationship(u'CmdbSYSManage',
                            primaryjoin='and_(foreign(Host.hostname) == CmdbSYSManage.uuid)',
                            lazy=False,
                            viewonly=True,
                            uselist=True)


class SearchEndPoint(Base, DictBase):
    __tablename__ = 'search_endpoint'
    __table_args__ = {'schema': 'falcon_portal'}
    attributes = ['hostname', 'exthostname', 'ip', 'source', 'type', 'env_type', 'env', 'tenant_id', 'project_id']

    hostname = Column(String(255), nullable=False, default='')
    exthostname = Column(String(255), nullable=False, default='')
    ip = Column(String(255), nullable=False, default='')
    source = Column(String(255), nullable=False, default='')
    type = Column(String(255), nullable=False, default='')
    env_type = Column(String(255), nullable=False, default='')
    env = Column(String(255), nullable=False, default='')
    tenant_id = Column(String(255), nullable=False, default='', primary_key=True)
    project_id = Column(String(255), nullable=False, default='', primary_key=True)


class HardwareModelManage(Base, DictBase):
    __tablename__ = 'if_hardware_model'
    attributes = ['id', 'name', 'brand', 'catalog', 'unit_height', 'description', 'create_time', 'update_time',
                  'catalog_detail']
    detail_attributes = attributes
    table_column = attributes

    id = Column(INT, primary_key=True)
    name = Column(String(63), nullable=False)
    brand = Column(String(63), nullable=False)
    catalog = Column(String(63), nullable=False)
    unit_height = Column(INT, nullable=False)
    description = Column(String(255))
    create_time = Column(DateTime, default=datetime.datetime.now())
    update_time = Column(DateTime)
    catalog_detail = Column(String(63))


class SWOidsManage(Base, DictBase):
    __tablename__ = 'sw_oids'
    attributes = ['id', 'model', 'metric', 'oid', 'uptime', 'description', 'is_deleted', 'oid_type', 'metric_type',
                  'calculate_type', 'calculate_oid', 'model_id']
    detail_attributes = attributes

    id = Column(INT, primary_key=True)
    model_id = Column(INT)
    model = Column(String(50), nullable=False)
    metric = Column(String(50), nullable=False)
    oid = Column(String(255))
    is_deleted = Column(INT, nullable=False, default=0)
    oid_type = Column(String(50), nullable=False, default='NODE_OID')
    metric_type = Column(String(50), nullable=False, default='GAUGE') #
    calculate_type = Column(String(50), default='')
    calculate_oid = Column(String(50), default='')
    description = Column(String(100))
    uptime = Column(DateTime, nullable=False, default=datetime.datetime.now())


class SWIprangeManage(Base, DictBase):
    __tablename__ = 'sw_iprange'
    attributes = ['iprange', 'serial_num', 'name', 'state', 'uptime', 'catalog', 'model', 'owner_name', 'owner_phone',
                  'mc', 'brand', 'pod', 'rack_code', 'module', 'env', 'enabled', 'environment', 'community',
                  'snmp_port', 'create_time', 'network_group', 'is_tor','snmp_enabled']
    detail_attributes = attributes
    summary_attributes = ['iprange', 'serial_num', 'name', 'state', 'catalog', 'model', 'owner_name', 'owner_phone',
                          'mc', 'brand', 'pod', 'rack_code', 'module', 'env', 'enabled', 'environment', 'community',
                          'snmp_port', 'network_group', 'is_tor','snmp_enabled']

    iprange = Column(String(50))
    serial_num = Column(String(50), primary_key=True)
    name = Column(String(100))
    state = Column(String(20))
    catalog = Column(String(50), default='')
    model = Column(String(50), default='')
    community = Column(String(100))
    owner_name = Column(String(50), default='')
    owner_phone = Column(String(50), default='')
    # mc = Column(String(50))
    mc = Column(ForeignKey('module.id'))
    brand = Column(String(50), default='')
    pod = Column(String(50), default='')
    env = Column(ForeignKey('environment.id'), default='pro')
    enabled = Column(INT, nullable=False, default=1)
    snmp_enabled = Column(INT, nullable=False, default=1)
    snmp_port = Column(INT)
    uptime = Column(DateTime, default=datetime.datetime.now())
    create_time = Column(DateTime, default=datetime.datetime.now())
    network_group = Column(String(50), default='')
    rack_code = Column(String(50), default='')
    is_tor = Column(INT)
    module = relationship('ModuleManage', lazy='select')
    environment = relationship('EnvironmentManage', lazy='select')


class IFWanManage(Base, DictBase):
    __tablename__ = 'if_wan'
    attributes = ['id', 'name', 'local_address', 'hardware_serial_num', 'upload_bandwidth_mb', 'download_bandwidth_mb',
                  'remote_address', 'remote_hardware_serial_num', 'local_hardware_interface_name', 'sw_iprange',
                  'remote_hardware_interface_name', 'type', 'uptime', 'line_code', 'access_point', 'isp', 'enabled',
                  'create_time', 'netline_type', 'measure_address', 'is_use_vpn']
    detail_attributes = attributes

    id = Column(String(100), primary_key=True)
    name = Column(String(50))
    local_address = Column(String(100))
    # hardware_serial_num = Column(String(100))
    hardware_serial_num = Column(ForeignKey('sw_iprange.serial_num'))
    upload_bandwidth_mb = Column(String(50))
    download_bandwidth_mb = Column(String(50))
    remote_address = Column(String(100))
    remote_hardware_serial_num = Column(String(100))
    local_hardware_interface_name = Column(String(100))
    remote_hardware_interface_name = Column(String(100))
    type = Column(String(50))
    isp = Column(String(50), default='')
    line_code = Column(String(100))
    access_point = Column(String(100))
    netline_type = Column(INT)
    enabled = Column(INT, nullable=False, default=1)
    uptime = Column(DateTime, default=datetime.datetime.now())
    create_time = Column(DateTime, default=datetime.datetime.now())
    measure_address = Column(String(100))
    is_use_vpn = Column(INT)
    sw_iprange = relationship('SWIprangeManage', lazy='joined')


class NetPodsManage(Base, DictBase):
    __tablename__ = 'net_pods'
    attributes = ['uuid', 'name', 'dc_name', 'env', 'update_at', 'environment']
    detail_attributes = attributes
    table_column = attributes

    uuid = Column(String(50), primary_key=True)
    name = Column(String(255), default='')
    env = Column(ForeignKey('environment.id'), nullable=False, default='')
    dc_name = Column(String(255), default='')
    update_at = Column(DateTime, default=datetime.datetime.now())

    environment = relationship('EnvironmentManage', lazy='select')


class NetSubsManage(Base, DictBase):
    __tablename__ = 'net_subs'
    attributes = ['uuid', 'name', 'cidr', 'env', 'vpc_uuid', 'pod_uuid', 'update_at', 'environment']
    detail_attributes = attributes
    table_column = attributes

    uuid = Column(String(50), primary_key=True)
    name = Column(String(255), default='')
    cidr = Column(String(255), default='')
    env = Column(ForeignKey('environment.id'), nullable=False, default='')
    vpc_uuid = Column(String(50), default='')
    pod_uuid = Column(String(50), default='')
    update_at = Column(DateTime, default=datetime.datetime.now())

    environment = relationship('EnvironmentManage', lazy='select')


class NetworkRelsManage(Base, DictBase):
    __tablename__ = 'network_rels'
    attributes = ['uuid', 'src_device', 'src_interface_name', 'dst_device', 'dst_interface_name', 'update_at']
    detail_attributes = attributes
    table_column = attributes

    uuid = Column(String(50), primary_key=True)
    src_device = Column(String(50))
    src_interface_name = Column(String(50))
    dst_device = Column(String(50))
    dst_interface_name = Column(String(50))
    update_at = Column(DateTime, default=datetime.datetime.now())


class ModuleManage(Base, DictBase):
    __tablename__ = 'module'
    attributes = ['id', 'name', 'env', 'rack_capacity', 'tdp_capacity', 'description', 'ctime', 'mtime', 'environment']
    detail_attributes = attributes
    summary_attributes = ['id', 'name', 'env', 'rack_capacity', 'tdp_capacity', 'description', 'ctime', 'mtime']

    id = Column(String(31), primary_key=True)
    name = Column(String(63), nullable=False)
    env = Column(ForeignKey('environment.id'), nullable=False)
    rack_capacity = Column(INT)
    tdp_capacity = Column(INT)
    description = Column(String(255), nullable=False)
    ctime = Column(DateTime, nullable=False, default=datetime.datetime.now())
    mtime = Column(DateTime, nullable=False, default=datetime.datetime.now())

    environment = relationship('EnvironmentManage', lazy='select')


class EnvironmentManage(Base, DictBase):
    __tablename__ = 'environment'
    attributes = ['id', 'enabled', 'name', 'gateway', 'graph', 'dashboard', 'tsdb', 'ctime', 'mtime']

    id = Column(String(36), primary_key=True)
    enabled = Column(INT, default=0)
    name = Column(String(255), nullable=False)
    gateway = Column(String(255), nullable=False, default='')
    graph = Column(String(255), nullable=False, default='')
    dashboard = Column(String(255), nullable=False, default='')
    tsdb = Column(String(255), nullable=False, default='')
    ctime = Column(DateTime, nullable=False, default=datetime.datetime.now())
    mtime = Column(DateTime)


class CMDBDBManage(Base, DictBase):
    __tablename__ = 'cmdb_db'
    attributes = ['uuid', 'name', 'type', 'sys_name', 'domain', 'tenant', 'env', 'charset', 'state', 'ctime', 'mtime',
                  'environment', 'cluster', 'storage_type', 'total_capacity', 'project_id', 'tenant_id',
                  'project_info', 'tenant_info']
    summary_attributes = ['uuid', 'name', 'type', 'sys_name', 'domain', 'tenant', 'env', 'charset', 'state',
                          'environment', 'cluster', 'storage_type', 'total_capacity', 'project_info', 'tenant_info']

    uuid = Column(String(255), primary_key=True)
    name = Column(String(255))
    type = Column(String(255), nullable=False)
    sys_name = Column(String(255))
    domain = Column(String(255))
    tenant = Column(String(255))
    env = Column(ForeignKey('environment.id'))
    charset = Column(String(255))
    state = Column(String(255))
    ctime = Column(DateTime, nullable=False, default=datetime.datetime.now())
    mtime = Column(DateTime, nullable=False, default=datetime.datetime.now())
    cluster = Column(String(255), default='')
    storage_type = Column(String(32))
    total_capacity = Column(Integer, default=0)
    project_id = Column(String(32), ForeignKey('if_project.id'))
    tenant_id = Column(String(64), ForeignKey('iam_tenant.uuid'))

    environment = relationship('EnvironmentManage', lazy='select')
    tenant_info = relationship('Tenant', lazy='select')
    project_info = relationship('Project', lazy='select')


class CMDBDBInstanceManage(Base, DictBase):
    __tablename__ = 'cmdb_db_instance'
    attributes = ['id', 'host_uuid', 'db_uuid', 'hostname', 'version', 'role', 'state', 'server_ip', 'server_port',
                  'ctime', 'mtime', 'db_instance', 'enabled', 'cmdb_host', 'node_id']
    detail_attributes = attributes
    id = Column(String(255), primary_key=True)
    host_uuid = Column(ForeignKey('cmdb_host.uuid'), nullable=False)
    db_uuid = Column(ForeignKey('cmdb_db.uuid'), nullable=False)
    hostname = Column(String(255), nullable=False)
    node_id = Column(String(36), nullable=False)
    version = Column(String(255))
    role = Column(String(255))
    state = Column(String(255))
    server_ip = Column(String(255), nullable=False)
    server_port = Column(String(255), nullable=False)
    user = Column(String(255))
    password = Column(String(255))
    enabled = Column(INT, nullable=False, default=1)
    ctime = Column(DateTime, nullable=False, default=datetime.datetime.now())
    mtime = Column(DateTime, nullable=False, default=datetime.datetime.now())

    db_instance = relationship('CMDBDBManage', lazy='select')
    cmdb_host = relationship('HostManage', lazy='select')


class ActionManage(Base, DictBase):
    __tablename__ = 'action'
    attributes = ['id', 'url', 'callback', 'before_callback_sms', 'before_callback_mail', 'after_callback_sms',
                  'after_callback_mail', 'sms_alarm', 'tenant_id', 'project_id', 'tenant', 'project']
    detail_attributes = attributes

    id = Column(Integer, primary_key=True)
    url = Column(String(255), nullable=False, default='')
    callback = Column(Integer, nullable=False, default=0)
    before_callback_sms = Column(Integer, nullable=False, default=0)
    before_callback_mail = Column(Integer, nullable=False, default=0)
    after_callback_sms = Column(Integer, nullable=False, default=0)
    after_callback_mail = Column(Integer, nullable=False, default=0)
    sms_alarm = Column(Integer, default=0)
    project_id = Column(String(32), ForeignKey('if_project.id'))
    tenant_id = Column(String(64), ForeignKey('iam_tenant.uuid'))

    tenant = relationship('Tenant', lazy='select')
    project = relationship('Project', lazy='select')


class ActionUserManage(Base, DictBase):
    __tablename__ = 'action_user'
    attributes = ['id', 'uic_id', 'user_name']
    detail_attributes = attributes

    id = Column(Integer, primary_key=True)
    uic_id = Column(Integer)
    user_name = Column(String(255), nullable=False)


class AlarmOtherManage(Base, DictBase):
    __tablename__ = 'alarm_other'
    attributes = ['id', 'metric', 's_name', 's_tag']
    detail_attributes = attributes

    id = Column(Integer, primary_key=True)
    metric = Column(String(255))
    s_name = Column(String(255))
    s_tag = Column(String(255))


class AlarmScheManage(Base, DictBase):
    __tablename__ = 'alarm_sche'
    attributes = ['id', 'group_type', 'start_date', 'end_date', 'empno_m', 'empno_b', 'isenable', 'updater', 'optime']
    detail_attributes = attributes

    id = Column(Integer, primary_key=True)
    group_type = Column(String(255), nullable=False)
    start_date = Column(String(255), nullable=False)
    end_date = Column(String(255), nullable=False)
    empno_m = Column(String(255), nullable=False)
    empno_b = Column(String(255))
    isenable = Column(Integer, default=0)
    updater = Column(String(255))
    optime = Column(String(255))


class AlarmTextCfgManage(Base, DictBase):
    __tablename__ = 'alarm_text_cfg'
    attributes = ['metric', 'title']
    detail_attributes = attributes

    metric = Column(String(255), primary_key=True)
    title = Column(String(255), nullable=False, default='')


class AlarmTypeManage(Base, DictBase):
    __tablename__ = 'alarm_type'
    attributes = ['id', 'endpoint', 'metric', 'a_type', 'tags']
    detail_attributes = attributes

    id = Column(Integer, primary_key=True)
    endpoint = Column(String(255), nullable=False)
    metric = Column(String(255), nullable=False, default='')
    a_type = Column(String(255), nullable=False)
    tags = Column(String(255), default='')


class BigDataAlertManage(Base, DictBase):
    __tablename__ = 'bigdata_alert'
    attributes = ['id', 'alert_msg', 'cur_count', 'is_close', 'al_level', 'update_time']
    detail_attributes = attributes

    id = Column(Integer, primary_key=True)
    alert_msg = Column(Text)
    cur_count = Column(Integer, nullable=False, default=1)
    is_close = Column(Integer, nullable=False, default=0)
    al_level = Column(Integer, nullable=False, default=0)
    update_time = Column(DateTime, nullable=False, default=datetime.datetime.now())


class CheckIPManage(Base, DictBase):
    __tablename__ = 'check_ip'
    attributes = ['id', 'ip_address', 'deploy_check_point', 'creator', 'dc']
    detail_attributes = attributes

    id = Column(Integer, primary_key=True)
    ip_address = Column(String(64), nullable=False)
    deploy_check_point = Column(String(64), nullable=False)
    creator = Column(String(32))
    dc = Column(String(10), default='')


class CheckIPPortManage(Base, DictBase):
    __tablename__ = 'check_ip_port'
    attributes = ['id', 'ip_address', 'port']
    detail_attributes = attributes

    id = Column(Integer, primary_key=True)
    ip_address = Column(String(64), nullable=False)
    port = Column(Integer, nullable=False)


class CheckPointManage(Base, DictBase):
    __tablename__ = 'check_point'
    attributes = ['hostname', 'dc']
    detail_attributes = attributes

    hostname = Column(String(64), primary_key=True)
    dc = Column(String(10), default='')


class ClusterManage(Base, DictBase):
    __tablename__ = 'cluster'
    attributes = ['id', 'grp_id', 'numerator', 'denominator', 'endpoint', 'metric', 'tags', 'ds_type', 'step',
                  'last_update', 'creator']
    detail_attributes = attributes

    id = Column(Integer, primary_key=True)
    grp_id = Column(Integer, nullable=False)
    numerator = Column(String(10240), nullable=False)
    denominator = Column(String(10240), nullable=False)
    endpoint = Column(String(255), nullable=False)
    metric = Column(String(255), nullable=False)
    tags = Column(String(255), nullable=False)
    ds_type = Column(String(255), nullable=False)
    step = Column(Integer, nullable=False)
    last_update = Column(DateTime, nullable=False, default=datetime.datetime.now())
    creator = Column(String(255), nullable=False)


class CmdbSYSManage(Base, DictBase):
    __tablename__ = 'cmdb_sys'
    __table_args__ = {'schema': 'falcon_portal'}
    attributes = ['uuid', 'ip', 'stack', 'system', 'app', 'create_time', 'business_owner', 'develop_owner',
                  'test_owner', 'service_owner']
    detail_attributes = attributes
    summary_attributes = ['stack', 'system', 'app']

    uuid = Column(String(255), primary_key=True)
    ip = Column(String(16), default='')
    stack = Column(String(100), default='')
    system = Column(String(100), default='')
    app = Column(String(100), default='')
    create_time = Column(String(100), default='')
    business_owner = Column(String(50), default='')
    develop_owner = Column(String(50), default='')
    test_owner = Column(String(50), default='')
    service_owner = Column(String(50), default='')


class CmdbSYSSecManage(Base, DictBase):
    __tablename__ = 'cmdb_sys_sec'
    attributes = ['uuid', 'ip', 'stack', 'system', 'app', 'create_time', 'business_owner', 'develop_owner',
                  'test_owner', 'service_owner']
    detail_attributes = attributes

    uuid = Column(String(255), primary_key=True)
    ip = Column(String(16), default='')
    stack = Column(String(100), default='')
    system = Column(String(100), default='')
    app = Column(String(100), default='')
    create_time = Column(String(100), default='')
    business_owner = Column(String(50), default='')
    develop_owner = Column(String(50), default='')
    test_owner = Column(String(50), default='')
    service_owner = Column(String(50), default='')


class ConfigKVManage(Base, DictBase):
    __tablename__ = 'config_kv'
    attributes = ['c_key', 'c_value']
    detail_attributes = attributes

    c_key = Column(String(255), primary_key=True)
    c_value = Column(String(255), default='')


class CounterManage(Base, DictBase):
    __tablename__ = "counter"
    attributes = ["counter", "note", "right_value", "asset_id"]
    detail_attributes = attributes

    counter = Column(String(255), primary_key=True)
    note = Column(String(128), default='')
    right_value = Column(String(64), default='')
    asset_id = Column(String(255))


class CustomManage(Base, DictBase):
    __tablename__ = 'custom'
    attributes = ['uuid', 'env_type', 'create_user', 'create_at', 'update_user', 'update_at', 'tenant_id', 'project_id',
                  'tenant', 'project', 'provider', 'region_id', 'az_id', "region", "az",
                  'host_info', 'environment', 'user_info']
    detail_attributes = attributes

    uuid = Column(String(36), primary_key=True)
    env_type = Column(String(32), ForeignKey('environment.id'), nullable=False, default='')
    create_user = Column(String(64), ForeignKey('uic.user.uid'), nullable=False, default='')
    create_at = Column(DateTime, nullable=False, default=datetime.datetime.now())
    update_user = Column(String(64), nullable=False, default=None)
    update_at = Column(DateTime, nullable=True)
    tenant_id = Column(String(32), ForeignKey("iam_tenant.uuid"), nullable=False)
    project_id = Column(String(32), ForeignKey("if_project.id"), nullable=False)
    provider = Column(String(32), nullable=True)
    region_id = Column(String(32), ForeignKey("if_region.id"), nullable=True)
    az_id = Column(String(32), ForeignKey("available_zone.id"), nullable=True)

    tenant = relationship('Tenant', lazy='select')
    project = relationship('Project', lazy='select')
    region = relationship('Region', lazy='select')
    az = relationship('AvailableZone', lazy='select')
    # host_info = relationship("Host", lazy='select')
    environment = relationship('EnvironmentManage', lazy='select')
    user_info = relationship('UserManage', lazy='select')
    host_info = relationship(u'Host',
                             primaryjoin='and_(foreign(CustomManage.uuid) == Host.hostname)',
                             lazy='select',
                             viewonly=True,
                             uselist=False)


class CustomAlertManage(Base, DictBase):
    __tablename__ = 'custom_alert'
    attributes = ['id', 'name', 'alert_msg', 'cur_count', 'is_close', 'al_level', 'req_type', 'update_time',
                  'alert_user']
    detail_attributes = attributes

    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    alert_msg = Column(String(2000), default='')
    cur_count = Column(Integer, nullable=False, default=1)
    is_close = Column(Integer, nullable=False, default=0)
    al_level = Column(Integer, nullable=False, default=0)
    req_type = Column(String(50), default='')
    update_time = Column(DateTime, default=datetime.datetime.now())
    alert_user = Column(String(500), default='')


class CustomCounterManage(Base, DictBase):
    __tablename__ = 'custom_counter'
    attributes = ['id', 'host_id', 'counter', 'step', 'type', 't_modify', 'u_modify']
    detail_attributes = attributes

    id = Column(Integer, primary_key=True)
    host_id = Column(Integer, nullable=False)
    counter = Column(String(255), nullable=False, default='')
    step = Column(Integer, nullable=False, default=60)
    type = Column(String(16), nullable=False)
    t_modify = Column(DateTime, nullable=False, default=datetime.datetime.now())
    u_modify = Column(String(50))


class ExpressionManage(Base, DictBase):
    __tablename__ = 'expression'
    attributes = ['id', 'expression', 'func', 'op', 'right_value', 'max_step', 'priority',
                  'note', 'action_id', 'create_user', 'pause']
    detail_attributes = attributes

    id = Column(Integer, primary_key=True)
    expression = Column(String(1024), nullable=False)
    func = Column(String(16), nullable=False, default='all(#1)')
    op = Column(String(8), nullable=False, default='')
    right_value = Column(String(16), nullable=False, default='')
    max_step = Column(Integer, nullable=False, default=1)
    priority = Column(Integer, nullable=False, default=0)
    note = Column(String(1024), nullable=False, default='')
    action_id = Column(Integer, nullable=False, default=0)
    create_user = Column(String(64), nullable=False, default='')
    pause = Column(Integer, nullable=False, default=0)


class GRPManage(Base, DictBase):
    __tablename__ = 'grp'
    attributes = ['id', 'grp_name', 'create_user', 'create_at', 'come_from', 'update_user', 'update_at', 'tenant_id',
                  'project_id', 'tenant', 'project']
    detail_attributes = attributes

    id = Column(Integer, primary_key=True)
    grp_name = Column(String(255), nullable=False, default='')
    create_user = Column(String(64), nullable=False, default='')
    create_at = Column(DateTime, nullable=False, default=datetime.datetime.now())
    come_from = Column(Integer, nullable=False, default=0)
    update_user = Column(String(64), nullable=True)
    update_at = Column(DateTime, nullable=True)
    tenant_id = Column(String(32), ForeignKey("iam_tenant.uuid"), nullable=False)
    project_id = Column(String(32), ForeignKey("if_project.id"), nullable=False)

    tenant = relationship('Tenant', lazy='select')
    project = relationship('Project', lazy='select')


class GRPHostManage(Base, DictBase):
    __tablename__ = 'grp_host'
    attributes = ['grp_id', 'host_id']
    detail_attributes = attributes

    # id = Column(Integer, primary_key=True)
    grp_id = Column(Integer, nullable=False, primary_key=True)
    host_id = Column(Integer, nullable=False, primary_key=True)


class TPLHostManage(Base, DictBase):
    __tablename__ = 'tpl_host'
    attributes = ['tpl_id', 'host_id']
    detail_attributes = attributes

    tpl_id = Column(Integer, nullable=False, primary_key=True)
    host_id = Column(Integer, nullable=False, primary_key=True)


class GRPHostnameManage(Base, DictBase):
    __tablename__ = 'grp_hostname'
    attributes = ['id', 'grp_id', 'hostname']
    detail_attributes = attributes

    id = Column(Integer, primary_key=True)
    grp_id = Column(Integer, nullable=False)
    hostname = Column(String(255), nullable=False)


class GRPTplManage(Base, DictBase):
    __tablename__ = 'grp_tpl'
    attributes = ['grp_id', 'tpl_id', 'bind_user']
    detail_attributes = attributes

    # id = Column(Integer, primary_key=True)
    grp_id = Column(Integer, nullable=False, primary_key=True)
    tpl_id = Column(Integer, nullable=False, primary_key=True)
    bind_user = Column(String(64), nullable=False, default='')
    bind_user_old = Column(String(64), default='')


class HolidayManage(Base, DictBase):
    __tablename__ = 'holiday'
    attributes = ['id', 'h_day']
    detail_attributes = attributes

    id = Column(Integer, primary_key=True)
    h_day = Column(String(20))


class HostMaintainingManage(Base, DictBase):
    __tablename__ = 'host_maintaining'
    attributes = ['id', 'endpoint', 'operator', 'metrics', 'is_deleted', 'start_time', 'end_time', 'deleted_time',
                  'shield_msg']
    detail_attributes = attributes

    id = Column(Integer, primary_key=True)
    endpoint = Column(String(64), nullable=False)
    operator = Column(String(50))
    metrics = Column(String(255))
    is_deleted = Column(Integer, default=0)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    deleted_time = Column(DateTime)
    shield_msg = Column(String(255))


class HostTplManage(Base, DictBase):
    __tablename__ = 'host_tpl'
    attributes = ['id', 'name', 'host_id', 'action_id', 'create_user', 'create_at', 'hostname', 'update_user',
                  'update_at', 'tenant_id', 'project_id', 'tenant', 'project']
    detail_attributes = attributes

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, default='')
    host_id = Column(Integer, nullable=False, default=0)
    action_id = Column(Integer, nullable=False, default=0)
    create_user = Column(String(64), nullable=False, default='')
    update_user = Column(String(64), nullable=False, default='')
    create_at = Column(DateTime, nullable=False, default=datetime.datetime.now())
    update_at = Column(DateTime, nullable=True)
    hostname = Column(String(255), default='')
    project_id = Column(String(32), ForeignKey('if_project.id'))
    tenant_id = Column(String(64), ForeignKey('iam_tenant.uuid'))

    tenant = relationship('Tenant', lazy='select')
    project = relationship('Project', lazy='select')


class LastPluginVManage(Base, DictBase):
    __tablename__ = 'last_plugin_v'
    attributes = ['id', 'last_plugin_version']
    detail_attributes = attributes

    id = Column(Integer, primary_key=True)
    last_plugin_version = Column(String(128), nullable=False, default='')


class MaintainCounterManage(Base, DictBase):
    __tablename__ = 'maintain_counter'
    attributes = ['id', 'hostname', 'counter', 'host']
    detail_attributes = attributes

    id = Column(Integer, primary_key=True)
    hostname = Column(String(255), ForeignKey("falcon_portal.host.hostname"), nullable=False)
    counter = Column(String(5000))

    host = relationship("Host", lazy='select')


class NetPodsConfigManage(Base, DictBase):
    __tablename__ = 'net_pods_config'
    attributes = ['id', 'pod', 'device', 'x_position', 'y_position', 'update_user', 'update_at']
    detail_attributes = attributes

    id = Column(Integer, primary_key=True)
    pod = Column(String(255), nullable=False)
    device = Column(String(255), default='')
    x_position = Column(String(50), default='0')
    y_position = Column(String(50), default='0')
    update_user = Column(String(50), default='')
    update_at = Column(DateTime, nullable=False, default=datetime.datetime.now())


class NetlineYSConfigManage(Base, DictBase):
    __tablename__ = 'netline_ys_config'
    attributes = ['id', 'name', 'desc']
    detail_attributes = attributes

    id = Column(Integer, primary_key=True)
    name = Column(String(255), default='')
    desc = Column(String(255), default='')


class PluginDirManage(Base, DictBase):
    __tablename__ = 'plugin_dir'
    attributes = ['id', 'grp_id', 'dir', 'create_user', 'create_at']
    detail_attributes = attributes

    id = Column(Integer, primary_key=True)
    grp_id = Column(Integer, nullable=False)
    dir = Column(String(255), nullable=False)
    create_user = Column(String(64), nullable=False, default='')
    create_at = Column(DateTime, nullable=False, default=datetime.datetime.now())


class StorageAlertManage(Base, DictBase):
    __tablename__ = 'storage_alert'
    attributes = ['id', 'alert_msg', 'cur_count', 'is_close', 'al_level', 'update_time', 'req_type']
    detail_attributes = attributes

    id = Column(Integer, primary_key=True)
    alert_msg = Column(String(2000), default='')
    cur_count = Column(Integer, nullable=False, default=1)
    is_close = Column(Integer, nullable=False, default=0)
    al_level = Column(Integer, nullable=False, default=0)
    update_time = Column(DateTime, nullable=False, default=datetime.datetime.now())
    req_type = Column(String(50))


class StorageCMDBManage(Base, DictBase):
    __tablename__ = 'storage_cmdb'
    attributes = ['id', 'snnum', 'device_type', 'ip', 't_modify', 'data_type']
    detail_attributes = attributes

    id = Column(Integer, primary_key=True)
    snnum = Column(String(100), nullable=False, default='')
    device_type = Column(String(255))
    ip = Column(String(50))
    t_modify = Column(DateTime, nullable=False, default=datetime.datetime.now())
    data_type = Column(String(50), default='')


class StorageStrategyManage(Base, DictBase):
    __tablename__ = 'storage_strategy'
    attributes = ['id', 'snnum', 'c_key', 'c_value', 'c_re', 'alarm_msg', 't_modify']
    detail_attributes = attributes

    id = Column(Integer, primary_key=True)
    snnum = Column(String(100), nullable=False, default='')
    c_key = Column(String(255))
    c_value = Column(String(255))
    c_re = Column(String(255))
    alarm_msg = Column(String(255))
    t_modify = Column(DateTime, nullable=False, default=datetime.datetime.now())


class StrategyManage(Base, DictBase):
    __tablename__ = 'strategy'
    attributes = ['id', 'metric', 'tags', 'max_step', 'priority', 'func', 'op', 'right_value', 'note', 'run_begin',
                  'run_end', 'tpl_id', 'tenant_id', 'project_id', 'tenant', 'project', 'envs']
    detail_attributes = attributes

    id = Column(Integer, primary_key=True)
    metric = Column(String(128), nullable=False, default='')
    tags = Column(String(256), nullable=False, default='')
    max_step = Column(Integer, nullable=False, default=1)
    priority = Column(Integer, nullable=False, default=0)
    func = Column(String(16), nullable=False, default='all(#1)')
    op = Column(String(8), nullable=False, default='')
    right_value = Column(String(64), nullable=False)
    note = Column(String(128), nullable=False, default='')
    run_begin = Column(String(16), nullable=False, default='')
    run_end = Column(String(16), nullable=False, default='')
    tpl_id = Column(Integer, nullable=False, default=0)
    tenant_id = Column(String(32), ForeignKey('iam_tenant.uuid'), nullable=False)
    project_id = Column(String(32), ForeignKey('if_project.id'), nullable=False)
    envs = Column(String(256), nullable=False, default='')

    tenant = relationship('Tenant', lazy='select')
    project = relationship('Project', lazy='select')


class StrategyCallbackManage(Base, DictBase):
    __tablename__ = 'strategy_callback'
    attributes = ['strategy_id', 'callback_id', 'callback_name', 'callback_type', 'update_at', 'update_user',
                  'last_active_time', 'active_count', 'success_count', 'env_enable']
    detail_attributes = attributes

    strategy_id = Column(Integer, primary_key=True)
    callback_id = Column(Integer, default=0)
    callback_name = Column(String(50), default='')
    callback_type = Column(String(50), default='')
    update_at = Column(DateTime, nullable=True)
    update_user = Column(String(50), default='')
    last_active_time = Column(DateTime, nullable=False, default=datetime.datetime.now())
    active_count = Column(Integer, default=0)
    success_count = Column(Integer, default=0)
    env_enable = Column(Integer, default=0)


class ServiceCatalogManage(Base, DictBase):
    __tablename__ = 'service_catalog'
    attributes = detail_attributes = summary_attributes = ['id', 'name']

    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False)


class TPLManage(Base, DictBase):
    __tablename__ = 'tpl'
    attributes = ['id', 'tpl_name', 'parent_id', 'action_id', 'create_user', 'create_at', 'update_user',
                  'update_at', 'tenant_id', 'project_id', 'tenant', 'project', 'asset_id']
    detail_attributes = attributes
    summary_attributes = ['id', 'tpl_name']

    id = Column(Integer, primary_key=True)
    tpl_name = Column(String(255), nullable=False, default='')
    parent_id = Column(Integer, nullable=False, default=0)
    action_id = Column(Integer, nullable=False, default=0)
    create_user = Column(String(64), nullable=False, default='')
    create_at = Column(DateTime, nullable=False, default=datetime.datetime.now())
    update_user = Column(String(64), nullable=True)
    update_at = Column(DateTime, nullable=True)
    tenant_id = Column(String(32), ForeignKey('iam_tenant.uuid'), nullable=False)
    project_id = Column(String(32), ForeignKey('if_project.id'), nullable=False)
    asset_id = Column(Integer)

    tenant = relationship('Tenant', lazy='select')
    project = relationship('Project', lazy='select')


class AssetTPLManage(Base, DictBase):
    """
    资源绑定模板使用 限制返回模板的字段 提高查询效率
    """
    __tablename__ = 'tpl'
    __table_args__ = {'schema': 'falcon_portal'}
    attributes = detail_attributes = summary_attributes = ['id', 'tpl_name', 'tenant_id', 'project_id']

    id = Column(Integer, primary_key=True)
    tpl_name = Column(String(255), nullable=False, default='')
    parent_id = Column(Integer, nullable=False, default=0)
    action_id = Column(Integer, nullable=False, default=0)
    create_user = Column(String(64), nullable=False, default='')
    create_at = Column(DateTime, nullable=False, default=datetime.datetime.now())
    update_user = Column(String(64), nullable=True)
    update_at = Column(DateTime, nullable=True)
    tenant_id = Column(String(32), nullable=False)
    project_id = Column(String(32), nullable=False)


class UnitManage(Base, DictBase):
    __tablename__ = 'unit'
    attributes = ['id', 'metric', 'unit', 'note']
    detail_attributes = attributes

    id = Column(Integer, primary_key=True)
    metric = Column(String(255))
    unit = Column(String(64), nullable=False, default='')
    note = Column(String(255), nullable=False, default='')


class UpgrateAgentVersionManage(Base, DictBase):
    __tablename__ = 'upgrate_agent_version'
    attributes = ['id', 'agent_version', 'vmtype']
    detail_attributes = attributes

    id = Column(Integer, primary_key=True)
    agent_version = Column(String(50), nullable=False, default='')
    vmtype = Column(String(50), nullable=False, default='linux')


class UrlMonitorManage(Base, DictBase):
    __tablename__ = 'url_monitor'
    attributes = ['url', 'cname']
    detail_attributes = attributes

    url = Column(String(255), primary_key=True)
    cname = Column(String(255), nullable=False, default='')


class UserHostManage(Base, DictBase):
    __tablename__ = 'user_host'
    attributes = ['id', 'userid', 'host_id']
    detail_attributes = attributes

    id = Column(Integer, primary_key=True)
    userid = Column(Integer)
    host_id = Column(Integer, nullable=False)


class SystemGroupManage(Base, DictBase):
    __tablename__ = 'system_group'
    attributes = ['id', 'name', 'name_cn', 'tenant_id', 'source_id', 'description', 'create_time', 'update_time',
                  'source_corel_id', 'tag', 'tenant']
    detail_attributes = attributes
    summary_attributes = attributes
    table_column = ['id', 'name', 'name_cn', 'tenant_id', 'source_id', 'description', 'create_time', 'update_time',
                    'source_corel_id', 'tag']
    update_column = ['name', 'name_cn', 'tenant_id', 'source_id', 'description', 'source_corel_id', 'tag']

    id = Column(String(63), primary_key=True)
    name = Column(String(63), nullable=False)
    name_cn = Column(String(63), nullable=False)
    tenant_id = Column(String(63), ForeignKey("iam_tenant.uuid"), nullable=False)
    source_id = Column(String(63), nullable=False)
    description = Column(String(255))
    create_time = Column(DateTime, nullable=False)
    update_time = Column(DateTime)
    source_corel_id = Column(String(63))
    tag = Column(String(63), nullable=False, default='system_group')

    tenant = relationship('Tenant', lazy='select')


class SystemManage(Base, DictBase):
    __tablename__ = 'system'
    attributes = ['id', 'name', 'name_cn', 'tenant_id', 'source_id', 'description', 'create_time', 'update_time',
                  'source_corel_id', 'tag', 'systemgroup_id', 'system_group']
    detail_attributes = attributes
    summary_attributes = attributes
    table_column = ['id', 'name', 'name_cn', 'tenant_id', 'source_id', 'description', 'create_time', 'update_time',
                    'source_corel_id', 'tag', 'systemgroup_id']
    update_column = ['name', 'name_cn', 'tenant_id', 'source_id', 'description',
                     'source_corel_id', 'tag', 'systemgroup_id']

    id = Column(String(63), primary_key=True)
    name = Column(String(63), nullable=False)
    name_cn = Column(String(63), nullable=False)
    tenant_id = Column(String(63), ForeignKey("iam_tenant.uuid"), nullable=False)
    systemgroup_id = Column(String(63), ForeignKey("system_group.id"), nullable=False)
    source_id = Column(String(63), nullable=False)
    description = Column(String(255))
    create_time = Column(DateTime, nullable=False)
    update_time = Column(DateTime)
    source_corel_id = Column(String(63))
    tag = Column(String(63), nullable=False, default='system')

    # tenant = relationship('Tenant', lazy='select')
    system_group = relationship('SystemGroupManage', lazy='select')


class SubSystemManage(Base, DictBase):
    __tablename__ = 'subsystem'
    attributes = ['id', 'name', 'name_cn', 'tenant_id', 'source_id', 'description', 'create_time', 'update_time',
                  'source_corel_id', 'tag', 'systemgroup_id', 'service_windows',
                  'development_owner', 'test_owner', 'operation_owner', 'system_id', 'status', 'level', 'system']
    detail_attributes = attributes
    summary_attributes = attributes
    table_column = ['id', 'name', 'name_cn', 'tenant_id', 'source_id', 'description', 'create_time', 'update_time',
                    'source_corel_id', 'tag', 'systemgroup_id', 'service_windows',
                    'development_owner', 'test_owner', 'operation_owner', 'system_id', 'status', 'level']
    update_column = ['id', 'name', 'name_cn', 'tenant_id', 'source_id', 'description',
                     'source_corel_id', 'tag', 'systemgroup_id', 'service_windows',
                     'development_owner', 'test_owner', 'operation_owner', 'system_id', 'status', 'level']

    id = Column(String(63), primary_key=True)
    name = Column(String(63), nullable=False)
    name_cn = Column(String(63), nullable=False)
    tenant_id = Column(String(63), ForeignKey("iam_tenant.uuid"), nullable=False)
    systemgroup_id = Column(String(63), ForeignKey("system_group.id"), nullable=False)
    system_id = Column(String(63), ForeignKey("system.id"), nullable=False)
    source_id = Column(String(63), nullable=False)
    description = Column(String(255))
    create_time = Column(DateTime, nullable=False)
    update_time = Column(DateTime)
    source_corel_id = Column(String(63))
    development_owner = Column(String(63))
    test_owner = Column(String(63))
    operation_owner = Column(String(63))
    status = Column(String(63))
    level = Column(String(63))
    service_windows = Column(String(63))
    tag = Column(String(63), default='subsystem')

    # tenant = relationship('Tenant', lazy='select')
    # system_group = relationship('SystemGroupManage', lazy='select')
    system = relationship('SystemManage', lazy='select')


class PublishUnitManage(Base, DictBase):
    __tablename__ = 'publish_unit'
    attributes = ['id', 'name', 'name_cn', 'tenant_id', 'source_id', 'description', 'create_time', 'update_time',
                  'source_corel_id', 'tag', 'systemgroup_id', 'zone_name', 'type_name',
                  'system_id', 'subsystem_id', 'subsystem']
    detail_attributes = attributes
    summary_attributes = attributes
    table_column = ['id', 'name', 'name_cn', 'tenant_id', 'source_id', 'description', 'create_time', 'update_time',
                    'source_corel_id', 'tag', 'systemgroup_id', 'zone_name', 'type_name',
                    'system_id', 'subsystem_id']
    update_column = ['id', 'name', 'name_cn', 'tenant_id', 'source_id', 'description',
                     'source_corel_id', 'tag', 'systemgroup_id', 'zone_name', 'type_name',
                     'system_id', 'subsystem_id']

    id = Column(String(63), primary_key=True)
    name = Column(String(63), nullable=False)
    name_cn = Column(String(255), nullable=False)
    tenant_id = Column(String(63), ForeignKey("iam_tenant.uuid"))
    systemgroup_id = Column(String(63), ForeignKey("system_group.id"))
    system_id = Column(String(63), ForeignKey("system.id"))
    subsystem_id = Column(String(63), ForeignKey("subsystem.id"), nullable=False)
    source_id = Column(String(63))
    description = Column(String(255))
    create_time = Column(DateTime)
    update_time = Column(DateTime)
    source_corel_id = Column(String(63))
    zone_name = Column(String(63))
    type_name = Column(String(63))
    tag = Column(String(63), default='unit')

    # tenant = relationship('Tenant', lazy='select')
    # system_group = relationship('SystemGroupManage', lazy='select')
    # system = relationship('SystemManage', lazy='select')
    subsystem = relationship('SubSystemManage', lazy='select')


class UnitInstanceManage(Base, DictBase):
    __tablename__ = 'unit_instance'
    attributes = ['id', 'type', 'host_id', 'create_time', 'update_time', 'port', 'status', 'unit_id', 'host_ip',
                  'system_id', 'subsystem_id', 'systemgroup_id', 'tenant_id', 'tag', 'description', 'source_id',
                  'source_corel_id', 'name', 'name_cn', 'unit']
    detail_attributes = attributes
    table_column = ['id', 'type', 'host_id', 'create_time', 'update_time', 'port', 'status', 'unit_id', 'host_ip',
                    'system_id', 'subsystem_id', 'systemgroup_id', 'tenant_id', 'tag', 'description', 'source_id',
                    'source_corel_id', 'name', 'name_cn']
    update_column = ['id', 'type', 'host_id', 'port', 'status', 'unit_id', 'host_ip',
                     'system_id', 'subsystem_id', 'systemgroup_id', 'tenant_id', 'tag', 'description', 'source_id',
                     'source_corel_id', 'name', 'name_cn']

    id = Column(String(63), primary_key=True)
    type = Column(String(63), nullable=False)
    host_id = Column(String(63))
    create_time = Column(DateTime, nullable=False)
    update_time = Column(DateTime)
    port = Column(String(63))
    status = Column(String(63), nullable=False)
    tenant_id = Column(String(63), ForeignKey("iam_tenant.uuid"))
    systemgroup_id = Column(String(63), ForeignKey("system_group.id"))
    system_id = Column(String(63), ForeignKey("system.id"))
    subsystem_id = Column(String(63), ForeignKey("subsystem.id"))
    unit_id = Column(String(63), ForeignKey("publish_unit.id"))
    description = Column(String(255))
    source_id = Column(String(63), nullable=False)
    host_ip = Column(String(63))
    source_corel_id = Column(String(63))
    name = Column(String(63))
    name_cn = Column(String(255))
    tag = Column(String(63), default='unit_instance')

    # tenant = relationship('Tenant', lazy='select')
    # system_group = relationship('SystemGroupManage', lazy='select')
    # system = relationship('SystemManage', lazy='select')
    # subsystem = relationship('SubSystemManage', lazy='select')
    unit = relationship('PublishUnitManage', lazy='select')


class IamPolicyManage(Base, DictBase):
    __tablename__ = 'iam_policy'
    attributes = ['id', 'url', 'method', 'name', 'is_default', 'create_time', 'update_time']
    detail_attributes = attributes
    table_column = ['id', 'url', 'method', 'name', 'is_default', 'create_time', 'update_time']

    id = Column(Integer, primary_key=True)
    url = Column(String(100), nullable=False)
    method = Column(String(36), nullable=False)
    name = Column(String(64), nullable=False)
    is_default = Column(Integer, default=0)
    is_deleted = Column(Integer, default=0)
    create_time = Column(DateTime, nullable=False, default=datetime.datetime.now())
    update_time = Column(DateTime)


# uic数据库中的表
class SessionManage(Base, DictBase):
    __tablename__ = 'session'
    attributes = ['id', 'uid', 'sig', 'expired']
    detail_attributes = attributes

    id = Column(Integer, primary_key=True)
    uid = Column(Integer, nullable=False)
    sig = Column(String(32), nullable=False, default='')
    expired = Column(Integer, nullable=False)


# uic数据库中的user表
class UserManage(Base, DictBase):
    __tablename__ = 'user'
    __table_args__ = {'schema': 'uic'}
    attributes = ['id', 'name', 'cnname', 'email', 'phone', 'created', 'uid']
    detail_attributes = attributes

    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)
    passwd = Column(String(64), nullable=False, default='')
    cnname = Column(String(128), nullable=False, default='')
    email = Column(String(255), nullable=False, default='')
    phone = Column(String(16), nullable=False, default='')
    im = Column(String(32), nullable=False, default='')
    qq = Column(String(16), nullable=False, default='')
    uid = Column(String(64), nullable=False, default='')
    role = Column(Integer, nullable=False, default=0)
    creator = Column(Integer, nullable=False, default=0)
    created = Column(DateTime, nullable=False, default=datetime.datetime.now())


# uic数据库中的rel_action_user表
class RelActionUserManage(Base, DictBase):
    __tablename__ = 'rel_action_user'
    __table_args__ = {'schema': 'uic'}
    attributes = ['id', 'action_id', 'uic_id']
    detail_attributes = attributes

    id = Column(Integer, primary_key=True)
    action_id = Column(Integer, nullable=False)
    uic_id = Column(String(32), nullable=False, default='')


# alarms数据库中的表
class EventCasesManage(Base, DictBase):
    __tablename__ = 'event_cases'
    __table_args__ = {'schema': 'alarms'}

    attributes = ['id', 'endpoint', 'metric', 'func', 'cond', 'note', 'max_step', 'current_step', 'priority', 'status',
                  'timestamp', 'update_at', 'closed_at', 'closed_note', 'user_modified', 'tpl_creator', 'expression_id',
                  'strategy_id', 'template_id', 'process_note', 'process_status', 'host_info',
                  'project', 'tenant', 'az', 'source_type', 'project_id', 'tenant_id']
    detail_attributes = attributes
    summary_attributes = attributes

    id = Column(String(50), primary_key=True)
    endpoint = Column(String(100), ForeignKey('falcon_portal.host.hostname'), nullable=False)
    metric = Column(String(200))
    func = Column(String(50))
    cond = Column(String(200))
    note = Column(String(500))
    max_step = Column(INT)
    current_step = Column(INT)
    priority = Column(INT, nullable=False)
    status = Column(String(20), nullable=False)
    timestamp = Column(DateTime, nullable=False)
    update_at = Column(DateTime)
    closed_at = Column(DateTime)
    closed_note = Column(String(250))
    user_modified = Column(INT)
    tpl_creator = Column(String(64))
    expression_id = Column(INT)
    strategy_id = Column(INT)
    template_id = Column(INT)
    process_note = Column(INT)
    process_status = Column(String(20))
    project_id = Column(String(32), ForeignKey('falcon_portal.if_project.id'), nullable=False, default='')
    tenant_id = Column(String(64), ForeignKey('falcon_portal.iam_tenant.uuid'))
    az_id = Column(String(36), ForeignKey('falcon_portal.available_zone.id'), nullable=False, default='')
    source_type = Column(String(20), default='')

    host_info = relationship('Host', lazy='select')
    project = relationship('CapacityProject', lazy='select')
    tenant = relationship('CapacityTenant', lazy='select')
    az = relationship('CapacityAvailableZone', lazy='select')


class AlarmNoteManage(Base, DictBase):
    """
    告警处置记录备注
    """
    __tablename__ = 'alarm_note'
    __table_args__ = {'schema': 'alarms'}
    attributes = ['event_case_id', 'timestamp', 'creator', 'alarm_note']
    detail_attributes = attributes

    id = Column(Integer, primary_key=True)
    event_case_id = Column(String(50), default='')
    timestamp = Column(DateTime, nullable=False, default=datetime.datetime.now())
    creator = Column(String(50), default='')
    alarm_note = Column(String(200), default='')


# alarms数据库中的表
class AlarmStatusManage(Base, DictBase):
    __tablename__ = 'alarm_status'
    attributes = ['id', 'endpoint', 'ip', 'user', 'pid', 'cpu', 'mem', 'disk_r', 'disk_w', 'swapin', 'io', 'start',
                  'p_time', 'command', 'update_at']
    detail_attributes = attributes

    id = Column(Integer, primary_key=True)
    endpoint = Column(String(255), nullable=False, default='')
    ip = Column(String(16), nullable=False, default='')
    user = Column(String(32), nullable=False, default='')
    pid = Column(Integer, nullable=False, default=0)
    cpu = Column(Integer, nullable=False, default=0)
    mem = Column(Integer, nullable=False, default=0)
    disk_r = Column(String(32), nullable=False, default='')
    disk_w = Column(String(32), nullable=False, default='')
    swapin = Column(String(32), nullable=False, default='')
    io = Column(String(32), nullable=False, default='')
    start = Column(String(32), nullable=False, default='')
    p_time = Column(String(32), nullable=False, default='')
    command = Column(String(500), nullable=False, default='')
    update_at = Column(DateTime, nullable=False, default=datetime.datetime.now())


# alarms数据库中的表
class DelLogManage(Base, DictBase):
    __tablename__ = 'del_log'
    attributes = ['id', 'event_cases_id', 'endpoint', 'metric', 'func', 'cond', 'max_step', 'current_step', 'timestamp',
                  'strategy_id', 'del_msg', 'del_user', 'del_time', 'priority', 'note']
    detail_attributes = attributes

    id = Column(Integer, primary_key=True)
    event_cases_id = Column(String(50), nullable=False)
    endpoint = Column(String(100))
    metric = Column(String(200))
    func = Column(String(50))
    cond = Column(String(200))
    max_step = Column(Integer)
    current_step = Column(Integer)
    timestamp = Column(String(30))
    strategy_id = Column(Integer)
    del_msg = Column(String(500))
    del_user = Column(String(100))
    del_time = Column(DateTime, default=datetime.datetime.now())
    priority = Column(Integer, default=1)
    note = Column(String(500), default='')


# alarms数据库中的表
class EventReportManage(Base, DictBase):
    __tablename__ = 'event_report'
    attributes = ['id', 'endpoint', 'hostname', 'ip', 'metric', 'note', 'tags', 'priority', 'func', 'start_cond',
                  'start_time', 'end_cond', 'end_time', 'strategy_id', 'template_id', 'stack', 'system', 'app',
                  'is_del', 'del_msg', 'del_user', 'del_time', 'data_time', 'update_at']
    detail_attributes = attributes

    id = Column(String(50), primary_key=True)
    endpoint = Column(String(100), nullable=False)
    hostname = Column(String(50))
    ip = Column(String(50))
    metric = Column(String(200), nullable=False)
    note = Column(String(500))
    tags = Column(String(200))
    priority = Column(Integer, nullable=False)
    func = Column(String(50))
    start_cond = Column(String(200))
    start_time = Column(String(50))
    end_cond = Column(String(200))
    end_time = Column(String(50))
    strategy_id = Column(Integer)
    template_id = Column(Integer)
    stack = Column(String(100))
    system = Column(String(100))
    app = Column(String(100))
    is_del = Column(Integer)
    del_msg = Column(String(500))
    del_user = Column(String(100))
    del_time = Column(String(50))
    data_time = Column(String(50))
    update_at = Column(DateTime, nullable=False, default=datetime.datetime.now())


# alarms数据库中的表
class EventsManage(Base, DictBase):
    __tablename__ = 'events'
    __table_args__ = {'schema': 'alarms'}
    attributes = ['id', 'event_caseId', 'step', 'cond', 'status', 'timestamp', 'event_cases']
    detail_attributes = attributes

    id = Column(Integer, primary_key=True)
    event_caseId = Column(String(50), ForeignKey('alarms.event_cases.id'))
    step = Column(Integer)
    cond = Column(String(200), nullable=False)
    status = Column(Integer, default=0)
    timestamp = Column(DateTime, nullable=False, default=datetime.datetime.now())
    event_cases = relationship('EventCasesManage', lazy='select')


# alarms数据库中的表
class RemarkCommonManage(Base, DictBase):
    __tablename__ = 'remark_common'
    attributes = ['id', 'remark', 'update_at']
    detail_attributes = attributes

    id = Column(Integer, primary_key=True)
    remark = Column(String(255), nullable=False)
    update_at = Column(DateTime)


# dashboard数据库中的表
class ButtonManage(Base, DictBase):
    __tablename__ = 'button'
    attributes = ['id', 'group_id', 'name', 'b_type', 'b_text', 'refresh_panels', 'refresh_charts', 'option_group',
                  'refresh_button']
    detail_attributes = attributes

    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, nullable=False, default=0)
    name = Column(String(50), nullable=False, default='')
    b_type = Column(String(50), nullable=False, default='')
    b_text = Column(String(50), nullable=False, default='')
    refresh_panels = Column(Integer, nullable=False, default=0)
    refresh_charts = Column(Integer, nullable=False, default=0)
    option_group = Column(Integer, default=0)
    refresh_button = Column(Integer, default=0)


# dashboard数据库中的表
class ChartManage(Base, DictBase):
    __tablename__ = 'chart'
    attributes = ['id', 'group_id', 'endpoint', 'metric', 'col', 'url', 'unit', 'title',
                  'grid_type', 'series_name', 'rate', 'agg_type', 'legend']
    detail_attributes = attributes

    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, nullable=False, default=0)
    endpoint = Column(String(2000), default='')
    metric = Column(String(2000), default='')
    col = Column(Integer, default=6)
    url = Column(String(200), default='')
    unit = Column(String(50), default='')
    title = Column(String(100), default='')
    grid_type = Column(String(20), default='line')
    series_name = Column(String(50), default='metric')
    rate = Column(Integer, default=0)
    agg_type = Column(String(20), default='avg')
    legend = Column(String(50), default='')


# dashboard数据库中的表
class CustomDashBoardManage(Base, DictBase):
    __tablename__ = 'custom_dashboard'
    attributes = ['id', 'name', 'panels_group', 'update_user', 'update_at', 'cfg', 'is_del']
    detail_attributes = attributes

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, default='')
    panels_group = Column(Integer)
    update_user = Column(String(50), default=0)
    update_at = Column(DateTime, nullable=False, default=datetime.datetime.now())
    cfg = Column(Text)
    is_del = Column(Integer, default=0)


# dashboard数据库中的表
class DashBoardManage(Base, DictBase):
    __tablename__ = 'dashboard'
    attributes = ['id', 'dashboard_type', 'name', 'search_type', 'search_enable', 'search_id', 'button_enable',
                  'button_group', 'message_enable', 'message_group', 'message_url', 'panels_enable', 'panels_type',
                  'panels_group', 'panels_param']
    detail_attributes = attributes

    id = Column(Integer, primary_key=True)
    dashboard_type = Column(String(50), nullable=False)
    name = Column(String(255))
    search_type = Column(String(255))
    search_enable = Column(Integer, nullable=False, default=0)
    search_id = Column(Integer, default=0)
    button_enable = Column(Integer, nullable=False, default=0)
    button_group = Column(Integer, default=0)
    message_enable = Column(Integer, nullable=False, default=0)
    message_group = Column(Integer, default=0)
    message_url = Column(String(200), default='')
    panels_enable = Column(Integer, nullable=False, default=1)
    panels_type = Column(String(20), default='tabs')
    panels_group = Column(Integer, default=0)
    panels_param = Column(String(50), default='')


# dashboard数据库中的表
class DashBoardGraphManage(Base, DictBase):
    __tablename__ = 'dashboard_graph'
    attributes = ['id', 'title', 'hosts', 'counters', 'screen_id', 'timespan', 'graph_type',
                  'method', 'position', 'falcon_tags']
    detail_attributes = attributes

    id = Column(Integer, primary_key=True)
    title = Column(String(128), nullable=False)
    hosts = Column(String(10240), nullable=False, default='')
    counters = Column(String(10240), nullable=False, default='')
    screen_id = Column(Integer, nullable=False)
    timespan = Column(Integer, nullable=False, default=3600)
    graph_type = Column(String(255), nullable=False, default='h')
    method = Column(String(255), default='')
    position = Column(Integer, nullable=False, default=0)
    falcon_tags = Column(String(512), nullable=False, default='')


# dashboard数据库中的表
class DashBoardScreenManage(Base, DictBase):
    __tablename__ = 'dashboard_screen'
    attributes = ['id', 'pid', 'name', 'time']
    detail_attributes = attributes

    id = Column(Integer, primary_key=True)
    pid = Column(Integer, nullable=False, default=0)
    name = Column(String(128), nullable=False)
    time = Column(DateTime, nullable=False, default=datetime.datetime.now())


# dashboard数据库中的表
class HostScreenCFGManage(Base, DictBase):
    __tablename__ = 'host_screen_cfg'
    attributes = ['id', 'counter', 'graph_type', 'order_position', 'tag', 'rename', 'screen_type', 'os_type']
    detail_attributes = attributes

    id = Column(Integer, primary_key=True)
    counter = Column(String(50), nullable=False, default='')
    graph_type = Column(String(10), nullable=False, default='k')
    order_position = Column(Integer, nullable=False)
    tag = Column(String(100))
    rename = Column(String(100))
    screen_type = Column(String(50))
    os_type = Column(String(10), default='linux')


# dashboard数据库中的表
class MessageManage(Base, DictBase):
    __tablename__ = 'message'
    attributes = ['id', 'group_id', 'k', 'rename', 'col', 'href', 'url']
    detail_attributes = attributes

    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, nullable=False, default=0)
    k = Column(String(50), nullable=False, default='')
    rename = Column(String(50), nullable=False, default='')
    col = Column(String(100), default='')
    href = Column(Integer, nullable=False, default=0)
    url = Column(String(200), nullable=False, default='')


# dashboard数据库中的表
class OptionManage(Base, DictBase):
    __tablename__ = 'option'
    attributes = ['id', 'group_id', 'option_text', 'option_value']
    detail_attributes = attributes

    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, nullable=False, default=0)
    option_text = Column(String(100), nullable=False, default='')
    option_value = Column(String(100), nullable=False, default='')


# dashboard数据库中的表
class PanelManage(Base, DictBase):
    __tablename__ = 'panel'
    attributes = ['id', 'group_id', 'title', 'tags_enable', 'tags_url', 'tags_key', 'chart_group']
    detail_attributes = attributes

    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, nullable=False, default=0)
    title = Column(String(50), nullable=False, default='')
    tags_enable = Column(Integer, nullable=False, default=0)
    tags_url = Column(String(200), nullable=False, default='')
    tags_key = Column(String(50), default='')
    chart_group = Column(Integer, default=0)


# dashboard数据库中的表
class SearchManage(Base, DictBase):
    __tablename__ = 'search'
    attributes = ['id', 'name', 'search_url', 'search_col', 'refresh_panels', 'refresh_message']
    detail_attributes = attributes

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, default='')
    search_url = Column(String(200), nullable=False, default='')
    search_col = Column(String(50), nullable=False, default='')
    refresh_panels = Column(Integer, nullable=False, default=0)
    refresh_message = Column(Integer, nullable=False, default=0)


# dashboard数据库中的表
class TmpGraphManage(Base, DictBase):
    __tablename__ = 'tmp_graph'
    attributes = ['id', 'endpoints', 'counters', 'ck', 'time_']
    detail_attributes = attributes

    id = Column(Integer, primary_key=True)
    endpoints = Column(String(10240), nullable=False, default='')
    counters = Column(String(10240), nullable=False, default='')
    ck = Column(String(32), nullable=False)
    time_ = Column(DateTime, nullable=False, default=datetime.datetime.now())


# graph数据库中的表
class CounterTextManage(Base, DictBase):
    __tablename__ = 'counter_text'
    attributes = ['counter', 'description']
    detail_attributes = attributes

    counter = Column(String(255), primary_key=True)
    description = Column(String(255), nullable=False, default='')


# graph数据库中的表
class EndpointManage(Base, DictBase):
    __tablename__ = 'endpoint'
    attributes = ['id', 'endpoint', 'ts', 't_create', 't_modify']
    detail_attributes = attributes

    id = Column(Integer, primary_key=True)
    endpoint = Column(String(255), nullable=False, default='')
    ts = Column(Integer)
    t_create = Column(DateTime, nullable=False)
    t_modify = Column(DateTime, nullable=False)


# graph数据库中的表
class EndpointCounterManage(Base, DictBase):
    __tablename__ = 'endpoint_counter'
    attributes = ['id', 'endpoint_id', 'counter', 'step', 'type', 'ts', 't_create', 't_modify']
    detail_attributes = attributes

    id = Column(Integer, primary_key=True)
    endpoint_id = Column(Integer, nullable=False)
    counter = Column(String(255), nullable=False, default='')
    step = Column(Integer, nullable=False, default=60)
    type = Column(String(16), nullable=False)
    ts = Column(Integer)
    t_create = Column(DateTime, nullable=False)
    t_modify = Column(DateTime, nullable=False)


# graph数据库中的表
class TagEndpointManage(Base, DictBase):
    __tablename__ = 'tag_endpoint'
    attributes = ['id', 'tag', 'endpoint_id', 'ts', 't_create', 't_modify']
    detail_attributes = attributes

    id = Column(Integer, primary_key=True)
    tag = Column(String(255), nullable=False, default='')
    endpoint_id = Column(Integer, nullable=False)
    ts = Column(Integer)
    t_create = Column(DateTime, nullable=False)
    t_modify = Column(DateTime, nullable=False)


class LogCollectManage(Base, DictBase):
    __tablename__ = 'log_collect'
    attributes = ['id', 'nid', 'name', 'tags', 'collect_type', 'step', 'file_path', 'time_format', 'pattern', 'func',
                  'degree', 'func_type', 'aggregate', 'unit', 'zero_fill', 'comment', 'creator', 'created',
                  'last_updator', 'last_updated', 'collect_name', 'tpl']

    detail_attributes = attributes
    table_column = attributes

    id = Column(Integer, primary_key=True)
    nid = Column(Integer, ForeignKey('tpl.id'))
    name = Column(String(255), nullable=False, default='')
    collect_name = Column(String(255), nullable=False, default='')
    tags = Column(String(255), nullable=False, default='')
    collect_type = Column(String(64), nullable=False, default='LOG')
    step = Column(Integer, nullable=False, default=0)
    file_path = Column(String(255), nullable=False, default='')
    time_format = Column(String(128), nullable=False, default='')
    pattern = Column(String(1024), nullable=False, default='')
    func = Column(String(64), nullable=False, default='')
    degree = Column(Integer, nullable=False, default=0)
    func_type = Column(String(64), nullable=False, default='')
    aggregate = Column(String(64), nullable=False, default='')
    unit = Column(String(64), nullable=False, default='')
    zero_fill = Column(Integer, nullable=False, default=0)
    comment = Column(String(512), nullable=False, default='')
    creator = Column(String(255), nullable=False, default='')
    created = Column(DateTime)
    last_updator = Column(String(255), nullable=False, default='')
    last_updated = Column(DateTime, default=datetime.datetime.now())
    tpl = relationship('TPLManage', lazy='select')


class ProcCollectManage(Base, DictBase):
    __tablename__ = 'proc_collect'
    attributes = ['id', 'nid', 'name', 'tags', 'collect_type', 'collect_method', 'target', 'step', 'comment', 'creator',
                  'created', 'last_updator', 'last_updated', 'collect_name', 'tpl']

    detail_attributes = attributes
    table_column = attributes

    id = Column(Integer, primary_key=True)
    nid = Column(Integer, ForeignKey('tpl.id'))
    name = Column(String(255), nullable=False, default='')
    collect_name = Column(String(255), nullable=False, default='')
    tags = Column(String(255), nullable=False, default='')
    collect_type = Column(String(64), nullable=False, default='PROC')
    collect_method = Column(String(64), nullable=False, default='name')
    target = Column(String(255), nullable=False, default='')
    step = Column(Integer, nullable=False, default=0)
    comment = Column(String(512), nullable=False, default='')
    creator = Column(String(255), nullable=False, default='')
    created = Column(DateTime)
    last_updator = Column(String(255), nullable=False, default='')
    last_updated = Column(DateTime, default=datetime.datetime.now())
    tpl = relationship('TPLManage', lazy='select')


class PortCollectManage(Base, DictBase):
    __tablename__ = 'port_collect'
    attributes = ['id', 'collect_type', 'nid', 'name', 'tags', 'port', 'step', 'timeout', 'comment', 'creator',
                  'created', 'last_updator', 'last_updated', 'collect_name', 'tpl']

    detail_attributes = attributes
    table_column = attributes

    id = Column(Integer, primary_key=True)
    collect_type = Column(String(64), nullable=False, default='PORT')
    nid = Column(Integer, ForeignKey('tpl.id'))
    name = Column(String(255), nullable=False, default='')
    collect_name = Column(String(255), nullable=False, default='')
    tags = Column(String(255), nullable=False, default='')
    port = Column(Integer, nullable=False, default=0)
    step = Column(Integer, nullable=False, default=0)
    timeout = Column(Integer, nullable=False, default=0)
    comment = Column(String(512), nullable=False, default='')
    creator = Column(String(255), nullable=False, default='')
    created = Column(DateTime)
    last_updator = Column(String(255), nullable=False, default='')
    last_updated = Column(DateTime, default=datetime.datetime.now())
    tpl = relationship('TPLManage', lazy='select')


class DatabaseResourceCapacity(Base, DictBase):
    __tablename__ = 'db_resource_capacity'
    attributes = ['f_id', 'f_date_time', 'f_uuid', 'f_name', 'f_type', 'f_domain', 'f_region_id', 'f_az_id',
                  'f_tenant_id',
                  'f_project_id', 'f_host_type', 'f_storage_type', 'f_env_type', 'f_storage_total',
                  'f_storage_allocation',
                  'f_storage_used', 'f_storage_free', 'f_storage_used_percent_p95', 'f_storage_free_percent_p95',
                  'f_message', 'f_modify_time', 'f_connect_num', 'f_connect_limit_num', 'f_connected_percent',
                  'tenant', 'available_zone', 'project', 'region']
    detail_attributes = attributes
    table_column = ['f_id', 'f_date_time', 'f_uuid', 'f_name', 'f_type', 'f_domain', 'f_region_id', 'f_az_id',
                    'f_tenant_id',
                    'f_project_id', 'f_host_type', 'f_storage_type', 'f_env_type', 'f_storage_total',
                    'f_storage_allocation',
                    'f_storage_used', 'f_storage_free', 'f_storage_used_percent_p95', 'f_storage_free_percent_p95',
                    'f_message', 'f_modify_time', 'f_connect_num', 'f_connect_limit_num', 'f_connected_percent']
    f_id = Column(Integer, primary_key=True)
    f_date_time = Column(String(10), nullable=False, default='0000-00-00')
    f_uuid = Column(String(50), nullable=False, default='')
    f_name = Column(String(50), nullable=False, default='')
    f_type = Column(String(50), nullable=False, default='')
    f_domain = Column(String(50), nullable=False, default='')
    f_region_id = Column(String(36), ForeignKey('if_region.id'), nullable=False, default='')
    f_az_id = Column(String(36), ForeignKey('available_zone.id'), nullable=False, default='')
    f_tenant_id = Column(String(32), ForeignKey('iam_tenant.uuid'), nullable=False, default='')
    f_project_id = Column(String(32), ForeignKey('if_project.id'), nullable=False, default='')
    f_host_type = Column(String(32), nullable=False, default='')
    f_storage_type = Column(String(32), nullable=False, default='')
    f_env_type = Column(String(32), nullable=False, default='')
    f_storage_total = Column(FLOAT, nullable=False, default=0)
    f_storage_allocation = Column(FLOAT, nullable=False, default=0)
    f_storage_used = Column(FLOAT, nullable=False, default=0)
    f_storage_free = Column(FLOAT, nullable=False, default=0)
    f_storage_used_percent_p95 = Column(FLOAT, nullable=False, default=0)
    f_storage_free_percent_p95 = Column(FLOAT, nullable=False, default=0)
    f_message = Column(String(1023), nullable=False, default='')
    f_modify_time = Column(DateTime, default=datetime.datetime.now())
    f_connect_num = Column(Integer, nullable=False, default=0)
    f_connect_limit_num = Column(Integer, nullable=False, default=0)
    f_connected_percent = Column(FLOAT, nullable=False, default=0)

    tenant = relationship('Tenant', lazy='select')
    available_zone = relationship('AvailableZone', lazy='select')
    project = relationship('Project', lazy='select')
    region = relationship('Region', lazy='select')


class DatabaseResourceWeekCapacity(Base, DictBase):
    __tablename__ = 'db_resource_capacity_week'
    attributes = ['f_id', 'f_date_time', 'f_uuid', 'f_name', 'f_type', 'f_domain', 'f_region_id', 'f_az_id',
                  'f_tenant_id',
                  'f_project_id', 'f_host_type', 'f_storage_type', 'f_env_type', 'f_storage_total',
                  'f_storage_allocation',
                  'f_storage_used', 'f_storage_free', 'f_storage_used_percent_p95', 'f_storage_free_percent_p95',
                  'f_message', 'f_modify_time', 'f_connect_num', 'f_connect_limit_num', 'f_connected_percent',
                  'tenant', 'available_zone', 'project', 'region']
    detail_attributes = attributes
    table_column = ['f_id', 'f_date_time', 'f_uuid', 'f_name', 'f_type', 'f_domain', 'f_region_id', 'f_az_id',
                    'f_tenant_id',
                    'f_project_id', 'f_host_type', 'f_storage_type', 'f_env_type', 'f_storage_total',
                    'f_storage_allocation',
                    'f_storage_used', 'f_storage_free', 'f_storage_used_percent_p95', 'f_storage_free_percent_p95',
                    'f_message', 'f_modify_time', 'f_connect_num', 'f_connect_limit_num', 'f_connected_percent']
    f_id = Column(Integer, primary_key=True)
    f_date_time = Column(String(10), nullable=False, default='0000-00-00')
    f_uuid = Column(String(50), nullable=False, default='')
    f_name = Column(String(50), nullable=False, default='')
    f_type = Column(String(50), nullable=False, default='')
    f_domain = Column(String(50), nullable=False, default='')
    f_region_id = Column(String(36), ForeignKey('if_region.id'), nullable=False, default='')
    f_az_id = Column(String(36), ForeignKey('available_zone.id'), nullable=False, default='')
    f_tenant_id = Column(String(32), ForeignKey('iam_tenant.uuid'), nullable=False, default='')
    f_project_id = Column(String(32), ForeignKey('if_project.id'), nullable=False, default='')
    f_host_type = Column(String(32), nullable=False, default='')
    f_storage_type = Column(String(32), nullable=False, default='')
    f_env_type = Column(String(32), nullable=False, default='')
    f_storage_total = Column(FLOAT, nullable=False, default=0)
    f_storage_allocation = Column(FLOAT, nullable=False, default=0)
    f_storage_used = Column(FLOAT, nullable=False, default=0)
    f_storage_free = Column(FLOAT, nullable=False, default=0)
    f_storage_used_percent_p95 = Column(FLOAT, nullable=False, default=0)
    f_storage_free_percent_p95 = Column(FLOAT, nullable=False, default=0)
    f_message = Column(String(1023), nullable=False, default='')
    f_modify_time = Column(DateTime, default=datetime.datetime.now())
    f_connect_num = Column(Integer, nullable=False, default=0)
    f_connect_limit_num = Column(Integer, nullable=False, default=0)
    f_connected_percent = Column(FLOAT, nullable=False, default=0)

    tenant = relationship('Tenant', lazy='select')
    available_zone = relationship('AvailableZone', lazy='select')
    project = relationship('Project', lazy='select')
    region = relationship('Region', lazy='select')


class DatabaseResourceMonthCapacity(Base, DictBase):
    __tablename__ = 'db_resource_capacity_month'
    attributes = ['f_id', 'f_date_time', 'f_uuid', 'f_name', 'f_type', 'f_domain', 'f_region_id', 'f_az_id',
                  'f_tenant_id',
                  'f_project_id', 'f_host_type', 'f_storage_type', 'f_env_type', 'f_storage_total',
                  'f_storage_allocation',
                  'f_storage_used', 'f_storage_free', 'f_storage_used_percent_p95', 'f_storage_free_percent_p95',
                  'f_message', 'f_modify_time', 'f_connect_num', 'f_connect_limit_num', 'f_connected_percent',
                  'tenant', 'available_zone', 'project', 'region']
    detail_attributes = attributes
    table_column = ['f_id', 'f_date_time', 'f_uuid', 'f_name', 'f_type', 'f_domain', 'f_region_id', 'f_az_id',
                    'f_tenant_id',
                    'f_project_id', 'f_host_type', 'f_storage_type', 'f_env_type', 'f_storage_total',
                    'f_storage_allocation',
                    'f_storage_used', 'f_storage_free', 'f_storage_used_percent_p95', 'f_storage_free_percent_p95',
                    'f_message', 'f_modify_time', 'f_connect_num', 'f_connect_limit_num', 'f_connected_percent']
    f_id = Column(Integer, primary_key=True)
    f_date_time = Column(String(10), nullable=False, default='0000-00-00')
    f_uuid = Column(String(50), nullable=False, default='')
    f_name = Column(String(50), nullable=False, default='')
    f_type = Column(String(50), nullable=False, default='')
    f_domain = Column(String(50), nullable=False, default='')
    f_region_id = Column(String(36), ForeignKey('if_region.id'), nullable=False, default='')
    f_az_id = Column(String(36), ForeignKey('available_zone.id'), nullable=False, default='')
    f_tenant_id = Column(String(32), ForeignKey('iam_tenant.uuid'), nullable=False, default='')
    f_project_id = Column(String(32), ForeignKey('if_project.id'), nullable=False, default='')
    f_host_type = Column(String(32), nullable=False, default='')
    f_storage_type = Column(String(32), nullable=False, default='')
    f_env_type = Column(String(32), nullable=False, default='')
    f_storage_total = Column(FLOAT, nullable=False, default=0)
    f_storage_allocation = Column(FLOAT, nullable=False, default=0)
    f_storage_used = Column(FLOAT, nullable=False, default=0)
    f_storage_free = Column(FLOAT, nullable=False, default=0)
    f_storage_used_percent_p95 = Column(FLOAT, nullable=False, default=0)
    f_storage_free_percent_p95 = Column(FLOAT, nullable=False, default=0)
    f_message = Column(String(1023), nullable=False, default='')
    f_modify_time = Column(DateTime, default=datetime.datetime.now())
    f_connect_num = Column(Integer, nullable=False, default=0)
    f_connect_limit_num = Column(Integer, nullable=False, default=0)
    f_connected_percent = Column(FLOAT, nullable=False, default=0)

    tenant = relationship('Tenant', lazy='select')
    available_zone = relationship('AvailableZone', lazy='select')
    project = relationship('Project', lazy='select')
    region = relationship('Region', lazy='select')


class CapacityTenant(Base, DictBase):
    __tablename__ = 'iam_tenant'
    __table_args__ = {'schema': 'falcon_portal'}
    attributes = ['uuid', 'name', 'description', 'state']
    summary_attributes = attributes
    detail_attributes = attributes
    table_column = attributes

    uuid = Column(String(36), primary_key=True)
    name = Column(String(63), nullable=False)
    description = Column(String(255), default='')
    state = Column(Boolean, nullable=False)


class CapacityProject(Base, DictBase):
    __tablename__ = 'if_project'
    __table_args__ = {'schema': 'falcon_portal'}
    attributes = ['id', 'name', 'desc', 'tenant_id', 'enabled', 'status', 'tenant', 'is_deleted']
    detail_attributes = attributes
    table_column = ['id', 'name', 'desc', 'tenant_id', 'enabled', 'status']

    id = Column(String(32), primary_key=True)
    name = Column(String(63))
    enabled = Column(Boolean, nullable=True, default=True)
    desc = Column(String(200))
    tenant_id = Column(ForeignKey("falcon_portal.iam_tenant.uuid"))
    status = Column(String(32))
    is_deleted = Column(Integer, default=0)

    tenant = relationship('CapacityTenant', lazy='select')


class CapacityAvailableZone(Base, DictBase):
    __tablename__ = 'available_zone'
    __table_args__ = {'schema': 'falcon_portal'}
    attributes = ['id', 'name', 'name_en', 'created_date', 'updated_date', 'enabled', 'location',
                  'city_code', 'module_code', 't_if_region',
                  'region_id', 'is_deleted', 'is_default_public', 'status', 'env']
    summary_attributes = attributes
    detail_attributes = attributes
    table_column = ['id', 'name', 'name_en', 'created_date', 'updated_date', 'enabled', 'supported_products',
                    'sms_validate', 'city_code', 'status', 'module_code',
                    'region_id', 'is_deleted', 'is_default_public', 'status', 'extend_info', 'config', 'sold_out']

    id = Column(String(32), primary_key=True)
    name = Column(String(64), default='')
    name_en = Column(String(36), default='')
    env = Column(ForeignKey('falcon_portal.environment.id'), nullable=False, default='')
    status = Column(String(30))
    created_date = Column(DateTime, default=datetime.datetime.now())
    updated_date = Column(DateTime, default=datetime.datetime.now())
    enabled = Column(Boolean, nullable=True, default=1)
    location = Column(String(64), default='')  # 地址
    extend_info = Column(String(255))  # 扩展信息
    region_id = Column(String(32), ForeignKey('falcon_portal.if_region.id'), nullable=False, default='')
    is_deleted = Column(Integer(), default=0)
    supported_products = Column(Text)
    config = Column(Text)
    sold_out = Column(Boolean, default=False)
    city_code = Column(String(64), default='')
    module_code = Column(ForeignKey('falcon_portal.module.id'), default='')
    sms_validate = Column(Integer(), default=0)
    is_default_public = Column(Integer(), default=0)

    t_if_region = relationship('CapacityRegion', lazy=False)


class CapacityRegion(Base, DictBase):
    __tablename__ = 'if_region'
    __table_args__ = {'schema': 'falcon_portal'}
    attributes = ['id', 'name', 'create_time', 'update_time', 'is_using']
    detail_attributes = attributes
    table_column = attributes
    update_column = ['name']

    id = Column(String(36), primary_key=True)
    name = Column(String(36))
    create_time = Column(DateTime)
    update_time = Column(DateTime, default=datetime.datetime.now())
    is_using = Column(Integer, nullable=False, default=0)


class CapacityHostManage(Base, DictBase):
    __tablename__ = 'cmdb_host'
    __table_args__ = {'schema': 'falcon_portal'}
    attributes = ['uuid', 'hostname', 'ip', 'os_type', 'os', 'env', 'host', 'env_type', 'enabled',
                  'parentos', 'os_platform', 'state', 'cpu', 'mem', 'create_user', 'note', 'remote_manage_ip',
                  'region_id', 'az_id', 'tenant_id']
    detail_attributes = attributes
    summary_attributes = ['uuid', 'hostname', 'ip', 'os_type', 'os', 'env_type', 'enabled',
                          'parentos', 'os_platform', 'state', 'cpu', 'mem', 'create_user', 'note', 'remote_manage_ip',
                          'region_id', 'az_id', 'tenant_id', 'project_id']

    uuid = Column(ForeignKey('falcon_portal.host.hostname'), primary_key=True)
    hostname = Column(String(100), default='')
    ip = Column(String(100), default='')
    os_type = Column(String(100), default='')
    os = Column(String(100), default='')
    env = Column(String(100), default='')
    enabled = Column(INT, nullable=False, default=1)
    create_time = Column(DateTime, default='')
    env_type = Column(ForeignKey('falcon_portal.environment.id'), default='')
    parentos = Column(String(255), default='')
    os_platform = Column(String(255), default='')
    state = Column(String(50), default='')
    cpu = Column(Integer)
    mem = Column(Integer)
    create_user = Column(String(100), default='')
    note = Column(String(255), default='')
    remote_manage_ip = Column(String(20), default='')
    region_id = Column(String(36))
    az_id = Column(String(36))
    tenant_id = Column(String(64), ForeignKey('falcon_portal.iam_tenant.uuid'))
    project_id = Column(String(32), ForeignKey('falcon_portal.if_project.id'))


class CmdbCbs(Base, DictBase):
    __tablename__ = 'cmdb_cbs'
    __table_args__ = {'schema': 'falcon_portal'}
    attributes = ['id', 'name', 'description', 'size_gb', 'status', 'tenant_id', 'project_id', 'az_id',
                  'mtime', 'host_id', 'device', 'data_disk_type', 'public_cloud_provider', 't_if_host',
                  't_iam_tenant', 't_if_project', 't_if_az']
    summary_attributes = attributes
    detail_attributes = ['id', 'name', 'description', 'szie_gb', 'status', 'tenant_id', 'project_id', 'az_id',
                         'mtime', 'host_id', 'device', 'data_disk_type', 'public_cloud_provider', 't_if_host',
                         't_if_az', 't_iam_tenant', 't_if_project']
    table_column = attributes
    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False, default='')
    description = Column(String(255), nullable=False, default='')
    size_gb = Column(Integer, nullable=False, default=0)
    status = Column(String(64), nullable=False, default='')
    tenant_id = Column(ForeignKey('falcon_portal.iam_tenant.uuid'), nullable=False)
    project_id = Column(ForeignKey('falcon_portal.if_project.id'), nullable=False)
    az_id = Column(ForeignKey('falcon_portal.available_zone.id'), nullable=False)
    mtime = Column(DateTime, default=datetime.datetime.now())
    host_id = Column(ForeignKey('falcon_portal.cmdb_host.uuid'), nullable=False)
    device = Column(String(255), nullable=False, default='')
    data_disk_type = Column(String(32), nullable=False, default='')
    public_cloud_provider = Column(String(20), nullable=False, default='')

    t_if_host = relationship('CapacityHostManage', lazy='select')
    t_iam_tenant = relationship('CapacityTenant', lazy='select')
    t_if_project = relationship('CapacityProject', lazy='select')
    t_if_az = relationship('CapacityAvailableZone', lazy='select')


# capacity库中的表
class DiskResourceCapacity(Base, DictBase):
    __tablename__ = 'cbs'
    __table_args__ = {'schema': 'capacity'}
    attributes = ['id', 'datetime', 'category', 'cbs_id', 'disk_io_util_p95', 'disk_io_await_p95',
                  'disk_io_read_requests_p95', 'disk_io_write_requests_p95', 'disk_io_read_bytes_p95',
                  'disk_io_write_bytes_p95', 'size_gb', 'actual_used_size', 'used_rate', 'cmdb_cbs']
    detail_attributes = attributes
    table_column = ['id', 'datetime', 'category', 'cbs_id', 'disk_io_util_p95', 'disk_io_await_p95',
                    'disk_io_read_requests_p95', 'disk_io_write_requests_p95', 'disk_io_read_bytes_p95',
                    'disk_io_write_bytes_p95', 'size_gb', 'actual_used_size', 'used_rate', 'cmdb_cbs']
    id = Column(Integer, primary_key=True)
    datetime = Column(String(10), nullable=False, default='0000-00-00')
    category = Column(String(32), nullable=False, default='')
    cbs_id = Column(ForeignKey(CmdbCbs.id))
    disk_io_util_p95 = Column(FLOAT, nullable=False, default=0)
    disk_io_await_p95 = Column(FLOAT, nullable=False, default=0)
    disk_io_read_requests_p95 = Column(FLOAT, nullable=False, default=0)
    disk_io_write_requests_p95 = Column(FLOAT, nullable=False, default=0)
    disk_io_read_bytes_p95 = Column(FLOAT, nullable=False, default=0)
    disk_io_write_bytes_p95 = Column(FLOAT, nullable=False, default=0)
    size_gb = Column(Integer, nullable=False, default=0)
    actual_used_size = Column(FLOAT, nullable=True)
    used_rate = Column(FLOAT, nullable=True)
    timestamp = Column(DateTime, nullable=False)

    cmdb_cbs = relationship('CmdbCbs', lazy='select')


class CmdbCephCluster(Base, DictBase):
    __tablename__ = 'cmdb_block_storage_cluster'
    __table_args__ = {'schema': 'falcon_portal'}
    attributes = ['id', 'name', 'cluster_id', 'monitor_id', 'region_id', 'az_id', 'capacity', 'openstack_id',
                  'mtime', 't_if_region', 't_if_az']
    summary_attributes = attributes
    detail_attributes = attributes
    table_column = ['id', 'name', 'cluster_id', 'monitor_id', 'region_id', 'az_id', 'capacity', 'openstack_id',
                    'mtime', 't_if_region', 't_if_az']
    id = Column(String(36), primary_key=True)
    name = Column(String(64), nullable=False, default='')
    cluster_id = Column(String(36), default='')
    monitor_id = Column(String(36), nullable=False, default='')
    region_id = Column(String(36), ForeignKey('falcon_portal.if_region.id'), nullable=False, default='')
    az_id = Column(String(36), ForeignKey('falcon_portal.available_zone.id'), nullable=False, default='')
    capacity = Column(Integer, default=0)
    openstack_id = Column(String(36), nullable=False, default='')
    mtime = Column(DateTime, default=datetime.datetime.now())

    t_if_region = relationship('CapacityRegion', lazy='select')
    t_if_az = relationship('CapacityAvailableZone', lazy='select')


# capacity库中的表
class CephResourceCapacity(Base, DictBase):
    __tablename__ = 'ceph'
    __table_args__ = {'schema': 'capacity'}
    attributes = ['id', 'datetime', 'category', 'ceph_id', 'usage_all_p95', 'usage_avail_p95',
                  'usage_used_p95', 'usage_used_percent_p95', 'ceph_info']
    detail_attributes = attributes
    table_column = ['id', 'datetime', 'category', 'ceph_id', 'usage_all_p95', 'usage_avail_p95',
                    'usage_used_p95', 'usage_used_percent_p95', 'ceph_info']
    id = Column(Integer, primary_key=True)
    datetime = Column(String(10), nullable=False, default='0000-00-00')
    category = Column(String(32), default='')
    ceph_id = Column(ForeignKey(CmdbCephCluster.id))
    usage_all_p95 = Column(FLOAT, default=0)
    usage_avail_p95 = Column(FLOAT, default=0)
    usage_used_p95 = Column(FLOAT, default=0)
    usage_used_percent_p95 = Column(FLOAT, nullable=False, default=0)

    ceph_info = relationship('CmdbCephCluster', lazy='select')


# 审计统计表
class AuditStatistics(Base, DictBase):
    __tablename__ = 'audit_statistics'
    attributes = ['type', 'date_time', 'total_count', 'sample_count', 'sample_total_percent', 'performant_error_count',
                  'performant_sample_percent', 'alive_error_count', 'alive_sample_percent', 'capacity_error_count',
                  'capacity_sample_percent', 'performant_strategy_error_count', 'performant_strategy_sample_percent',
                  'alive_strategy_error_count', 'alive_strategy_sample_percent']
    table_column = detail_attributes = attributes

    type = Column(String(10), primary_key=True)
    date_time = Column(String(10), primary_key=True)
    total_count = Column(Integer, nullable=False)
    sample_count = Column(Integer, nullable=False)
    sample_total_percent = Column(FLOAT, nullable=False)
    performant_error_count = Column(Integer, nullable=False)
    performant_sample_percent = Column(FLOAT, nullable=False)
    alive_error_count = Column(Integer, nullable=False)
    alive_sample_percent = Column(FLOAT, nullable=False)
    capacity_error_count = Column(Integer, nullable=False)
    capacity_sample_percent = Column(FLOAT, nullable=False)
    performant_strategy_error_count = Column(Integer, nullable=False)
    performant_strategy_sample_percent = Column(FLOAT, nullable=False)
    alive_strategy_error_count = Column(Integer, nullable=False)
    alive_strategy_sample_percent = Column(FLOAT, nullable=False)


# 主机审计表
class AuditHost(Base, DictBase):
    __tablename__ = 'audit_host'
    attributes = ['uuid', 'date_time', 'status', 'region', 'az', 'tenant', 'project', 'agent_alive',
                  'ip_ping', 'mem_use', 'agent_alive_policy', 'ip_ping_policy']
    table_column = detail_attributes = attributes

    uuid = Column(Integer, primary_key=True)
    date_time = Column(String(10), primary_key=True)
    status = Column(Integer, primary_key=True)
    region = Column(String(255), nullable=False)
    az = Column(String(255), nullable=False)
    tenant = Column(String(63), nullable=False)
    project = Column(String(63), nullable=False)
    agent_alive = Column(String(10), nullable=False)
    ip_ping = Column(String(10), nullable=False)
    mem_use = Column(String(20), nullable=False)
    agent_alive_policy = Column(Integer, nullable=False)
    ip_ping_policy = Column(Integer, nullable=False)


# 数据库审计表
class AuditDatabase(Base, DictBase):
    __tablename__ = 'audit_database'
    attributes = ['id', 'node_id', 'date_time', 'status', 'host_uuid', 'db_uuid', 'az', 'tenant', 'project',
                  'db_alive', 'connected_percent', 'db_alive_policy']
    table_column = detail_attributes = attributes

    node_id = Column(Integer)
    id = Column(String(255), primary_key=True)
    date_time = Column(String(10), primary_key=True)
    status = Column(Integer, primary_key=True)
    host_uuid = Column(String(255), nullable=False)
    db_uuid = Column(String(255), nullable=False)
    az = Column(String(255), nullable=False)
    tenant = Column(String(63), nullable=False)
    project = Column(String(63), nullable=False)
    db_alive = Column(String(10), nullable=False)
    connected_percent = Column(String(20), nullable=False)
    db_alive_policy = Column(Integer, nullable=False)


# 网络设备审计表
class AuditNetwork(Base, DictBase):
    __tablename__ = 'audit_network'
    attributes = ['serial_num', 'date_time', 'status',
                  'network_status', 'network_alive', 'network_status_policy', 'network_alive_policy']
    table_column = detail_attributes = attributes

    serial_num = Column(String(50), primary_key=True)
    date_time = Column(String(10), primary_key=True)
    status = Column(Integer, primary_key=True)
    network_status = Column(String(10), nullable=False)
    network_alive = Column(String(10), nullable=False)
    network_status_policy = Column(Integer, nullable=False)
    network_alive_policy = Column(Integer, nullable=False)


# 网络专线审计表
class AuditNetline(Base, DictBase):
    __tablename__ = 'audit_netline'
    attributes = ['id', 'serial_num', 'local_address', 'date_time', 'status', 'iprange', 'net_in_octets_percent',
                  'netline_alive', 'net_in_octets', 'net_in_octets_percent_policy', 'netline_alive_policy']
    table_column = detail_attributes = attributes

    id = Column(String(100), primary_key=True)
    serial_num = Column(String(50), nullable=False)
    local_address = Column(String(16), nullable=False)
    date_time = Column(String(10), primary_key=True)
    status = Column(Integer, primary_key=True)
    iprange = Column(String(16), nullable=False)
    net_in_octets_percent = Column(String(10), nullable=False)
    netline_alive = Column(String(10), nullable=False)
    net_in_octets = Column(String(20), nullable=False)
    net_in_octets_percent_policy = Column(Integer, nullable=False)
    netline_alive_policy = Column(Integer, nullable=False)


# ceph集群表
class CephCluster(Base, DictBase):
    __tablename__ = 'ceph_cluster'
    attributes = ['id', 'ceph_id', 'display_name', 'ceph_version', 'cluster_type', 'super_score_ratio',
                  'cluster_network', 'public_network', 'region_id', 'zone_id', 'monitor_id', 'openstack_id', 'status',
                  'monitor_url', 'monitor_usr', 'monitor_pwd', 'environ_id', 'station_id', 'tenant_id', 'project_id',
                  'user_id', 'is_deleted', 'enabled', 'env']
    detail_attributes = attributes

    id = Column(String(32), primary_key=True)
    ceph_id = Column(String(36), nullable=False)
    display_name = Column(String(128), nullable=False)
    ceph_version = Column(String(32), nullable=False)
    cluster_type = Column(String(32), nullable=False)
    super_score_ratio = Column(FLOAT(0), nullable=False)
    cluster_network = Column(String(32), nullable=False)
    public_network = Column(String(32), nullable=False)
    region_id = Column(String(32), nullable=False)
    zone_id = Column(String(256), nullable=False)
    monitor_id = Column(String(36), nullable=False)
    openstack_id = Column(String(36), nullable=False)
    status = Column(String(32), nullable=False)
    monitor_url = Column(String(64), nullable=False)
    monitor_usr = Column(String(32), nullable=False)
    monitor_pwd = Column(String(32), nullable=False)
    environ_id = Column(String(32), nullable=False)
    station_id = Column(String(32), nullable=False)
    tenant_id = Column(String(32), nullable=False)
    project_id = Column(String(32), nullable=False)
    user_id = Column(String(32), nullable=False)
    is_deleted = Column(INT, nullable=False)
    enabled = Column(INT, nullable=False)
    env = Column(String(32), nullable=False)


class CephClusterHost(Base, DictBase):
    __tablename__ = "ceph_cluster_host"
    attributes = ['id', 'cluster_id', 'display_name', 'status', 'room_name', 'rack_name', 'role', 'ip', 'storage_ip',
                  'environ_id', 'station_id', 'tenant_id', 'project_id', 'user_id', 'is_deleted', 'host_uuid']
    detail_attributes = attributes

    id = Column(String(32), primary_key=True)
    cluster_id = Column(ForeignKey('ceph_cluster.id'))
    display_name = Column(String(64), nullable=False)
    status = Column(String(32), nullable=False)
    room_name = Column(String(32), nullable=False)
    rack_name = Column(String(32), nullable=False)
    role = Column(String(64), nullable=False)
    ip = Column(String(64), nullable=False)
    storage_ip = Column(String(64), nullable=False)
    environ_id = Column(String(32), nullable=False)
    station_id = Column(String(32), nullable=False)
    tenant_id = Column(String(32), nullable=False)
    project_id = Column(String(32), nullable=False)
    user_id = Column(String(32), nullable=False)
    is_deleted = Column(INT, nullable=False)
    host_uuid = Column(String(100), nullable=False)

    ceph_cluster = relationship('CephCluster', lazy='select')


class CephClusterRgw(Base, DictBase):
    __tablename__ = "ceph_cluster_rgw"
    attributes = ["id", "cluster_id", "display_name", "status", "environ_id", "station_id", "tenant_id", "project_id",
                  "user_id", "is_deleted", "host_id", "gateway", "update_user", "update_user_name", "created_user",
                  'ceph_host']
    detail_attributes = attributes

    id = Column(String(32), primary_key=True)
    cluster_id = Column(ForeignKey('ceph_cluster.id'))
    display_name = Column(String(64), nullable=False)
    status = Column(String(32), nullable=False)
    environ_id = Column(String(32), nullable=False)
    station_id = Column(String(32), nullable=False)
    tenant_id = Column(String(64), nullable=False)
    project_id = Column(String(64), nullable=False)
    user_id = Column(String(64), nullable=False)
    created_user = Column(String(32), nullable=False)
    host_id = Column(ForeignKey('ceph_cluster_host.id'))
    gateway = Column(String(32), nullable=False)
    update_user = Column(String(32), nullable=False)
    update_user_name = Column(String(32), nullable=False)
    is_deleted = Column(INT, nullable=False)

    ceph_cluster = relationship('CephCluster', lazy='select')
    ceph_host = relationship('CephClusterHost', lazy='select')


# 负载均衡
class LoadBalance(Base, DictBase):
    __tablename__ = "load_balance"
    attributes = ["id", "host_uuid", "vip", "ip", "port", "lb_type", "create_time", "update_time"]
    detail_attributes = attributes
    # id是用的是trigger生成的,执行时,sqlalchemy报错 FlushError
    # 怎么破?
    # 1. 重写insert方法,在insert之前先执行trigger
    # 2. 在trigger中获取id,然后再插入
    # 代码修改为
    # id = Column(String(32), primary_key=True, default=uuid.uuid4().hex)
    id = Column(String(48), primary_key=True, comment='仅用于上报时作为节点使用,避免直接上报到主机uuid', )
    # default=lambda: str(uuid.uuid4()))
    host_uuid = Column(String(36), nullable=False, comment='主机uuid,唯一')
    vip = Column(String(20), nullable=False)
    ip = Column(String(20), nullable=False)
    port = Column(Integer, nullable=False)
    lb_type = Column(String(20), nullable=False)
    create_time = Column(DateTime, nullable=False)
    update_time = Column(DateTime, nullable=False)
    tenant_id = Column(String(64), nullable=False)
    project_id = Column(String(64), nullable=False)

    __table_args__ = (
        UniqueConstraint('host_uuid', name='unique_index_host_uuid'),
    )
