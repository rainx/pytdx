#
# This is a migrate to python verion of https://github.com/280185386/tdxhq/blob/master/TDXHQ/TDXHQ.cpp
# Just for practising
#
import os
import socket
import sys

if __name__ == '__main__':
    sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from pytdx.log import DEBUG, log
from pytdx.parser.get_security_bars import GetSecurityBarsCmd
from pytdx.parser.get_security_quotes import GetSecurityQuotesCmd
from pytdx.parser.get_security_count import GetSecurityCountCmd
from pytdx.parser.get_security_list import GetSecurityList

CONNECT_TIMEOUT = 5.000
RECV_HEADER_LEN = 0x10

class TdxHq_API(object):

    def __init__(self):
        ip = None
        current_ip = None
        client = None



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
        return True

    def disconnect(self):
        if self.client:
            log.debug("disconnecting")
            self.client.shutdown(socket.SHUT_RDWR)
            self.client.close()
            log.debug("disconnected")

    #### API List

    def get_security_bars(self, category, market, code, start, count):
        cmd = GetSecurityBarsCmd(self.client)
        cmd.setParams(category, market, code, start, count)
        return cmd.call_api()

    def get_security_quotes(self, all_stock):
        cmd = GetSecurityQuotesCmd(self.client)
        cmd.setParams(all_stock)
        return cmd.call_api()

    def get_security_count(self, market):
        cmd = GetSecurityCountCmd(self.client)
        cmd.setParams(market)
        return cmd.call_api()

    def get_security_list(self, market, start):
        cmd = GetSecurityList(self.client)
        cmd.setParams(market, start)
        return cmd.call_api()

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
        pprint.pprint(api.get_security_list(1, 255))
        api.disconnect()

