# coding=utf-8

from pytdx.parser.base import BaseParser
from pytdx.helper import get_datetime, get_volume, get_price
from collections import OrderedDict
import struct
"""
这个是获取大连商品的数据

OrderedDict([('market', 29),
              ('category', 3),
              ('name', '大连商品'),
              ('short_name', 'QD')]),


1d 是请求的数据数量，

01 c1 06 0b 00 02 0b 00  0b 00 00 24 1d 00 00 00 00 1d 00 01 00
"""

class GetInstrumentQuoteList(BaseParser):

    def setParams(self, market, category, start, count):
        pkg = bytearray.fromhex("01 c1 06 0b 00 02 0b 00 0b 00 00 24")
        pkg.extend(
            struct.pack("<BHHHH", market, 0, start, count, 1)
        )
        self.category = category
        self.send_pkg = pkg

    def parseResponse(self, body_buf):

        pos = 0
        num = struct.unpack('<H', body_buf[pos: pos+2])
        pos += 2

        if num == 0:
            return []

        if self.category != 3:
            return NotImplementedError("暂时不支持期货之外的品类")

        for i in range(num):

        if self.category == 3:

            data_pack_format = "IfffffIIIIfIIIIfIIIIIIIIIfIIII"

            # market, code, bishu, zuojie, jinkai, zuigao, zuidi, maichu, kaicang, _, zongliang,
            # xianliang, zongjine, neipan, waipan, _, chicangliang, mairu, _, _, _, _, mailiang,
            # _, _, _, _, maijia,_, _, _, _
            #     = []



if __name__ == '__main__':
    from pytdx.exhq import TdxExHq_API

    api = TdxExHq_API()
    with api.connect('61.152.107.141', 7727):
        print(api.to_df(api.get_instrument_quote(47, "IF1709")))



