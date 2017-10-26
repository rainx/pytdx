#coding: utf-8
# see https://github.com/rainx/pytdx/issues/38 IP寻优的简单办法
# by yutianst

import datetime
from pytdx.hq import TdxHq_API


def ping(ip):
    __time1 = datetime.datetime.now()
    api = TdxHq_API()
    try:
        with api.connect(ip, 7709):
            if len(api.get_security_list(0, 1)) > 800:
                return datetime.datetime.now() - __time1
    except:
        return datetime.timedelta(9, 9, 0)


def select_best_ip():
    listx = ['180.153.18.170', '180.153.18.171', '202.108.253.130', '202.108.253.131', '60.191.117.167', '115.238.56.198', '218.75.126.9', '115.238.90.165',
             '124.160.88.183', '60.12.136.250', '218.108.98.244', '218.108.47.69', '14.17.75.71', '180.153.39.51']
    data = [ping(x) for x in listx]
    return listx[data.index(min(data))]

if __name__ == '__main__':
    ip = select_best_ip()
    print(ip)
