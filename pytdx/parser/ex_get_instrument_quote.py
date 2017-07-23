# coding=utf-8

from pytdx.parser.base import BaseParser
from pytdx.helper import get_datetime, get_volume, get_price
from collections import OrderedDict
import struct

# bytearray(b'TDX_DS\x00\x00\x00\x00\x00\x1f\xdc\x00\x00\x01\x00\x00\x00=\x9c\x00\x00t\x00\x00\x00\x00\x00\x00\x00')
class GetInstrumentCount(BaseParser):

    def setup(self):
        pkg = bytearray.fromhex("")

        self.send_pkg = pkg