# coding=utf-8

#
# Just for practising
#


import os
import socket
import sys
import pandas as pd

if __name__ == '__main__':
    sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from pytdx.log import DEBUG, log
from pytdx.parser.get_security_bars import GetSecurityBarsCmd
from pytdx.parser.get_security_quotes import GetSecurityQuotesCmd
from pytdx.parser.get_security_count import GetSecurityCountCmd
from pytdx.parser.get_security_list import GetSecurityList
from pytdx.parser.get_index_bars import GetIndexBarsCmd
from pytdx.parser.get_minute_time_data import GetMinuteTimeData
from pytdx.parser.get_history_minute_time_data import GetHistoryMinuteTimeData
from pytdx.parser.get_transaction_data import GetTransactionData
from pytdx.parser.get_history_transaction_data import GetHistoryTransactionData
from pytdx.parser.get_company_info_category import GetCompanyInfoCategory
from pytdx.parser.get_company_info_content import GetCompanyInfoContent
from pytdx.parser.get_xdxr_info import GetXdXrInfo
from pytdx.parser.get_finance_info import GetFinanceInfo
from pytdx.util import get_real_trade_date,trade_date_sse
from pytdx.params import TDXParams

from pytdx.parser.setup_commands import SetupCmd1, SetupCmd2, SetupCmd3
import threading,datetime

CONNECT_TIMEOUT = 5.000
RECV_HEADER_LEN = 0x10

class TdxHq_API(object):

    def __init__(self, multithread=False):
        self.need_setup = True
        if multithread:
            self.lock = threading.Lock()
        else:
            self.lock = None

    def connect(self, ip, port):
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
        SetupCmd1(self.client).call_api()
        SetupCmd2(self.client).call_api()
        SetupCmd3(self.client).call_api()

    #### API List

    def get_security_bars(self, category, market, code, start, count):
        cmd = GetSecurityBarsCmd(self.client, lock=self.lock)
        cmd.setParams(category, market, code, start, count)
        return cmd.call_api()

    def get_index_bars(self, category, market, code, start, count):
        cmd = GetIndexBarsCmd(self.client, lock=self.lock)
        cmd.setParams(category, market, code, start, count)
        return cmd.call_api()

    def get_security_quotes(self, all_stock):
        cmd = GetSecurityQuotesCmd(self.client, lock=self.lock)
        cmd.setParams(all_stock)
        return cmd.call_api()

    def get_security_count(self, market):
        cmd = GetSecurityCountCmd(self.client, lock=self.lock)
        cmd.setParams(market)
        return cmd.call_api()

    def get_security_list(self, market, start):
        cmd = GetSecurityList(self.client, lock=self.lock)
        cmd.setParams(market, start)
        return cmd.call_api()

    def get_minute_time_data(self, market, code):
        cmd = GetMinuteTimeData(self.client, lock=self.lock)
        cmd.setParams(market, code)
        return cmd.call_api()

    def get_history_minute_time_data(self, market, code, date):
        cmd = GetHistoryMinuteTimeData(self.client, lock=self.lock)
        cmd.setParams(market, code, date)
        return cmd.call_api()

    def get_transaction_data(self, market, code, start, count):
        cmd = GetTransactionData(self.client, lock=self.lock)
        cmd.setParams(market, code, start, count)
        return cmd.call_api()

    def get_history_transaction_data(self, market, code, start, count, date):
        cmd = GetHistoryTransactionData(self.client, lock=self.lock)
        cmd.setParams(market, code, start, count, date)
        return cmd.call_api()

    def get_company_info_category(self, market, code):
        cmd = GetCompanyInfoCategory(self.client, lock=self.lock)
        cmd.setParams(market, code)
        return cmd.call_api()

    def get_company_info_content(self, market, code, filename, start, length):
        cmd = GetCompanyInfoContent(self.client, lock=self.lock)
        cmd.setParams(market, code, filename, start, length)
        return cmd.call_api()

    def get_xdxr_info(self, market, code):
        cmd = GetXdXrInfo(self.client, lock=self.lock)
        cmd.setParams(market, code)
        return cmd.call_api()

    def get_finance_info(self, market, code):
        cmd = GetFinanceInfo(self.client, lock=self.lock)
        cmd.setParams(market, code)
        return cmd.call_api()


    def get_k_data(self, code, start,end):
        # 具体详情参见 https://github.com/rainx/pytdx/issues/5
        if str(code)[0]=='6':
            #0 - 深圳， 1 - 上海
            market_code=1
        else:
            market_code=0
        start_date=get_real_trade_date(start,1)
        end_date=get_real_trade_date(end,-1)
        index_0=str(datetime.date.today())
        index_of_index_0=trade_date_sse.index(index_0)
        index_of_index_end=trade_date_sse.index(end_date)
        index_of_index_start=trade_date_sse.index(start_date)
        
        index_of_end=index_of_index_0-index_of_index_end
        index_length=index_of_index_end+1-index_of_index_start
        return  self.get_security_bars(9, market_code, code,index_of_end, index_length)  # 返回普通list
        

    def to_df(self, v):
        if isinstance(v, list):
            return pd.DataFrame(data=v)
        elif isinstance(v, dict):
            return pd.DataFrame(data=[v,])
        else:
            return pd.DataFrame(data=[{'value': v}])

if __name__ == '__main__':
    import pprint

    api = TdxHq_API()
    if api.connect('101.227.73.20', 7709):
        log.info("获取股票行情")
        stocks = api.get_security_quotes([(0, "000001"), (1, "600300")])
        pprint.pprint(stocks)
        log.info("获取k线")
        data = api.get_security_bars(9,0, '000001', 4, 3)
        pprint.pprint(data)
        log.info("获取 深市 股票数量")
        pprint.pprint(api.get_security_count(0))
        log.info("获取股票列表")
        stocks = api.get_security_list(1, 255)
        pprint.pprint(stocks)
        log.info("获取指数k线")
        data = api.get_index_bars(9,1, '000001', 1, 2)
        pprint.pprint(data)
        log.info("查询分时行情")
        data = api.get_minute_time_data(TDXParams.MARKET_SH, '600300')
        pprint.pprint(data)
        log.info("查询历史分时行情")
        data = api.get_history_minute_time_data(TDXParams.MARKET_SH, '600300', 20161209)
        pprint.pprint(data)
        log.info("查询分时成交")
        data = api.get_transaction_data(TDXParams.MARKET_SZ, '000001', 0, 30)
        pprint.pprint(data)
        log.info("查询历史分时成交")
        data = api.get_history_transaction_data(TDXParams.MARKET_SZ, '000001', 0, 10, 20170209)
        pprint.pprint(data)
        log.info("查询公司信息目录")
        data = api.get_company_info_category(TDXParams.MARKET_SZ, '000001')
        pprint.pprint(data)
        log.info("读取公司信息-最新提示")
        data = api.get_company_info_content(0, '000001', '000001.txt', 0, 10)
        pprint.pprint(data)
        log.info("读取除权除息信息")
        data = api.get_xdxr_info(1, '600300')
        pprint.pprint(data)
        log.info("读取财务信息")
        data = api.get_finance_info(0, '000001')
        pprint.pprint(data)
        log.info("日线级别k线获取函数")
        data =api.get_k_data('000001','2017-07-01','2017-07-10')
        pprint.pprint(data)

        api.disconnect()



