# coding=utf8

from monitor.core.utils import decrypt
from monitor.core import config

import redis


class RedisForCommon:
    """
    非集群的redis
    """

    INSTANCE = None

    def __init__(self, **init_config):
        host = init_config.get("host")
        port = int(init_config.get('port'))
        max_connections = int(init_config.get('max_connections', 20))
        password = decrypt(init_config.get('password', ''))
        pool = redis.ConnectionPool(host=host, port=port, max_connections=max_connections, password=password)
        self.redis = redis.Redis(connection_pool=pool)

    @classmethod
    def get_instance(cls, name):
        if not cls.INSTANCE:
            cache_config = config.CONF.to_dict().get("cache") or {}
            init_config = cache_config.get(name, {})
            RedisForCommon.INSTANCE = RedisForCommon(**init_config)
        return RedisForCommon.INSTANCE

    @classmethod
    def get_instance_for_common_1(cls):
        return cls.get_instance("common_redis_1").redis
