# coding=utf-8
"""
fitcloud.server.wsgi_server
~~~~~~~~~~~~~~~~~~~~~~~~~~

本模块提供wsgi启动能力

"""

from __future__ import absolute_import

import os
from monitor.server import base

# 优先从环境变量monitor_CONF, monitor_CONF_DIR读取，其次是本地预设路径/etc/monitor
# 请修改环境变量,不再修改代码提交
application = base.initialize_server('monitor', os.environ.get('monitor_CONF', '/etc/monitor-api/monitor-api.conf'),
                                     conf_dir=os.environ.get('monitor_CONF_DIR', '/etc/monitor-api/conf.d'))
