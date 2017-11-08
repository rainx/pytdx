from pytdx.parser.base import SendPkgNotReady, SendRequestPkgFails, ResponseRecvFails
import asyncio
from pytdx.log import DEBUG, log
import struct
import zlib
import sys
from pytdx.helper import get_datetime, get_volume, get_price
from collections import OrderedDict
import struct
import six

RSP_HEADER_LEN = 0x10

try:
    import cython

    if cython.compiled:
        def buffer(x):
            return x
except ImportError:
    pass


class AsyncParser(object):
    send_pkg = None
    rsp_header_len = RSP_HEADER_LEN

    def __init__(self, client,lock=None):
        self.client = client
        self.lock = lock

    def parseResponse(self, body_buf):
        return body_buf

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


class SetupCmd1(AsyncParser):
    send_pkg = bytearray.fromhex(u'0c 02 18 93 00 01 03 00 03 00 0d 00 01')

    def parseResponse(self, body_buf):
        return body_buf

    def call_api(self):
        pass


class SetupCmd2(AsyncParser):
    bytearray.fromhex(u'0c 02 18 94 00 01 03 00 03 00 0d 00 02')

    def parseResponse(self, body_buf):
        return body_buf

    def call_api(self):
        pass


class SetupCmd3(AsyncParser):
    bytearray.fromhex(u'0c 03 18 99 00 01 20 00 20 00 db 0f d5'
                      u'd0 c9 cc d6 a4 a8 af 00 00 00 8f c2 25'
                      u'40 13 00 00 d5 00 c9 cc bd f0 d7 ea 00'
                      u'00 00 02')

    def parseResponse(self, body_buf):
        return body_buf

    def call_api(self):
        pass


class GetSecurityBarsCmd(AsyncParser):

    def setParams(self, category, market, code, start, count):
        if type(code) is six.text_type:
            code = code.encode("utf-8")

        self.category = category

        values = (
            0x10c,
            0x01016408,
            0x1c,
            0x1c,
            0x052d,
            market,
            code,
            category,
            1,
            start,
            count,
            0, 0, 0  # I + I +  H total 10 zero
        )

        pkg = struct.pack("<HIHHHH6sHHHHIIH", *values)
        self.send_pkg = pkg

    def parseResponse(self, body_buf):
        pos = 0

        (ret_count,) = struct.unpack("<H", body_buf[0: 2])
        pos += 2

        klines = []

        pre_diff_base = 0
        for i in range(ret_count):
            year, month, day, hour, minute, pos = get_datetime(self.category, body_buf, pos)

            price_open_diff, pos = get_price(body_buf, pos)
            price_close_diff, pos = get_price(body_buf, pos)

            price_high_diff, pos = get_price(body_buf, pos)
            price_low_diff, pos = get_price(body_buf, pos)

            (vol_raw,) = struct.unpack("<I", body_buf[pos: pos + 4])
            vol = get_volume(vol_raw)

            pos += 4
            (dbvol_raw,) = struct.unpack("<I", body_buf[pos: pos + 4])
            dbvol = get_volume(dbvol_raw)
            pos += 4

            open = self._cal_price1000(price_open_diff, pre_diff_base)

            price_open_diff = price_open_diff + pre_diff_base

            close = self._cal_price1000(price_open_diff, price_close_diff)
            high = self._cal_price1000(price_open_diff, price_high_diff)
            low = self._cal_price1000(price_open_diff, price_low_diff)

            pre_diff_base = price_open_diff + price_close_diff

            #### 为了避免python处理浮点数的时候，浮点数运算不精确问题，这里引入了多余的代码

            kline = OrderedDict([
                ("open", open),
                ("close", close),
                ("high", high),
                ("low", low),
                ("vol", vol),
                ("amount", dbvol),
                ("year", year),
                ("month", month),
                ("day", day),
                ("hour", hour),
                ("minute", minute),
                ("datetime", "%d-%02d-%02d %02d:%02d" % (year, month, day, hour, minute))
            ])
            klines.append(kline)
        return klines

    def _cal_price1000(self, base_p, diff):
        return float(base_p + diff)/1000