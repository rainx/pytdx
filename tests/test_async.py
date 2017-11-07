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
    cmd.setParams(9, 0, '000001', 4, 3)
    data = yield from cmd.call_api()
    return data


def test_security_bars():
    api = TdxHq_API()
    with api.connect('101.227.73.20', 7709):
        data = api.get_security_bars(9, 0, '000001', 4, 3)
        return data


def test_async():
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(async_security_bars(loop))


# print(test_async())
# print(test_security_bars())
# print(timeit.timeit(test_async, number=5))
# print(timeit.timeit(test_security_bars, number=5))
