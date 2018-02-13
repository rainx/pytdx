# coding: utf-8

import tempfile
import six
import math

if six.PY2:
    from urllib2 import urlopen
else:
    from urllib.request import urlopen



def demo_reporthook(downloaded, total_size):
    print("Downloaded {}, Total is {}".format(downloaded, total_size))

class BaseCralwer:

    def __construct(self):
        pass

    def fetch_and_parse(self, reporthook = None, path_to_download=None, proxies=None, chunksize=1024 * 50, *args, **kwargs):
        """
        function to get data ,
        :param reporthook 使用urllib.request 的report_hook 来汇报下载进度 \
                    参考 https://docs.python.org/3/library/urllib.request.html#module-urllib.request
        :param path_to_download 数据文件下载的地址，如果没有提供，则下载到临时文件中，并在解析之后删除
        :param proxies urllib格式的代理服务器设置
        :return: 解析之后的数据结果
        """
        if path_to_download is None:
            download_file = tempfile.NamedTemporaryFile(delete=True)
        else:
            download_file = open(path_to_download, 'wb')

        url = self.get_url(*args, **kwargs)
        req = urlopen(url)

        if six.PY2:
            reqinfo = req.info()
        else:
            reqinfo = req

        if reqinfo.getheader('Content-Length') is not None:
            total_size = int(reqinfo.getheader('Content-Length').strip())
            downloaded = 0

            while True:
                chunk = req.read(chunksize)
                downloaded += len(chunk)
                if reporthook is not None:
                    reporthook(downloaded,total_size)
                if not chunk:
                    break
                download_file.write(chunk)
        else:
            content = req.read()
            download_file.write(content)

        download_file.seek(0)

        return self.parse(download_file, *args, **kwargs)

        download_file.close()


    def get_url(self, *args, **kwargs):
        raise NotImplementedError("will impl in subclass")

    def parse(self, download_file, *args, **kwargs):
        raise NotImplementedError("will impl in subclass")