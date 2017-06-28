#coding=utf-8
from __future__ import unicode_literals, division

import pandas as pd
import os

import struct
"""
读取通达信数据
"""


class TdxFileNotFoundException(Exception):
    pass

class TdxNotAssignVipdocPathException(Exception):
    pass

class TdxDailyBarReader:

    def __init__(self, vipdoc_path=None):
        self.vipdoc_path = vipdoc_path

    def get_kline_by_code(self, code, exchange):
        if self.vipdoc_path == None:
            raise TdxNotAssignVipdocPathException(r"Please provide a vipdoc path , such as c:\\newtdx\\vipdoc")

        fname = os.path.join(self.vipdoc_path, exchange)
        fname = os.path.join(fname, 'lday')
        fname = os.path.join(fname, '%s%s.day' % (exchange, code))
        return self.parse_data_by_file(fname)

    def parse_data_by_file(self, fname):

        if not os.path.isfile(fname):
            raise TdxFileNotFoundException('no tdx kline data, pleaes check path %s', fname)

        with open(fname, 'rb') as f:
            content = f.read()
            return self.unpack_records('<IIIIIfII', content)
        return []

    def unpack_records(self, format, data):
        record_struct = struct.Struct(format)
        return (record_struct.unpack_from(data, offset)
                for offset in range(0, len(data), record_struct.size))

    def get_df(self, code_or_file, exchange=None):

        if exchange == None:
            # 只传入了一个参数
            data = [self._df_convert(row) for row in self.parse_data_by_file(code_or_file)]
        else:
            data = [self._df_convert(row) for row in self.get_kline_by_code(code_or_file, exchange)]

        df =  pd.DataFrame(data=data, columns=('date', 'open', 'high', 'low', 'close', 'amount', 'volume'))
        df.index = pd.to_datetime(df.date)
        return df[['open', 'high', 'low', 'close', 'amount', 'volume']]

    def _df_convert(self, row):
        t_date = str(row[0])
        datestr = t_date[:4] + "-" + t_date[4:6] + "-" + t_date[6:]

        new_row = (
            datestr,
            row[1] * 0.01, # * 0.01 * 1000 , zipline need 1000 times to original price
            row[2] * 0.01,
            row[3] * 0.01,
            row[4] * 0.01,
            row[5],
            row[6]
        )

        return new_row


if __name__ == '__main__':
    tdx_reader = TdxDailyBarReader('/Users/rainx/tmp/vipdoc/')
    try:
        #for row in tdx_reader.parse_data_by_file('/Volumes/more/data/vipdoc/sh/lday/sh600000.day'):
        #    print(row)
        for row in tdx_reader.get_kline_by_code('000001', 'sz'):
            print(row)
        print(tdx_reader.get_df('000001', 'sz'))
    except TdxFileNotFoundException as e:
        pass

