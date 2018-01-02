import os
import asyncio
from itertools import chain
from .async_base_socket_client import AsyncTrafficStatSocket

import os


class ConnectionPool(object):

    def __init__(self, ip, port, max_connections=None, loop=None):

        self.pid = os.getpid()
        self.max_connections = max_connections or 2 ** 31

        self.loop = loop or asyncio.get_event_loop()
        self.ip = ip
        self.port = port
        self._available_connections = []
        self.created_connect = 0
        self._in_use_connections = set()

    def get_connection(self):
        try:
            connection = self._available_connections.pop()
        except IndexError:
            connection = self.make_connection()

        self._in_use_connections.add(connection)
        return connection

    def make_connection(self):
        if self.created_connect >= self.max_connections:
            raise ConnectionError("Too many connections")

        self.created_connect += 1
        return AsyncTrafficStatSocket(self.ip, self.port, self.loop)

    def release(self, connection):
        self._in_use_connections.remove(connection)
        self._available_connections.append(connection)

    def disconnect(self):
        "Disconnects all connections in the pool"
        all_conns = chain(self._available_connections,
                          self._in_use_connections)
        for connection in all_conns:
            connection.disconnect()

    def run_until_complete(self,*args,**kwargs):
        return self.loop.run_until_complete(*args,**kwargs)
