import asyncio


class AsyncClient(object):
    reader = None
    writer = None

    def __init__(self, loop, multithread=False, heartbeat=False, auto_retry=False, raise_exception=False):
        self.loop = loop

    async def connect(self, ip='101.227.73.20', port=7709):
        self.reader, self.writer = await asyncio.open_connection(ip, port, loop=self.loop)

    def disconnect(self):
        self.writer.close()

    def close(self):
        self.disconnect()

    def get_traffic_stats(self):
        pass

    def send_raw_pkg(self, pkg):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def to_df(self, v):
        pass

    def send(self, data, mode=None):
         self.writer.write(data)

    @asyncio.coroutine
    def recv(self, pkg_len, mode=None):
        return (yield from self.reader.read(pkg_len))
