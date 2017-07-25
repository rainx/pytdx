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
from pytdx.parser.ex_setup_commands import ExSetupCmd1
from pytdx.parser.ex_get_markets import GetMarkets
from pytdx.parser.ex_get_instrument_count import GetInstrumentCount
from pytdx.parser.ex_get_instrument_quote import GetInstrumentQuote
from pytdx.parser.ex_get_minute_time_data import GetMinuteTimeData


from pytdx.params import TDXParams

import threading,datetime

CONNECT_TIMEOUT = 5.000
RECV_HEADER_LEN = 0x10

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

class TdxExHq_API(object):

    def __init__(self, multithread=False):
        self.need_setup = True
        if multithread:
            self.lock = threading.Lock()
        else:
            self.lock = None

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
        except socket.timeout as e:
            print(str(e))
            log.debug("connection expired")
            return False
        log.debug("connected!")

        if self.need_setup:
            self.setup()

        return self

    def disconnect(self):
        if self.client:
            log.debug("disconnecting")
            try:
                self.client.shutdown(socket.SHUT_RDWR)
                self.client.close()
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

    def setup(self):
        ExSetupCmd1(self.client).call_api()


    ### API LIST

    def get_markets(self):
        cmd = GetMarkets(self.client)
        return cmd.call_api()

    def get_instrument_count(self):
        cmd = GetInstrumentCount(self.client)
        return cmd.call_api()

    def get_instrument_quote(self, market, code):
        cmd = GetInstrumentQuote(self.client)
        cmd.setParams(market, code)
        return cmd.call_api()

    def get_minute_time_data(self, market, code):
        cmd = GetMinuteTimeData(self.client)
        cmd.setParams(market, code)
        return cmd.call_api()

if __name__ == '__main__':
    import pprint

    api = TdxExHq_API()
    with api.connect('61.152.107.141', 7727):
        log.info("获取市场代码")
        pprint.pprint(api.get_markets())
        log.info("查询市场中商品数量")
        pprint.pprint(api.get_instrument_count())
        log.info("查询行情")
        #pprint.pprint(api.get_instrument_quote(47, "IF1709"))
        #pprint.pprint(api.get_instrument_quote(8, "10000889"))
        pprint.pprint(api.get_instrument_quote(31, "00020"))
        log.info("查询分时行情")
        #pprint.pprint(api.get_minute_time_data(47, "IF1709"))
        #pprint.pprint(api.get_minute_time_data(8, "10000889"))
        #pprint.pprint(api.get_minute_time_data(31, "00020"))