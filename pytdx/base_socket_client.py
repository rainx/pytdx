# coding=utf-8

#
# Just for practising
#


import os
import socket
import sys
import pandas as pd

if __name__ == '__main__':
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from pytdx.log import DEBUG, log

import threading,datetime
import time
from pytdx.heartbeat import HqHeartBeatThread
import functools


CONNECT_TIMEOUT = 5.000
RECV_HEADER_LEN = 0x10
DEFAULT_HEARTBEAT_INTERVAL = 10.0


"""
In [7]: 0x7e
Out[7]: 126

In [5]: len(body)
Out[5]: 8066

In [6]: len(body)/126
Out[6]: 64.01587301587301

In [7]: len(body)%126
Out[7]: 2

In [8]: (len(body)-2)/126
Out[8]: 64.0
"""
def update_last_ack_time(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kw):
        self.last_ack_time = time.time()
        log.debug("last ack time update to " + str(self.last_ack_time))
        try:
            ret = func(self, *args, **kw)
        except Exception as e:
            self.last_transaction_failed = True
            ret = None
            raise e
        finally:
            return ret
    return wrapper


class BaseSocketClient(object):

    def __init__(self, multithread=False, heartbeat=False):
        self.need_setup = True
        if multithread or heartbeat:
            self.lock = threading.Lock()
        else:
            self.lock = None

        self.client = None
        self.heartbeat = heartbeat
        self.heartbeat_thread = None
        self.stop_event = None
        self.heartbeat_interval = DEFAULT_HEARTBEAT_INTERVAL # 默认10秒一个心跳包
        self.last_ack_time = time.time()
        self.last_transaction_failed = False
        self.ip = None
        self.port = None

    def connect(self, ip='101.227.73.20', port=7709):
        """

        :param ip:  服务器ip 地址
        :param port:  服务器端口
        :return: 是否连接成功 True/False
        """

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.settimeout(CONNECT_TIMEOUT)
        log.debug("connecting to server : %s on port :%d" % (ip, port))
        try:
            self.client.connect((ip, port))
            self.ip = ip
            self.port = port
        except socket.timeout as e:
            print(str(e))
            log.debug("connection expired")
            return False
        log.debug("connected!")

        if self.need_setup:
            self.setup()

        if self.heartbeat:
            self.stop_event = threading.Event()
            self.heartbeat_thread = HqHeartBeatThread(self, self.stop_event, self.heartbeat_interval)
            self.heartbeat_thread.start()
        return self

    def disconnect(self):

        if self.heartbeat_thread and \
            self.heartbeat_thread.is_alive():
            self.stop_event.set()

        if self.client:
            log.debug("disconnecting")
            try:
                self.client.shutdown(socket.SHUT_RDWR)
                self.client.close()
                self.client = None
            except Exception as e:
                log.debug(str(e))
            log.debug("disconnected")

    def close(self):
        """
        disconnect的别名，为了支持 with closing(obj): 语法
        :return:
        """
        self.disconnect()


    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def to_df(self, v):
        if isinstance(v, list):
            return pd.DataFrame(data=v)
        elif isinstance(v, dict):
            return pd.DataFrame(data=[v,])
        else:
            return pd.DataFrame(data=[{'value': v}])
