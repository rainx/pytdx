from pytdx.async.async_parser import *
from pytdx.async.async_client import *
import asyncio
from pytdx.hq import TdxHq_API
import timeit
from functools import partial


@asyncio.coroutine
def async_security_bars(loop):
    client = AsyncClient(loop)
    yield from client.connect('101.227.73.20', 7709)
    cmd = GetSecurityBarsCmd(client)
    cmd.setParams(9, 0, '000001', 0, 80)
    yield from cmd.call_api()


def test_security_bars():
    api = TdxHq_API()
    with api.connect('101.227.73.20', 7709):
        for i in range(30):
            api.get_security_bars(9, 0, '000001', 0, 80)


def test_async():
    loop = asyncio.get_event_loop()
    tasks = [
        async_security_bars(loop) for i in range(30)
    ]
    loop.run_until_complete(asyncio.wait(tasks))


print(timeit.timeit(test_async, number=1))
print(timeit.timeit(test_security_bars, number=1))
