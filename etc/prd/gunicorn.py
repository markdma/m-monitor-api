# coding=utf-8
from __future__ import absolute_import

import logging
from logging.handlers import WatchedFileHandler
import multiprocessing
import os
import sys
sys.path.append("/data/monitor-api")
from monitor.core import config as __config


# 优先从环境变量FICLOUD_CONF, FICLOUD_CONF_DIR读取，其次是本地预设路径/etc/monitor
# 请修改环境变量,不再修改代码提交
__config.setup(os.environ.get('monitor_CONF', '/etc/monitor-api/monitor-api.conf'),
               dir_path=os.environ.get('monitor_CONF_DIR', '/etc/monitor-api/conf.d'))
CONF = __config.CONF

name = 'monitor'
proc_name = 'monitor'
bind = '%s:%d' % (CONF.server.bind, CONF.server.port)
backlog = CONF.server.backlog
# 超时
timeout = 300
# 进程数
workers = 20
# 指定每个进程开启的线程数
threads = 5 
debug = True
daemon = False
# 日志级别，这个日志级别指的是错误日志的级别，而访问日志的级别无法设置
loglevel = CONF.log.level.lower()
# 访问日志文件的路径
accesslog = "/dev/null"
# 错误日志文件的路径
errorlog = "/tmp/error.log"
acclog = logging.getLogger('gunicorn.access')
acclog.addHandler(WatchedFileHandler(CONF.log.gunicorn_access))
acclog.propagate = False
errlog = logging.getLogger('gunicorn.error')
errlog.addHandler(WatchedFileHandler(CONF.log.gunicorn_error))
errlog.propagate = False

# keyfile =
# certfile =
# ca_certs =
# chdir = '/home/user'
# sync/gevent/eventlet/tornado/gthread/gaiohttp
# worker_class = 'gevent'
# worker_connections = 1000
# 到达max requests之后worker会重启
# max_requests = 0
# keepalive = 5
# reload = True
# %(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"
# access_log_format = CONF.log.format_string
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(L)s %(b)s "%(f)s" "%(a)s"'
# syslog_addr = udp://localhost:514
# HTTP URL长度限制
# limit_request_line = 4094
limit_request_line = 0
