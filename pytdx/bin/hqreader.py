#coding=utf-8
from __future__ import unicode_literals, division
import click
import sys
import os
if __name__ == '__main__':
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))

from pytdx.reader import TdxDailyBarReader, TdxFileNotFoundException, TdxNotAssignVipdocPathException
from pytdx.reader import TdxMinBarReader
from pytdx.reader import TdxLCMinBarReader

@click.command()
@click.argument("input", type=click.Path(exists=True))
@click.option("-o", '--output', help="")
@click.option("-d", "--datatype", default="daily", help="数据文件格式， daily 代表日K线, min 代表5分钟或者1分钟线, lc 代表lc1, lc5格式的分钟线")
def main(input, output, datatype):
    """
    通达信数据文件读取
    """

    if datatype == 'daily':
        reader = TdxDailyBarReader()
    elif datatype == 'lc':
        reader = TdxLCMinBarReader()
    else:
        reader = TdxMinBarReader()

    try:
        df = reader.get_df(input)
        if (output):
            click.echo("写入到文件 : " + output)
            df.to_csv(output)
        else:
            print(df)
    except Exception as e:
        print(str(e))

if __name__ == '__main__':
    main()