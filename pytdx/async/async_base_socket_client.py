#coding: utf-8

import datetime
import asyncio


class AsyncTrafficStatSocket(object):
    """
    实现支持流量统计的socket类
    """

    def __init__(self, reader, writer, loop):
        super(AsyncTrafficStatSocket, self).__init__()
        # 流量统计相关
        self.send_pkg_num = 0  # 发送次数
        self.recv_pkg_num = 0  # 接收次数
        self.send_pkg_bytes = 0  # 发送字节
        self.recv_pkg_bytes = 0  # 接收字节数
        self.first_pkg_send_time = None  # 第一个数据包发送时间

        self.last_api_send_bytes = 0  # 最近的一次api调用的发送字节数
        self.last_api_recv_bytes = 0  # 最近一次api调用的接收字节数
        self.reader = reader
        self.writer = writer
        self.loop = loop

    @asyncio.coroutine
    def send(self, data, flags=None):
        nsended = len(data)
        self.writer.write(data)
        yield self.writer.drain()
        if self.first_pkg_send_time is None:
            self.first_pkg_send_time = datetime.datetime.now()
        self.send_pkg_num += 1
        self.send_pkg_bytes += nsended
        return nsended

    @asyncio.coroutine
    def recv(self, buffersize, flags=None):
        head_buf = yield from self.reader.read(buffersize)
        self.recv_pkg_num += 1
        self.recv_pkg_bytes += buffersize
        return head_buf

    def set_last_api_sent(self,num):
        self.last_api_recv_bytes = num

    def set_last_api_received(self,num):
        self.last_api_recv_bytes = num