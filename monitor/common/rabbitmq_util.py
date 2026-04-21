# -*- coding:utf-8 -*-
'''
rabbitmq客户端封装
'''
# __author__ = 'guozhiwei'

import time
import puka
import random
import logging
import threading
import traceback
import thread_util

SEND_MSG_LOCK = threading.Lock()


class Rabbit:

    INSTANCE = None

    def __init__(self, server_list):
        '''
            server_list = ['','']
        '''
        self.server_list = server_list
        random.shuffle(self.server_list)

        # 当前使用节点列表中的哪个index
        self.current_node_index = 0
        self.connect_time_out = 10

    @classmethod
    def get_instance(cls, server_list):
        if not cls.INSTANCE:
            cls.INSTANCE = Rabbit(server_list)
            cls.INSTANCE.connect()
        return cls.INSTANCE

    def connect(self):
        ''' 连接rabbitmq-server
            return 0  成功
                   -1 失败
        '''
        for i in range(1000):
            for j in range(2):
                if self._connect() == 0:
                    return 0
            self.current_node_index = (self.current_node_index + 1) % len(self.server_list)
            logging.warning('now change another rabbitmq-server node,please wait a moment')
        return -1

    def _connect(self):
        ''' connnect to rabbitmq server
            return 0表示成功
        '''
        server_url = self.server_list[self.current_node_index]
        try:
            self.client = puka.Client(server_url)
            promise = self.client.connect()
            res = self.client.wait(promise,timeout=self.connect_time_out)
            if res and res.has_key('server_properties'):
                logging.info('connect to rabbitmq-server [%s] success',server_url)
            else:
                logging.error('fail to connect or init rabbitmq-server ,amqp url is [%s] error is [%s]', server_url, traceback.format_exc())
                return -1
            return 0
        except:
            logging.error('fail to connect or init rabbitmq-server ,amqp url is [%s] error is [%s]', server_url, traceback.format_exc())
            time.sleep(0.5)
            return -1

    def declare_my_exchange(self, **kwargs):
        ''' declare exchange
        '''
        promise_exchange = self.client.exchange_declare(**kwargs)
        res = self.client.wait(promise_exchange)
        if res == {}:
            return 0
        else:
            return -1

    def declare_my_queue(self, **kwargs):
        '''
            declare my queue name
        '''
        promise = self.client.queue_declare(**kwargs)
        res = self.client.wait(promise)
        if res and res.is_error is False:
            return 0
        else:
            return -1

    def bind_my_queue(self, bind_key, exchange_name, queue_name):
        ''' bind queue and exchange with key
        '''
        promise = self.client.queue_bind(exchange=exchange_name, queue=queue_name, routing_key=bind_key)
        self.client.wait(promise)
        return 0

    def receive_msg(self, consume_promise):
        for i in range(2):
            try:
                msg_result = self.client.wait(consume_promise)
                return msg_result
            # except puka.PreconditionFailed:
            #     logging.warning('from receive %s',traceback.format_exc())
            #     return None
            # except select.error,e:
            #     if e[0] == 4:
            #         logging.warning('from receive select error %s',traceback.format_exc())
            #     return None
            except:
                logging.error(traceback.format_exc())

                # 重连
                self.current_node_index = (self.current_node_index + 1)%len(self.server_list)
                self.connect()

                return None

    def init_consumer(self, queue_name):
        consume_promise = self.client.basic_consume(queue=queue_name, no_ack=True)
        return consume_promise

    def _send_msg(self, msg, routing_key, exchange_name, timeout):
        try:
            if timeout == 0:
                timeout = None
            promise = self.client.basic_publish(exchange=exchange_name,
                                                routing_key=routing_key,
                                                body=msg,
                                           )
            ress = self.client.wait(promise, timeout)
            if ress == {}:
                logging.info("send rabbitmq msg, key:%s msg:%s", routing_key, msg)
                return True
            else:
                return False
        except:
            logging.error('from send %s', traceback.format_exc())
            return False

    @thread_util.lockingCall(SEND_MSG_LOCK)
    def send_msg(self, msg, routing_key, exchange_name, timeout=1):
        for i in range(2):
            res = self._send_msg(msg, routing_key, exchange_name, timeout)
            if res:
                return True
            else:
                self.current_node_index = (self.current_node_index + 1) % len(self.server_list)
                self.connect()
        return False


if __name__ == '__main__':
    pass
