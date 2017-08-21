# coding=utf-8

from pytdx.parser.base import BaseParser
from pytdx.helper import get_datetime, get_volume, get_price, get_time
from collections import OrderedDict
import struct
import six


class GetTransactionData(BaseParser):

    def setParams(self, market, code, start, count):
        if type(code) is six.text_type:
            code = code.encode("utf-8")
        pkg = bytearray.fromhex('01 01 08 00 03 01 12 00 12 00 fc 23')
        pkg.extend(struct.pack("<B9siH", market, code, start, count))
        self.send_pkg = pkg

    def parseResponse(self, body_buf):

        pos = 0
        market, code, _, num = struct.unpack('<B9s4sH', body_buf[pos: pos + 16])
        pos += 16
        result = []
        for i in range(num):

            (raw_time, price, volume, zengcang, nature) = struct.unpack("<HIIiH", body_buf[pos: pos + 16])

            pos += 16
            hour = raw_time // 60
            minute = raw_time % 60

            result.append(OrderedDict([
                ("hour", hour),
                ("minute", minute),
                ("price", price),
                ("volume", volume),
                ("zengcang", zengcang),
                ("nature", nature),
                ("nature_mark", nature // 10000),
                ("nature_value", nature % 10000)
            ]))

        return result
