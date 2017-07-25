#coding=utf-8
from __future__ import unicode_literals, division

import pandas as pd
import os

from pytdx.reader.base_reader import TdxFileNotFoundException, TdxNotAssignVipdocPathException
from pytdx.reader.base_reader import BaseReader
from collections import OrderedDict
import struct
import pprint


class TicReader(BaseReader):

    def get_df(self, file):

        if not(os.path.isfile(file)):
            raise TdxFileNotFoundException("指定位置 %s 没有找到tic文件" % file)
        with open(file, 'rb') as f:
            content = f.read()


        (num_stock, ) = struct.unpack("<H", content[:2])
        pos = 2
        arr = []
        for i in range(num_stock):
            header_fmt = "<B6s1sIIf"
            header_len = struct.calcsize(header_fmt)
            market, code, _, date, size, open_price = struct.unpack(header_fmt,
                                                                    content[pos: pos + header_len])
            pos += header_len
            data = content[pos:pos + size]

            (tic_date, tic_num) = struct.unpack("<IH", data[:6])
            pos += size
            arr.append({
                'market': market,
                'code': code,
                'date': date,
                'size': size,
                'open_price': open_price,

                # 后续结构方便分析使用，后续应该会有调整

                'data': data,
                'data_extracted': {
                    'tic_date': tic_date,
                    'tic_num': tic_num
                },
                'datalen' : len(data),
            })

        # 先返回普通数组，等解析结构完成之后再改变格式
        return arr

if __name__ == '__main__':
    reader = TicReader()

    data = reader.get_df("/Users/rainx/Downloads/20170721.tic")
    thin_data = []
    for row in data:
        new_row = row
        new_row['data'] = row['data'][:100]
        thin_data.append(new_row)

    pprint.pprint(thin_data)
