# coding=utf-8

from pytdx.parser.base import BaseParser
from pytdx.helper import get_datetime, get_volume, get_price, get_time
from collections import OrderedDict
import struct
"""
need to fix

get_volume ?

4098 ---> 3.0

2434.0062499046326 ---> 2.6

1218.0031249523163 ---> 2.3

"""

class GetXdXrInfo(BaseParser):

    def setParams(self, market, code):
        if type(code) is str:
            code = code.encode("utf-8")
        pkg = bytearray.fromhex(u'0c 1f 18 76 00 01 0b 00 0b 00 0f 00 01 00')
        pkg.extend(struct.pack("<B6s", market, code))
        self.send_pkg = pkg

    def parseResponse(self, body_buf):
        pos = 0

        if len(body_buf) < 11:
            return []

        pos += 9 # skip 9
        (num, ) = struct.unpack("<H", body_buf[pos:pos+2])
        pos += 2

        rows = []
        for i in range(num):
            market, code = struct.unpack(u"<B6s", body_buf[:7])
            pos += 7
            pos += 1 #skip a byte
            year, month, day, hour, minite, pos = get_datetime(9, body_buf, pos)
            pos += 1 #skip a byte



            # b'\x00\xe8\x00G' => 33000.00000
            # b'\x00\xc0\x0fF' => 9200.00000
            # b'\x00@\x83E' => 4200.0000

            cash_raw, peigu_price_raw, songgu_num_raw, peigu_percent_raw = struct.unpack("<IIII", body_buf[pos: pos + 16])
            pos += 16

            def _get_v(v):
                if v == 0:
                    return 0
                else:
                    return get_volume(v)


            row = OrderedDict(
                [
                    ('year', year),
                    ('month', month),
                    ('day', day),
                    ('cash', _get_v(cash_raw)),
                    ('peigu_price', _get_v(peigu_price_raw)),
                    ('songgu_num', _get_v(songgu_num_raw)),
                    ('peigu_percent', _get_v(peigu_percent_raw)),
                ]
            )
            rows.append(row)

        return rows
