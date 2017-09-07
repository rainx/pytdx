#coding: utf-8
import struct
from pytdx.reader.base_reader import BaseReader
from collections import OrderedDict
import pandas as pd

"""
参考这个 http://blog.csdn.net/Metal1/article/details/44352639

"""

BlockReader_TYPE_FLAT = 0
BlockReader_TYPE_GROUP = 1

class BlockReader(BaseReader):

    def get_df(self, fname, type=BlockReader_TYPE_FLAT):

        result = []

        with open(fname, "rb") as f:
            data = f.read()

            pos = 384
            (num, ) = struct.unpack("<H", data[pos: pos+2])
            pos += 2
            for i in range(num):
                blockname_raw = data[pos: pos+9]
                pos += 9
                blockname = blockname_raw.decode("gbk", 'ignore').rstrip("\x00")
                stock_count, block_type = struct.unpack("<HH", data[pos: pos+4])
                pos += 4
                block_stock_begin = pos
                codes=[]
                for code_index in range(stock_count):
                    one_code = data[pos: pos+7].decode("utf-8", 'ignore').rstrip("\x00")
                    pos += 7

                    if type == BlockReader_TYPE_FLAT:
                        result.append(
                            OrderedDict([
                                ("blockname", blockname),
                                ("block_type", block_type),
                                ("code_index", code_index),
                                ("code", one_code),
                            ])
                        )
                    elif type == BlockReader_TYPE_GROUP:
                        codes.append(one_code)

                if type == BlockReader_TYPE_GROUP:
                    result.append(
                        OrderedDict([
                            ("blockname", blockname),
                            ("block_type", block_type),
                            ("stock_count", stock_count),
                            ("code_list", ",".join(codes))
                        ])
                    )

                pos = block_stock_begin + 2800


        return pd.DataFrame(result)


if __name__ == '__main__':
    df = BlockReader().get_df("/Users/rainx/tmp/block_zs.dat")
    print(df)
    df2 = BlockReader().get_df("/Users/rainx/tmp/block_zs.dat", BlockReader_TYPE_GROUP)
    print(df2)