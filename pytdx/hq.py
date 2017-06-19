#
# This is a migrate to python verion of https://github.com/280185386/tdxhq/blob/master/TDXHQ/TDXHQ.cpp
# Just for practising
#
import socket
import logging
import struct
import zlib

LOGLEVEL = logging.DEBUG
CONNECT_TIMEOUT = 5.000


DEBUG = True

log = logging.getLogger("PYTDX")
log.setLevel(LOGLEVEL)
ch = logging.StreamHandler()
ch.setLevel(LOGLEVEL)
# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# add formatter to ch
ch.setFormatter(formatter)
log.addHandler(ch)


RECV_HEADER_LEN = 0x10

class TdxHq_API(object):

    def __init__(self):
        ip = None
        current_ip = None
        client = None



    def connect(self, ip, port):
        """

        :param ip:  服务器ip 地址
        :param port:  服务器端口
        :return: 是否连接成功 True/False
        """

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.settimeout(CONNECT_TIMEOUT)
        log.info("connecting to server : %s on port :%d" % (ip, port))
        try:
            self.client.connect((ip, port))
        except socket.timeout as e:
            print(str(e))
            log.warning("connection expired")
            return False
        log.info("connected!")
        return True

    def disconnect(self):
        if self.client:
            log.info("disconnecting")
            self.client.shutdown(socket.SHUT_RDWR)
            self.client.close()
            log.info("disconnected")


    def get_price(self, data, pos):
        pos_byte = 6
        bdata = data[pos]
        intdata = bdata & 0x3f

        if bdata & 0x40:
            sign = True
        else:
            sign = False

        if bdata & 0x80:
            while True:
                pos += 1
                bdata = data[pos]
                intdata += (bdata & 0x7f) << pos_byte
                pos_byte += 7

                if bdata & 0x80:
                    pass
                else:
                    break

        pos += 1

        if sign:
            intdata = -intdata

        return intdata, pos

    def get_volume(self, ivol):
        logpoint = ivol >> (8*3)
        hheax = ivol >> (8 * 3); # [3]
        hleax = (ivol >> (8 * 2)) & 0xff; # [2]
        lheax = (ivol >> 8) & 0xff; # [1]
        lleax = ivol & 0xff; # [0]

        dbl_1 = 1.0
        dbl_2 = 2.0
        dbl_128 = 128.0

        dwEcx = logpoint * 2 - 0x7f;
        dwEdx = logpoint * 2 - 0x86;
        dwEsi = logpoint * 2 - 0x8e;
        dwEax = logpoint * 2 - 0x96;
        if dwEcx < 0:
            tmpEax = - dwEcx
        else:
            tmpEax = dwEcx

        dbl_xmm6 = 0.0
        dbl_xmm6 = pow(2.0, tmpEax)
        if dwEcx < 0:
            dbl_xmm6 = 1.0 / dbl_xmm6

        dbl_xmm4 = 0
        if hleax > 0x80:
            tmpdbl_xmm3 = 0.0
            tmpdbl_xmm1 = 0.0
            dwtmpeax = dwEdx + 1
            tmpdbl_xmm3 = pow(2.0, dwtmpeax)
            dbl_xmm0 = pow(2.0, dwEdx) * 128.0
            dbl_xmm0 += (hleax & 0x7f) * tmpdbl_xmm3
            dbl_xmm4 = dbl_xmm0

        else:
            dbl_xmm0 = 0.0
            if dwEdx >= 0:
                dbl_xmm0 = pow(2.0, dwEdx) * hleax
            else:
                dbl_xmm0 = (1 / pow(2.0, dwEdx)) * hleax
            dbl_xmm4 = dbl_xmm0

        dbl_xmm3 = pow(2.0, dwEsi) * lheax
        dbl_xmm1 = pow(2.0, dwEax) * lleax
        if hleax & 0x80:
            dbl_xmm3 *= 2.0
            dbl_xmm1 *= 2.0

        dbl_ret = dbl_xmm6 + dbl_xmm4 + dbl_xmm3 + dbl_xmm1
        return dbl_ret


    def get_datetime(self, category, buffer, pos):
        year = 0
        month = 0
        day = 0
        hour = 15
        minute = 0
        if category < 4 or category == 7 or category == 8:
            (zipday, tminutes) = struct.unpack("<HH", buffer[pos: pos+4])
            year = (zipday >> 11) + 2004
            month = int((zipday % 2048) / 100)
            day = (zipday % 2048) % 100

            hour = int(tminutes / 60)
            minute = tminutes %  60
        else:
            (zipday,) = struct.unpack("<I", buffer[pos: pos + 4])

            year = int(zipday / 10000);
            month = int((zipday % 10000) / 100)
            day = zipday % 100

        pos += 4

        return year, month, day, hour, minute, pos

    """
    param: category=9, market=0, stockcode=000001, start=0, count=10
    send: 0c01086401011c001c002d0500003030303030310900010000000a0000000000000000000000
    recv: b1cb74000c01086401002d05aa00aa000a006ec73301b28c011e3254a081ad4816d6984d6fc7330154ae0182024ab0a51d4978090c4e70c733015414285e8003bb488b59a64d71c73301140086015ec059274945cb154e74c73301006828724060f648ae0edc4d75c73301000a1e7c40f6da48a37dc24d76c7330100680ad0018052b748ad68a24d77c7330100680072a0f0a448f8b9914d78c733010054285ee0a48b48c294764d7bc733010aa401b8014a001def4874abd44d


    """


    def get_security_bars(self, category, market, code, start, count):
        if type(code) is str:
            code = code.encode("utf-8")

        values = (
            0x10c,
            0x01016408,
            0x1c,
            0x1c,
            0x052d,
            market,
            code,
            category,
            1,
            start,
            count,
            0, 0, 0  # I + I +  H total 10 zero
        )

        pkg = struct.pack("<HIHHHH6sHHHHIIH", *values)

        nsended = self.client.send(pkg)

        log.info("send package:" + str(pkg))
        if nsended != len(pkg):
            log.info("send bytes error")
            return False
        else:
            head_buf = self.client.recv(0x10)
            if DEBUG:
                log.info("recv head_buf:" + str(head_buf)  + " |len is :" + str(len(head_buf)))
            if len(head_buf) == 0x10:
                _, _, _, zipsize, unzipsize = struct.unpack("<IIIHH", head_buf)
                logging.info("zip size is: " + str(zipsize))
                body_buf = bytearray()

                while True:
                    buf = self.client.recv(zipsize)
                    body_buf.extend(buf)
                    if not(buf) or len(buf) == 0 or len(body_buf) == zipsize:
                        break
                if len(buf) == 0:
                    log.info("接收数据体失败服务器断开连接")
                    return False
                if zipsize == unzipsize:
                    log.info("不需要解压")
                else:
                    log.info("需要解压")
                    unziped_data = zlib.decompress(body_buf)
                    body_buf = unziped_data
                    ## 解压
                if DEBUG:
                    log.info("recv body: ")
                    log.info(body_buf)

                pos = 0

                (ret_count, ) = struct.unpack("<H", body_buf[0: 2])
                pos += 2

                klines = []

                pre_diff_base = 0
                for i in range(ret_count):
                    year, month, day, hour, minute, pos = self.get_datetime(category, body_buf, pos)

                    price_open_diff, pos = self.get_price(body_buf, pos)
                    price_close_diff, pos = self.get_price(body_buf, pos)

                    price_high_diff, pos = self.get_price(body_buf, pos)
                    price_low_diff, pos = self.get_price(body_buf, pos)

                    (vol_raw, ) = struct.unpack("<I", body_buf[pos: pos+4])
                    vol = self.get_volume(vol_raw)

                    pos += 4
                    (dbvol_raw, ) = struct.unpack("<I", body_buf[pos: pos+4])
                    dbvol = self.get_volume(dbvol_raw)
                    pos += 4

                    open = self._cal_price1000(price_open_diff, pre_diff_base)

                    price_open_diff = price_open_diff + pre_diff_base

                    close = self._cal_price1000(price_open_diff, price_close_diff)
                    high = self._cal_price1000(price_open_diff, price_high_diff)
                    low = self._cal_price1000(price_open_diff, price_low_diff)

                    pre_diff_base = price_open_diff + price_close_diff

                    #### 为了避免python处理浮点数的时候，浮点数运算不精确问题，这里引入了多余的代码

                    kline = {
                        "open": open,
                        "close": close,
                        "high": high,
                        "low": low,
                        "vol": vol,
                        "amount": dbvol,
                        "year": year,
                        "month": month,
                        "day": day,
                        "hour": hour,
                        "minute": minute,
                        "datetime": "%d-%02d-%02d %02d:%02d" % (year, month, day, hour, minute)
                    }
                    klines.append(kline)
                return klines

            else:
                log.info("head_buf is not 0x10")
                return False




    def get_security_quotes(self, all_stock):
        """

        :param all_stock: 一个包含 (market, code) 元组的列表， 如 [ (0, '000001'), (1, '600001') ]
        :return:
        """

        stock_len = len(all_stock)
        if stock_len <= 0:
            return False

        pkgdatalen = stock_len * 7 + 12

        values = (
            0x10c,
            0x02006320,
            pkgdatalen,
            pkgdatalen,
            0x5053e,
            0,
            0,
            stock_len,
        )


        pkg_header = struct.pack("<HIHHIIHH", *values)
        pkg = bytearray(pkg_header)

        for stock in all_stock:
            market, code = stock
            if type(code) is str:
                code = code.encode("utf-8")
                one_stock_pkg = struct.pack("<B6s", market, code)
                pkg.extend(one_stock_pkg)


        nsended = self.client.send(pkg)

        if DEBUG:
            log.info("sending package:" + str(pkg))

        if nsended != len(pkg):
            log.info("send bytes error")
            return False
        else:
            head_buf = self.client.recv(0x10)
            if DEBUG:
                log.info("recv head_buf:" + str(head_buf)  + " |len is :" + str(len(head_buf)))
            if len(head_buf) == 0x10:
                _, _, _, zipsize, unzipsize = struct.unpack("<IIIHH", head_buf)
                logging.info("zip size is: " + str(zipsize))
                body_buf = bytearray()

                while True:
                    buf = self.client.recv(zipsize)
                    body_buf.extend(buf)
                    if not(buf) or len(buf) == 0 or len(body_buf) == zipsize:
                        break
                if len(buf) == 0:
                    log.info("接收数据体失败服务器断开连接")
                    return False
                if zipsize == unzipsize:
                    log.info("不需要解压")
                else:
                    log.info("需要解压")
                    unziped_data = zlib.decompress(body_buf)
                    body_buf = unziped_data

                    ## 解压
                if DEBUG:
                    log.info("recv body: ")
                    log.info(body_buf)

                pos = 0
                pos += 2 # skip b1 cb
                (num_stock,) = struct.unpack("<H", body_buf[pos: pos+2])
                pos += 2
                stocks = []

                for _ in range(num_stock):
                    # print(body_buf[pos:])
                    # b'\x00000001\x95\n\x87\x0e\x01\x01\x05\x00\xb1\xb9\xd6\r\xc7\x0e\x8d\xd7\x1a\x84\x04S\x9c<M\xb6\xc8\x0e\x97\x8e\x0c\x00\xae\n\x00\x01\xa0\x1e\x9e\xb3\x03A\x02\x84\xf9\x01\xa8|B\x03\x8c\xd6\x01\xb0lC\x04\xb7\xdb\x02\xac\x7fD\x05\xbb\xb0\x01\xbe\xa0\x01y\x08\x01GC\x04\x00\x00\x95\n'
                    (market, code, active1) = struct.unpack("<B6sH", body_buf[pos: pos + 9])
                    pos += 9
                    price, pos = self.get_price(body_buf, pos)
                    last_close_diff, pos = self.get_price(body_buf, pos)
                    open_diff, pos = self.get_price(body_buf, pos)
                    high_diff, pos = self.get_price(body_buf, pos)
                    low_diff, pos = self.get_price(body_buf, pos)
                    # 不确定这里应该是用 get_price 跳过还是直接跳过4个bytes
                    reversed_bytes0 = body_buf[pos: pos+4]
                    pos += 4
                    #reversed_bytes0, pos = self.get_price(body_buf, pos)
                    # 应该是 -price
                    reversed_bytes1, pos = self.get_price(body_buf, pos)
                    assert (reversed_bytes1 == -price)
                    vol, pos = self.get_price(body_buf, pos)
                    cur_vol, pos = self.get_price(body_buf, pos)
                    (amount_raw,) = struct.unpack("<I", body_buf[pos: pos+4])
                    amount = self.get_volume(amount_raw)
                    pos += 4
                    s_vol, pos = self.get_price(body_buf, pos)
                    b_vol, pos = self.get_price(body_buf, pos)
                    reversed_bytes2, pos = self.get_price(body_buf, pos)
                    reversed_bytes3, pos = self.get_price(body_buf, pos)

                    bid1, pos = self.get_price(body_buf, pos)
                    ask1, pos = self.get_price(body_buf, pos)
                    bid_vol1, pos = self.get_price(body_buf, pos)
                    ask_vol1, pos = self.get_price(body_buf, pos)

                    bid2, pos = self.get_price(body_buf, pos)
                    ask2, pos = self.get_price(body_buf, pos)
                    bid_vol2, pos = self.get_price(body_buf, pos)
                    ask_vol2, pos = self.get_price(body_buf, pos)

                    bid3, pos = self.get_price(body_buf, pos)
                    ask3, pos = self.get_price(body_buf, pos)
                    bid_vol3, pos = self.get_price(body_buf, pos)
                    ask_vol3, pos = self.get_price(body_buf, pos)

                    bid4, pos = self.get_price(body_buf, pos)
                    ask4, pos = self.get_price(body_buf, pos)
                    bid_vol4, pos = self.get_price(body_buf, pos)
                    ask_vol4, pos = self.get_price(body_buf, pos)

                    bid5, pos = self.get_price(body_buf, pos)
                    ask5, pos = self.get_price(body_buf, pos)
                    bid_vol5, pos = self.get_price(body_buf, pos)
                    ask_vol5, pos = self.get_price(body_buf, pos)

                    (reversed_bytes4, reversed_bytes5, reversed_bytes6,
                     reversed_bytes7, reversed_bytes8, reversed_bytes9,
                     active2) = struct.unpack("<HbbbbHH", body_buf[pos: pos+10])

                    pos += 10

                    one_stock = {
                        "market" : market,
                        "code" : code,
                        "active1" : active1,
                        "price" : self._cal_price(price, 0),
                        "last_close" : self._cal_price(price, last_close_diff),
                        "open" : self._cal_price(price, open_diff),
                        "high" : self._cal_price(price, high_diff),
                        "low" : self._cal_price(price, low_diff),
                        "reversed_bytes0" : reversed_bytes0,
                        "reversed_bytes1" : reversed_bytes1,
                        "vol" : vol,
                        "cur_vol": cur_vol,
                        "amount": amount,
                        "s_vol" : s_vol,
                        "b_vol" : b_vol,
                        "reversed_bytes2" : reversed_bytes2,
                        "reversed_bytes3" : reversed_bytes3,
                        "bid1" : self._cal_price(price, bid1),
                        "ask1" : self._cal_price(price, ask1),
                        "bid_vol1" : bid_vol1,
                        "ask_vol1" :  ask_vol1,
                        "bid2": self._cal_price(price, bid2),
                        "ask2": self._cal_price(price, ask2),
                        "bid_vol2": bid_vol2,
                        "ask_vol2": ask_vol2,
                        "bid3": self._cal_price(price, bid3),
                        "ask3": self._cal_price(price, ask3),
                        "bid_vol3": bid_vol1,
                        "ask_vol3": ask_vol1,
                        "bid4": self._cal_price(price, bid4),
                        "ask4": self._cal_price(price, ask4),
                        "bid_vol4": bid_vol1,
                        "ask_vol4": ask_vol1,
                        "bid5": self._cal_price(price, bid5),
                        "ask5": self._cal_price(price, ask5),
                        "bid_vol5": bid_vol1,
                        "ask_vol5": ask_vol1,
                        "reversed_bytes4" : reversed_bytes4,
                        "reversed_bytes5" : reversed_bytes5,
                        "reversed_bytes6" : reversed_bytes6,
                        "reversed_bytes7" : reversed_bytes7,
                        "reversed_bytes8" : reversed_bytes8,
                        "reversed_bytes9" : reversed_bytes9,
                        "active2" : active2
                    }
                    stocks.append(one_stock)
                return stocks
            else:
                log.info("head_buf is not 0x10")
                return False

    def _cal_price(self, base_p, diff):
        return (base_p + diff)/100

    def _cal_price1000(self, base_p, diff):
        return (base_p + diff)/1000



if __name__ == '__main__':
    import pprint
    import pandas as pd
    api = TdxHq_API();
    if api.connect('101.227.73.20', 7709):
        #stocks = api.get_security_quotes([(0, "000001"), (1, "600300")])
        #pprint.pprint(stocks)
        #df = pd.DataFrame(data=stocks)
        #print(df)
        data = api.get_security_bars(9,0, '000001', 4, 3)
        pprint.pprint(data)
        api.disconnect()

