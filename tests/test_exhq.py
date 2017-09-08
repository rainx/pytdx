#coding: utf-8

import pytest
from pytdx.errors import TdxFunctionCallError, TdxConnectionError
from collections import OrderedDict
import pandas as pd
import socket
from pytdx.exhq import TdxExHq_API, TDXParams


class Log(object):
    def info(self, *args):
        pass

log = Log()


def test_all_functions():

    symbol_params = [
        [47, "IF1709"],
        [8, "10000889"],
        [31, "00020"],
        [47, "IFL0"],
        [31, "00700"]
    ]

    api = TdxExHq_API(auto_retry=True)
    try:
        with api.connect('121.14.110.210', 7727):
            log.info("获取市场代码")
            data = api.get_markets()
            assert data is not None
            assert type(data) is list
            assert len(data) > 0

            log.info("查询市场中商品数量")
            data =api.get_instrument_count()
            assert data is not None
            assert data > 0

            log.info("查询五档行情")
            for params in symbol_params:
                data = api.get_instrument_quote(*params)

                assert data is not None
                assert type(data) is list
                assert len(data) > 0


            # log.info("查询分时行情")
            for params in symbol_params:
                data = api.get_minute_time_data(*params)
                assert data is not None
                assert type(data) is list
                assert len(data) >= 0

            log.info("查询历史分时行情")
            for params in symbol_params:
                data = api.get_history_minute_time_data(params[0], params[1], 20170811)
                assert data is not None
                assert type(data) is list
                assert len(data) > 0

            log.info("查询分时成交")
            for params in symbol_params:
                data = api.get_transaction_data(*params)
                assert data is not None
                assert type(data) is list
                assert len(data) >= 0

            log.info("查询历史分时成交")
            for params in symbol_params:
                data = api.get_history_transaction_data(params[0], params[1], 20170811)
                assert data is not None
                assert type(data) is list
                assert len(data) >= 0

            log.info("查询k线")
            for params in symbol_params:
                data = api.get_instrument_bars(TDXParams.KLINE_TYPE_DAILY, params[0], params[1])
                assert data is not None
                assert type(data) is list
                assert len(data) > 0

            log.info("查询代码列表")
            data = api.get_instrument_info(10000, 98)
            assert data is not None
            assert type(data) is list
            assert len(data) > 0
    except socket.timeout as e:
        pass


def test_get_history_instrument_bars_range():
    log.info("查询代码列表")
    api = TdxExHq_API(auto_retry=True)
    try:
        with api.connect('61.152.107.141', 7727):
            data = api.get_history_instrument_bars_range(74, "BABA", 20170613,20170620)
            assert data is not None
            assert type(data) is list
            assert len(data) > 0
    except socket.timeout as e:
        pass