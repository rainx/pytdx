# coding: utf-8

import six
from functools import partial

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
import asyncio

from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(1)


def make_async_parser(parser, connection):
    """
    通过反射，重新绑定Parser 的 call_api 和 _call_api 方法
    :param parser:
    :return:
    """

    async def call_api(self):
        if self.lock:
            with self.lock:
                log.debug("sending thread lock api call")
                result = await self._call_api()
        else:
            result = await self._call_api()
        return result

    async def _call_api(self):
        if not self.send_pkg:
            SendPkgNotReady("send pkg not ready")

        await connection.send(self.send_pkg)
        head_buf = await connection.recv(self.rsp_header_len)
        if len(head_buf) == self.rsp_header_len:
            _, _, _, zipsize, unzipsize = struct.unpack("<IIIHH", head_buf)
            body_buf = bytearray()

            while True:
                buf = await connection.recv(zipsize)
                len_buf = len(buf)
                body_buf.extend(buf)
                if not (buf) or len_buf == 0 or len(body_buf) == zipsize:
                    break

            connection.pool.release(connection)

            if len(buf) == 0:
                log.debug("接收数据体失败服务器断开连接")
                raise ResponseRecvFails("接收数据体失败服务器断开连接")
            if zipsize == unzipsize:
                log.debug("不需要解压")
            else:
                log.debug("需要解压")
                unziped_data = await asyncio.get_event_loop().run_in_executor(executor, zlib.decompress, body_buf)
                body_buf = unziped_data
                ## 解压
            if DEBUG:
                log.debug("recv body: ")
                log.debug(body_buf)

            return await asyncio.get_event_loop().run_in_executor(executor, self.parseResponse, body_buf)

    cmd = parser(None, None)

    setattr(cmd, "call_api", partial(call_api,cmd))
    setattr(cmd, "_call_api", partial(_call_api, cmd))

    return cmd
