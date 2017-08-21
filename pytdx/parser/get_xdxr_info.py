# coding=utf-8

from pytdx.parser.base import BaseParser
from pytdx.helper import get_datetime, get_volume, get_price, get_time
from collections import OrderedDict
import struct
import six
"""
need to fix

get_volume ?

4098 ---> 3.0

2434.0062499046326 ---> 2.6

1218.0031249523163 ---> 2.3

"""

class GetXdXrInfo(BaseParser):

    def setParams(self, market, code):
        if type(code) is six.text_type:
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

        def _get_v(v):
            if v == 0:
                return 0
            else:
                return get_volume(v)

        for i in range(num):
            market, code = struct.unpack(u"<B6s", body_buf[:7])
            pos += 7
            # noused = struct.unpack(u"<B", body_buf[pos: pos+1])
            pos += 1 #skip a byte
            year, month, day, hour, minite, pos = get_datetime(9, body_buf, pos)
            (category, ) = struct.unpack(u"<B", body_buf[pos: pos+1])
            pos += 1



            # b'\x00\xe8\x00G' => 33000.00000
            # b'\x00\xc0\x0fF' => 9200.00000
            # b'\x00@\x83E' => 4200.0000

            suogu = None
            panqianliutong, panhouliutong, qianzongguben, houzongguben = None, None, None, None
            songzhuangu, fenhong, peigu, peigujia = None, None, None, None
            if category == 1:
                fenhong, peigujia, songzhuangu, peigu  = struct.unpack("<ffff", body_buf[pos: pos + 16])
            elif category == 11:
                (_, _, suogu_raw, _) = struct.unpack("<IIII", body_buf[pos: pos + 16])
                suogu = _get_v(suogu_raw)
            else :
                panqianliutong_raw, qianzongguben_raw, panhouliutong_raw, houzongguben_raw = struct.unpack("<IIII", body_buf[pos: pos + 16])
                panqianliutong = _get_v(panqianliutong_raw)
                panhouliutong = _get_v(panhouliutong_raw)
                qianzongguben = _get_v(qianzongguben_raw)
                houzongguben = _get_v(houzongguben_raw)

            pos += 16

            row = OrderedDict(
                [
                    ('year', year),
                    ('month', month),
                    ('day', day),
                    ('category', category),
                    ('fenhong', fenhong),
                    ('peigujia', peigujia),
                    ('songzhuangu', songzhuangu),
                    ('peigu', peigu),
                    ('suogu', suogu),
                    ('panqianliutong', panqianliutong),
                    ('panhouliutong', panhouliutong),
                    ('qianzongguben', qianzongguben),
                    ('houzongguben', houzongguben),
                ]
            )
            rows.append(row)

        return rows


if __name__ == '__main__':

    from pytdx.hq import TdxHq_API
    api = TdxHq_API()
    with api.connect():
        print(api.to_df(api.get_xdxr_info(1, '600300')))

