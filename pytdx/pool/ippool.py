#utf-8

import random
import threading
from functools import partial
from pytdx.log import DEBUG, log
import time
from collections import OrderedDict

"""
ips 应该还是一个 (ip ,port) 对的列表，如

[
    (ip1, port1),
    (ip2, port2),
    (ip3, port3),
]

"""

class BaseIPPool(object):

    def __init__(self):
        self.hq_class = None

    def setup(self, hq_class):
        self.hq_class = hq_class

    def teardown(self):
        pass


class RandomIPPool(BaseIPPool):
    """
    获取一个随机的优先级列表
    """

    def __init__(self, ips):
        """
        :param ips: ip should be a list
        """
        super(RandomIPPool, self).__init__()
        self.ips = ips

    def get_ips(self):
        random.shuffle(self.ips)
        return self.ips



class AvailableIPPool(BaseIPPool):
    """
    测试可连接性，并根据连接速度排序
    我们启动一个新的线程，周期性的进行更新
    """

    def __init__(self, ips):
        super(AvailableIPPool, self).__init__()
        self.ips = ips
        self.sorted_ips = None
        self.worker_thread = None
        self.sorted_ips_lock = threading.Lock()
        self.stop_event = threading.Event()
        self.wait_interval = 20 * 60

    def setup(self, hq_class):
        super(AvailableIPPool, self).setup(hq_class)

        self.worker_thread = threading.Thread(target=self.run)
        self.worker_thread.start()


    def get_ips(self):
        if not self.sorted_ips:
            return self.ips
        else:
            return list(self.sorted_ips.items())

    def teardown(self):
        self.stop_event.set()
        self.worker_thread = None

    def run(self):
        log.debug("pool thread start ")
        while not self.stop_event.is_set():
            _available_ips = OrderedDict()
            for ip in self.ips:
                ip_addr, port = ip
                api = self.hq_class(multithread=False, heartbeat=False)
                try:
                    with api.connect(ip_addr, port):
                        start_ts = time.time()
                        api.do_heartbeat()
                        end_ts = time.time()
                        diff_ts = end_ts - start_ts
                        _available_ips[diff_ts] = ip
                        log.debug("time diff is %f for %s" % (diff_ts, _available_ips))
                except Exception as e:
                    log.debug("can not use %s:%d the exception is %s" % (ip_addr, port, str(e)) )
                    continue
            sorted_keys = sorted(_available_ips)
            with self.sorted_ips_lock:
                self.sorted_ips = OrderedDict((key, _available_ips[key]) for key in sorted_keys)
            self.stop_event.wait(self.wait_interval)


if __name__ == "__main__":
    from pytdx.hq import TdxHq_API
    from pytdx.config.hosts import hq_hosts
    import logging
    log.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # add formatter to ch
    ch.setFormatter(formatter)
    log.addHandler(ch)

    ips = [(v[1], v[2]) for v in hq_hosts]
    pool = AvailableIPPool(ips)
    pool.wait_interval = 1
    pool.setup(TdxHq_API)
    log.debug("ready to sleep 100")
    time.sleep(100)
    pool.teardown()


