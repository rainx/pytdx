# coding=utf-8

from pytdx.log import DEBUG, log
import zlib
import struct
import sys


class SocketClientNotReady(BaseException):
    pass


class SendPkgNotReady(BaseException):
    pass


class SendRequestPkgFails(BaseException):
    pass


class ResponseHeaderRecvFails(BaseException):
    pass


class ResponseRecvFails(BaseException):
    pass

RSP_HEADER_LEN = 0x10

class BaseParser(object):

    def __init__(self, client, lock=None):
        self.client = client
        self.data = None
        self.send_pkg = None

        self.rsp_header = None
        self.rsp_body = None
        self.rsp_header_len = RSP_HEADER_LEN

        if lock:
            self.lock = lock
        else:
            self.lock = None

    def setParams(self, *args, **xargs):
        """
        构建请求
        :return:
        """
        pass

    def parseResponse(self, body_buf):
        pass

    def setup(self):
        pass


    def call_api(self):
        if self.lock:
            with self.lock:
                log.debug("sending thread lock api call")
                result = self._call_api()
        else:
            result = self._call_api()
        return result
    def _call_api(self):

        self.setup()

        if not(self.client):
            raise SocketClientNotReady("socket client not ready")

        if not(self.send_pkg):
            raise SendPkgNotReady("send pkg not ready")

        nsended = self.client.send(self.send_pkg)

        if DEBUG:
            log.debug("send package:" + str(self.send_pkg))
        if nsended != len(self.send_pkg):
            log.debug("send bytes error")
            raise SendRequestPkgFails("send fails")
        else:
            head_buf = self.client.recv(self.rsp_header_len)
            if DEBUG:
                log.debug("recv head_buf:" + str(head_buf)  + " |len is :" + str(len(head_buf)))
            if len(head_buf) == self.rsp_header_len:
                _, _, _, zipsize, unzipsize = struct.unpack("<IIIHH", head_buf)
                if DEBUG:
                    log.debug("zip size is: " + str(zipsize))
                body_buf = bytearray()

                while True:
                    buf = self.client.recv(zipsize)
                    body_buf.extend(buf)
                    if not(buf) or len(buf) == 0 or len(body_buf) == zipsize:
                        break
                if len(buf) == 0:
                    log.debug("接收数据体失败服务器断开连接")
                    raise ResponseRecvFails("接收数据体失败服务器断开连接")
                if zipsize == unzipsize:
                    log.debug("不需要解压")
                else:
                    log.debug("需要解压")
                    if sys.version_info[0] == 2:
                        unziped_data = zlib.decompress(buffer(body_buf))
                    else:
                        unziped_data = zlib.decompress(body_buf)
                    body_buf = unziped_data
                    ## 解压
                if DEBUG:
                    log.debug("recv body: ")
                    log.debug(body_buf)

                return self.parseResponse(body_buf)

            else:
                log.debug("head_buf is not 0x10")
                raise ResponseHeaderRecvFails("head_buf is not 0x10")

