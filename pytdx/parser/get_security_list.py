from pytdx.parser.base import BaseParser
from pytdx.helper import get_datetime, get_volume, get_price
from collections import OrderedDict
import struct


class GetSecurityList(BaseParser):

    def setup(self):
        self.client.send(bytes.fromhex(u'd0c9ccd6a4c8af0000008fc22540130000d500c9ccbdf0d7ea00000002'))
        header = self.client.recv(0x10)
        print(header)
        size = int.from_bytes(header[-4: -2], 'little')
        body = self.client.recv(size)
        print(body)


    def setParams(self, market, start):
        pkg = bytearray.fromhex(u'0c 01 18 64 01 01 06 00 06 00 50 04')
        pkg_param = struct.pack("<HH", market, start)
        pkg.extend(pkg_param)
        self.send_pkg = pkg

    def parseResponse(self, body_buf):

        return body_buf