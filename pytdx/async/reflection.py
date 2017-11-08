#coding: utf-8

import six
if six.PY2:
    raise NotImplementedError("I am only working for Python3")

from pytdx.parser.base import BaseParser
import asyncio
from pytdx.parser.base import SendPkgNotReady, SendRequestPkgFails, ResponseRecvFails
from pytdx.log import DEBUG, log
import struct
import zlib


def make_async_parser(parser: BaseParser):
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

        self.client.send(self.send_pkg)
        head_buf = yield from self.client.recv(self.rsp_header_len)
        if len(head_buf) == self.rsp_header_len:
            _, _, _, zipsize, unzipsize = struct.unpack("<IIIHH", head_buf)
            body_buf = bytearray()

            while True:
                buf = yield from self.client.recv(zipsize)
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

    return parser


