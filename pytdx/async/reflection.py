# coding: utf-8

import six

if six.PY2:
    raise NotImplementedError("I am only working for Python3")

from pytdx.parser.base import BaseParser
import asyncio
from pytdx.parser.base import SendPkgNotReady, SendRequestPkgFails, ResponseRecvFails
from pytdx.parser.setup_commands import (
    SetupCmd1,
    SetupCmd2,
    SetupCmd3
)
from pytdx.log import DEBUG, log
import struct
import zlib
from pytdx.async.pool import ConnectionPool
import timeit


def make_async_parser(parser, connection):
    """
    通过反射，重新绑定Parser 的 call_api 和 _call_api 方法
    :param parser:
    :return:
    """

    @asyncio.coroutine
    def call_api(self):
        if self.lock:
            with self.lock:
                log.debug("sending thread lock api call")
                result = yield from self._call_api()
        else:
            result = yield from self._call_api()
        return result

    @asyncio.coroutine
    def _call_api(self):
        if not self.send_pkg:
            SendPkgNotReady("send pkg not ready")

        yield from connection.send(self.send_pkg)
        head_buf = yield from connection.recv(self.rsp_header_len)
        if len(head_buf) == self.rsp_header_len:
            _, _, _, zipsize, unzipsize = struct.unpack("<IIIHH", head_buf)
            body_buf = bytearray()

            while True:
                buf = yield from connection.recv(zipsize)
                len_buf = len(buf)
                body_buf.extend(buf)
                if not (buf) or len_buf == 0 or len(body_buf) == zipsize:
                    break

            if len(buf) == 0:
                log.debug("接收数据体失败服务器断开连接")
                raise ResponseRecvFails("接收数据体失败服务器断开连接")
            if zipsize == unzipsize:
                log.debug("不需要解压")
            else:
                log.debug("需要解压")
                unziped_data = zlib.decompress(body_buf)
                body_buf = unziped_data
                ## 解压
            if DEBUG:
                log.debug("recv body: ")
                log.debug(body_buf)

            return self.parseResponse(body_buf)

    setattr(parser, "call_api", call_api)
    setattr(parser, "_call_api", _call_api)

    return parser(None, None)


if __name__ == '__main__':
    from pytdx.parser.get_security_bars import GetSecurityBarsCmd
    from pytdx.hq import TdxHq_API
    import pprint

    def time_async():

        pool = ConnectionPool(ip='101.227.73.20', port=7709)

        def exec_command(pool,cmd):

            connection = pool.get_connection()

            if not connection.connected:
                yield from make_async_parser(SetupCmd1, connection).call_api()

                yield from  make_async_parser(SetupCmd2, connection).call_api()

                yield from make_async_parser(SetupCmd3, connection).call_api()


            async_cmd = make_async_parser(cmd, connection)

            async_cmd.setParams(8, 0, '000001', 0, 80)

            data = yield from async_cmd.call_api()
            pool.release(connection)

            return data

        res = [exec_command(pool,GetSecurityBarsCmd) for i in range(100)]
        pool.run_until_complete(asyncio.wait(res))

    def time_orig():
        api = TdxHq_API()
        api.connect(ip='218.108.98.244', port=7709)

        for i in range(100):
            api.get_security_bars(8, 0, '000001', 0, 80)

    # print(timeit.timeit(time_async, number=1))
    print(timeit.timeit(time_orig, number=1))