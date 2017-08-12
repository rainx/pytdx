# coding=utf-8

from pytdx.parser.base import BaseParser
from pytdx.helper import get_datetime, get_volume, get_price
from collections import OrderedDict
import struct


class GetHistoryTransactionData(BaseParser):

    def setParams(self, market, code, start, count, date):
        # print(six.text_type)

        # if type(code) is six.text_type:
        code = code.encode("utf-8")
        # if type(date) is (type(date) is six.text_type) or (type(date) is six.binary_type):
        #     date = int(date)

        # pkg1 = bytearray.fromhex('01 01 30 00 02 01 16 00 16 00 06 24 3b c8 33 01 1f 30 30 30 32 30 00 00 00 01 00 00 00 00 f0 00')
        pkg = bytearray.fromhex('01 01 30 00 02 01 16 00 16 00 06 24')
        pkg.extend(struct.pack("<IB9siH", date, market, code, start, count))
        self.send_pkg = pkg

    def parseResponse(self, body_buf):

        pos = 0
        market, code, _, num = struct.unpack('<B9s4sH', body_buf[pos: pos + 16])
        pos += 16
        result = []
        for i in range(num):

            (raw_time, price, avg_price, volume, amount) = struct.unpack("<HIIIH", body_buf[pos: pos + 16])

            pos += 16
            hour = raw_time // 60
            minute = raw_time % 60

            result.append(OrderedDict([
                ("hour", hour),
                ("minute", minute),
                ("price", price),
                ("avg_price", avg_price),
                ("volume", volume),
                ("open_interest", amount),
            ]))

        return result
