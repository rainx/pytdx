# coding: utf-8

from struct import calcsize, unpack
from pytdx.crawler.base_crawler import BaseCralwer
import shutil
import tempfile
import random
import os

class HistoryFinancialListCrawler(BaseCralwer):

    def get_url(self, *args, **kwargs):
        return "http://down.tdx.com.cn:8001/fin/gpcw.txt"

    def parse(self, download_file, *args, **kwargs):
        content = download_file.read()
        content = content.decode("utf-8")

        def list_to_dict(l):
            return {
                'filename': l[0],
                'hash': l[1],
                'filesize': int(l[2])
            }
        result = [list_to_dict(l) for l in [line.strip().split(",") for line in content.strip().split('\n')]]
        return result


class HistoryFinancialCrawler(BaseCralwer):

    def get_url(self, *args, **kwargs):
        if 'filename' in kwargs:
            filename = kwargs['filename']
        else:
            raise Exception("Param filename is not set")

        return "http://down.tdx.com.cn:8001/fin/{}".format(filename)

    def parse(self, download_file, *args, **kwargs):

        tmpdir_root = tempfile.gettempdir()
        subdir_name = "pytdx_" + str(random.randint(0, 1000000))
        tmpdir = os.path.join(tmpdir_root, subdir_name)
        shutil.rmtree(tmpdir, ignore_errors=True)
        os.makedirs(tmpdir, exist_ok=True)
        shutil.unpack_archive(download_file.name, extract_dir=tmpdir)
        # only one file endswith .dat should be in zip archives
        datfile = None
        for _file in os.listdir(tmpdir):
            if _file.endswith(".dat"):
                datfile = open(os.path.join(tmpdir, _file), "rb")

        if datfile is None:
            raise Exception("no dat file found in zip archive")

        header_size = calcsize("<3h1H3L")
        stock_item_size = calcsize("<6s1c1L")
        data_header = datfile.read(header_size)
        stock_header = unpack("<3h1H3L", data_header)
        max_count = stock_header[3]

        for stock_idx in range(0, max_count):
            datfile.seek(header_size + stock_idx * calcsize("<6s1c1L"))
            si = datfile.read(stock_item_size)
            stock_item = unpack("<6s1c1L", si)
            code = stock_item[0].decode("utf-8")
            foa = stock_item[2]
            print(code, foa)
            datfile.seek(foa)
            info_data = datfile.read(calcsize('<264f'))
            data_size = len(info_data)
            cw_info = unpack('<264f', info_data)
            print("%s, %s" % (code, str(cw_info)))

        datfile.close()

        shutil.rmtree(tmpdir, ignore_errors=True)




if __name__ == '__main__':
    import pandas as pd
    from pytdx.crawler.base_crawler import demo_reporthook
    crawler = HistoryFinancialListCrawler()
    #
    # list_data = crawler.fetch_and_parse(reporthook=demo_reporthook)
    # print(pd.DataFrame(data=list_data))

    # 读取其中一个
    #
    # filename = list_data[1]['filename']
    #
    datacrawler = HistoryFinancialCrawler()
    # result = datacrawler.fetch_and_parse(reporthook=demo_reporthook, filename=filename, path_to_download="/tmp/tmpfile.zip")
    with open(r"/tmp/tmpfile.zip", "rb") as fp:
        result = datacrawler.parse(download_file=fp)
        print(result)