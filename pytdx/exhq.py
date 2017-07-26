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
from pytdx.base_socket_client import BaseSocketClient, update_last_ack_time


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

class TdxExHq_API(BaseSocketClient):

    def setup(self):
        ExSetupCmd1(self.client).call_api()

    ### API LIST

    @update_last_ack_time
    def get_markets(self):
        cmd = GetMarkets(self.client)
        return cmd.call_api()

    @update_last_ack_time
    def get_instrument_count(self):
        cmd = GetInstrumentCount(self.client)
        return cmd.call_api()

    @update_last_ack_time
    def get_instrument_quote(self, market, code):
        cmd = GetInstrumentQuote(self.client)
        cmd.setParams(market, code)
        return cmd.call_api()

    @update_last_ack_time
    def get_minute_time_data(self, market, code):
        cmd = GetMinuteTimeData(self.client)
        cmd.setParams(market, code)
        return cmd.call_api()

    def do_heartbeat(self):
        self.get_instrument_count()

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