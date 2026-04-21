# coding=utf-8
"""
fitcloud.server.simple_server
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

本模块提供开发测试用的简单服务启动能力

"""
import os
import logging
import sys
from wsgiref.simple_server import make_server

import six

from monitor.core import config
from monitor.server import base


LOG = logging.getLogger(__name__)
CONF = config.CONF

if six.PY2:
    reload(sys)
    sys.setdefaultencoding('UTF-8')


def main():
    """
    主函数，启动一个基于wsgiref的测试/开发用途的wsgi服务器

    绑定地址由配置文件提供， 监听端口由配置文件提供
    """
    # 优先从环境变量FICLOUD_CONF, FICLOUD_CONF_DIR读取，其次是本地预设路径./fitcloud
    # 请修改环境变量,不再修改代码提交
    app = base.initialize_server('monitor', os.environ.get('monitor', './monitor-api.conf'),
                                 conf_dir=os.environ.get('monitor_conf'))
    bind_addr = CONF.server.bind
    port = CONF.server.port
    httpd = make_server(bind_addr, port, app)
    print("Serving on %s:%d..." % (bind_addr, port))
    httpd.serve_forever()


if __name__ == '__main__':
    main()
