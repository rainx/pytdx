# coding: utf-8

import os
import asyncio
from itertools import chain
from .async_base_socket_client import AsyncTrafficStatSocket
import pandas as pd
import os


class ConnectionPool(object):

    def __init__(self, ip, port, max_connections=100, loop=None):

        self.pid = os.getpid()
        self.max_connections = max_connections

        self.loop = loop or asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.ip = ip
        self.port = port
        self._available_connections = []
        self.created_connect = 0
        self._in_use_connections = set()

    async def get_connection(self):
        try:
            if self.created_connect >= self.max_connections:
                # if self.created_connect > self.max_connections:
                while len(self._available_connections) == 0:
                    await asyncio.sleep(0.2)
            connection = self._available_connections.pop()
        except IndexError:
            connection = self.make_connection()

        self._in_use_connections.add(connection)
        return connection

    def make_connection(self):
        self.created_connect += 1
        return AsyncTrafficStatSocket(self.ip, self.port, self.loop, self)

    def release(self, connection):
        self._in_use_connections.remove(connection)
        self._available_connections.append(connection)

    def disconnect(self):
        "Disconnects all connections in the pool"
        all_conns = chain(self._available_connections,
                          self._in_use_connections)
        for connection in all_conns:
            connection.disconnect()

    def run_until_complete(self, *args, **kwargs):
        return self.loop.run_until_complete(*args, **kwargs)
