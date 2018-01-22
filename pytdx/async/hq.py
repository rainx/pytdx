# coding: utf-8

from pytdx.async.pool import ConnectionPool
from pytdx.async.reflection import make_async_parser
import timeit
import random
import pandas as pd
from pytdx.base_socket_client import update_last_ack_time

from pytdx.parser.get_block_info import (GetBlockInfo, GetBlockInfoMeta,
                                         get_and_parse_block_info)
from pytdx.parser.get_company_info_category import GetCompanyInfoCategory
from pytdx.parser.get_company_info_content import GetCompanyInfoContent
from pytdx.parser.get_finance_info import GetFinanceInfo
from pytdx.parser.get_history_minute_time_data import GetHistoryMinuteTimeData
from pytdx.parser.get_history_transaction_data import GetHistoryTransactionData
from pytdx.parser.get_index_bars import GetIndexBarsCmd
from pytdx.parser.get_minute_time_data import GetMinuteTimeData
from pytdx.parser.get_security_bars import GetSecurityBarsCmd
from pytdx.parser.get_security_count import GetSecurityCountCmd
from pytdx.parser.get_security_list import GetSecurityList
from pytdx.parser.get_security_quotes import GetSecurityQuotesCmd
from pytdx.parser.get_transaction_data import GetTransactionData
from pytdx.parser.get_xdxr_info import GetXdXrInfo

from functools import wraps
import struct

async def receive_all(send_pkg, connection):
    await connection.send(send_pkg)
    head_buf = await connection.recv(0x10)
    if len(head_buf) == 0x10:
        _, _, _, zipsize, unzipsize = struct.unpack("<IIIHH", head_buf)
        body_buf = bytearray()
        while True:
            buf = await connection.recv(zipsize)
            body_buf.extend(buf)
            if not (buf) or len(buf) == 0 or len(body_buf) == zipsize:
                break


def exec_command(func):
    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        connection = await self.pool.get_connection()

        if not connection.connected:
            await receive_all(bytearray.fromhex(u'0c 02 18 93 00 01 03 00 03 00 0d 00 01'), connection)
            await receive_all(bytearray.fromhex(u'0c 02 18 94 00 01 03 00 03 00 0d 00 02'), connection)
            await receive_all(bytearray.fromhex(u'0c 03 18 99 00 01 20 00 20 00 db 0f d5'
                                      u'd0 c9 cc d6 a4 a8 af 00 00 00 8f c2 25'
                                      u'40 13 00 00 d5 00 c9 cc bd f0 d7 ea 00'
                                      u'00 00 02'), connection)

        data = await func(self, *args, **kwargs, connection=connection)
        return data

    return wrapper


class ATdxHq_API():

    def __init__(self, ip='101.227.73.20', port=7709, auto_retry=False, raise_exception=True):
        self.pool = ConnectionPool(ip=ip, port=port)
        self.auto_retry = auto_retry
        self.raise_exception = raise_exception
        connection = None

    # Notice：，如果一个股票当天停牌，那天的K线还是能取到，成交量为0
    @update_last_ack_time
    @exec_command
    def get_security_bars(self, category, market, code, start, count, connection=None):
        cmd = make_async_parser(GetSecurityBarsCmd, connection)
        cmd.setParams(category, market, code, start, count)
        return cmd.call_api()

    @update_last_ack_time
    @exec_command
    def get_index_bars(self, category, market, code, start, count, connection=None):
        cmd = make_async_parser(GetIndexBarsCmd, connection)
        cmd.setParams(category, market, code, start, count)
        return cmd.call_api()

    @update_last_ack_time
    @exec_command
    def get_security_quotes(self, all_stock, code=None, connection=None):
        """
        支持三种形式的参数
        get_security_quotes(market, code )
        get_security_quotes((market, code))
        get_security_quotes([(market1, code1), (market2, code2)] )
        :param all_stock （market, code) 的数组
        :param code{optional} code to query
        :return:
        """

        if code is not None:
            all_stock = [(all_stock, code)]
        elif (isinstance(all_stock, list) or isinstance(all_stock, tuple)) \
                and len(all_stock) == 2 and type(all_stock[0]) is int:
            all_stock = [all_stock]

        cmd = make_async_parser(GetSecurityQuotesCmd, connection)
        cmd.setParams(all_stock)
        return cmd.call_api()

    @update_last_ack_time
    @exec_command
    def get_security_count(self, market, connection=None):
        cmd = make_async_parser(GetSecurityCountCmd, connection)
        cmd.setParams(market)
        return cmd.call_api()

    @update_last_ack_time
    @exec_command
    def get_security_list(self, market, start, connection=None):
        cmd = make_async_parser(GetSecurityList, connection)
        cmd.setParams(market, start)
        return cmd.call_api()

    @update_last_ack_time
    @exec_command
    def get_minute_time_data(self, market, code, connection=None):
        cmd = make_async_parser(GetMinuteTimeData, connection)
        cmd.setParams(market, code)
        return cmd.call_api()

    @update_last_ack_time
    @exec_command
    def get_history_minute_time_data(self, market, code, date, connection=None):
        cmd = make_async_parser(GetHistoryMinuteTimeData, connection)
        cmd.setParams(market, code, date)
        return cmd.call_api()

    @update_last_ack_time
    @exec_command
    def get_transaction_data(self, market, code, start, count, connection=None):
        cmd = make_async_parser(GetTransactionData, connection)
        cmd.setParams(market, code, start, count)
        return cmd.call_api()

    @update_last_ack_time
    @exec_command
    def get_history_transaction_data(self, market, code, start, count, date, connection=None):
        cmd = make_async_parser(GetHistoryTransactionData, connection)
        cmd.setParams(market, code, start, count, date)
        return cmd.call_api()

    @update_last_ack_time
    @exec_command
    def get_company_info_category(self, market, code, connection=None):
        cmd = make_async_parser(GetCompanyInfoCategory, connection)
        cmd.setParams(market, code)
        return cmd.call_api()

    @update_last_ack_time
    @exec_command
    def get_company_info_content(self, market, code, filename, start, length, connection=None):
        cmd = make_async_parser(GetCompanyInfoContent, connection)
        cmd.setParams(market, code, filename, start, length)
        return cmd.call_api()

    @update_last_ack_time
    @exec_command
    def get_xdxr_info(self, market, code, connection=None):
        cmd = make_async_parser(GetXdXrInfo, connection)
        cmd.setParams(market, code)
        return cmd.call_api()

    @update_last_ack_time
    @exec_command
    def get_finance_info(self, market, code, connection=None):
        cmd = make_async_parser(GetFinanceInfo, connection)
        cmd.setParams(market, code)
        return cmd.call_api()

    @update_last_ack_time
    @exec_command
    def get_block_info_meta(self, blockfile, connection=None):
        cmd = make_async_parser(GetBlockInfoMeta, connection)
        cmd.setParams(blockfile)
        return cmd.call_api()

    @update_last_ack_time
    @exec_command
    def get_block_info(self, blockfile, start, size, connection=None):
        cmd = make_async_parser(GetBlockInfo, connection)
        cmd.setParams(blockfile, start, size)
        return cmd.call_api()

    def get_and_parse_block_info(self, blockfile):
        return get_and_parse_block_info(self, blockfile)

    @update_last_ack_time
    @exec_command
    def do_heartbeat(self):
        return self.get_security_count(random.randint(0, 1), connection=None)

    def run_until_complete(self, *args, **kwargs):
        return self.pool.run_until_complete(*args, **kwargs)

    @update_last_ack_time
    @exec_command
    def get_k_data(self, code, start_date, end_date, connection=None):
        # 具体详情参见 https://github.com/rainx/pytdx/issues/5
        # 具体详情参见 https://github.com/rainx/pytdx/issues/21
        def __select_market_code(code):
            code = str(code)
            if code[0] in ['5', '6', '9'] or code[:3] in ["009", "126", "110", "201", "202", "203", "204"]:
                return 1
            return 0

        # 新版一劳永逸偷懒写法zzz
        market_code = 1 if str(code)[0] == '6' else 0
        # https://github.com/rainx/pytdx/issues/33
        # 0 - 深圳， 1 - 上海

        data = pd.concat([self.to_df(self.get_security_bars(9, __select_market_code(
            code), code, (9 - i) * 800, 800)) for i in range(10)], axis=0)

        data = data.assign(date=data['datetime'].apply(lambda x: str(x)[0:10])).assign(code=str(code)) \
                   .set_index('date', drop=False, inplace=False) \
                   .drop(['year', 'month', 'day', 'hour', 'minute', 'datetime'], axis=1)[start_date:end_date]
        return data.assign(date=data['date'].apply(lambda x: str(x)[0:10]))


if __name__ == '__main__':
    import asyncio


    def main():
        api = ATdxHq_API(ip='218.108.98.244')

        res = [api.get_security_bars(8, 0, '000001', 0, 80) for i in range(100)]

        api.run_until_complete(asyncio.wait(res))


    print(timeit.timeit(main, number=1))
