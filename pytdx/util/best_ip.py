#coding: utf-8
# see https://github.com/rainx/pytdx/issues/38 IP寻优的简单办法
# by yutianst

import time
from concurrent import futures
from pytdx.hq import TdxHq_API
from pytdx.config.hosts import hq_hosts

def ping(ip, port=7709, multithread=False):
    api = TdxHq_API(multithread=multithread)
    success = False
    starttime = time.time()
    try:
        with api.connect(ip, port, time_out=1):
            x = api.get_security_bars(7, 0, '000001', 800, 100)
            if x:
                success = True
    except Exception as e:
        success = False
    endtime = time.time()
    return (success, endtime - starttime, ip, port)


def select_best_ip(return_only_one=True):
    def ping2(host):
        return ping(host[0], host[1], host[2])
        
    hosts = [(host[1], host[2], True) for host in hq_hosts]
    with futures.ThreadPoolExecutor() as executor:
        res = executor.map(ping2, hosts, timeout=2)
    x = [i[2:] for i in res if i[0] == True]
    x.sort(key=lambda item: item[1])
    return x[0] if return_only_one else x


if __name__ == '__main__':
    ip = select_best_ip()
    print(ip)
