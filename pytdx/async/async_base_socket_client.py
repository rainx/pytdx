#coding: utf-8

import datetime
import asyncio


class AsyncTrafficStatSocket(object):
    """
    实现支持流量统计的socket类
    """

    def __init__(self, ip, port, loop, pool):
        super(AsyncTrafficStatSocket, self).__init__()
        # 流量统计相关
        self.send_pkg_num = 0  # 发送次数
        self.recv_pkg_num = 0  # 接收次数
        self.send_pkg_bytes = 0  # 发送字节
        self.recv_pkg_bytes = 0  # 接收字节数
        self.first_pkg_send_time = None  # 第一个数据包发送时间

        self.last_api_send_bytes = 0  # 最近的一次api调用的发送字节数
        self.last_api_recv_bytes = 0  # 最近一次api调用的接收字节数
        self.reader = None
        self.writer = None
        self.ip = ip
        self.port = port
        self.loop = loop

        self.pool = pool

        self.connected = False

    async def connect(self):
        self.reader, self.writer = await asyncio.open_connection(self.ip, self.port, loop=self.loop)
        self.connected = True
        return self

    def disconnect(self):
        self.writer.close()

    async def send(self, data, flags=None):
        if not (self.reader and self.writer):
            await self.connect()
        nsended = len(data)
        self.writer.write(data)
        # yield from self.writer.drain()
        if self.first_pkg_send_time is None:
            self.first_pkg_send_time = datetime.datetime.now()
        self.send_pkg_num += 1
        self.send_pkg_bytes += nsended
        return nsended

    async def recv(self, buffersize, flags=None):
        if not (self.reader and self.writer):
            await self.connect()
        head_buf = await self.reader.read(buffersize)
        self.recv_pkg_num += 1
        self.recv_pkg_bytes += buffersize
        return head_buf

    def set_last_api_sent(self,num):
        self.last_api_recv_bytes = num

    def set_last_api_received(self,num):
        self.last_api_recv_bytes = num