1.24
------
* 增加 TdxExHqDailyBarReader ，用于读取扩展行情（如期货，现货，期权等）的盘后日线数据 https://github.com/rainx/pytdx/issues/25

1.23
------
* 增加历史分时行情，分时成交，历史分时成交 https://github.com/rainx/pytdx/pull/24 wopalm

1.22
------
* 解决扩展行情，无法指定数据长度的问题 https://github.com/rainx/pytdx/issues/22 wopalm

1.21
------
* Reader 支持 lc1, lc5 文件格式

1.20
------
* 修复了exhq get_instrument_info(10000, 98)取不到数据, change to name = name_raw.decode("gbk", 'ignore')

1.19
------
* 合并了hqpool分支，增加行情备选连接池支持

1.18
------
* 增加了扩展行情的 查询代码列表 `get_instrument_info`

1.17
------
* 修正了get_instrument_bars接口的ohlc位置对应错误的bug
* 修改了对应的列名 vol, amount -> position, trade

1.16
------
* 增加了扩展行情里面的获取k线接口 eg. api.get_instrument_bars(TDXParams.KLINE_TYPE_DAILY, 8, "10000843")

1.15
------
* 在 get_security_list 接口中增加了 小数点位数 (decimal_point) 列 https://github.com/rainx/pytdx/issues/16

1.14
------
* 增加判断，只在heartbeat=True的时候启动heartbeat线程

1.13
------
* 增加心跳包heartbeat参数，自动创建心跳包线程
* 将HqAPI和 ExHqAPI部分逻辑放到BaseSocketClient里

1.12
------
* pr #13 简化用户输入 https://github.com/rainx/pytdx/pull/13

1.11
------
* 追加exhq get_minute_time_data 接口

1.10
------
* 更新了reader中读取通达信1，5分钟k线的数据文件的方法， TdxMinBarReader
* try hqreader -d min ~/Downloads/sh000001.5
* 写了一半的exhq读取，请忽略，当初应该搞个单独的分支的，懒了...

1.9
------
* 更新了主机列表, 参考 issue: https://github.com/rainx/pytdx/issues/3
* 增加了部分常量定义 https://github.com/rainx/pytdx/issues/7
* hqget 增加了 --all 参数，以支持获取全部股票列表

1.8
------
* 修复关于除权除息信息错误的bug, 后续还有待进一步完善  issue ： https://github.com/rainx/pytdx/issues/8

1.7
------
* 支持Reader类读取通达信导出的数据文件 参见 https://github.com/rainx/pytdx/issues/5 感谢 @yutiansut

1.6
------
* 调整GetSecurityQuotesCmd，修复了后几个字节解析的时候的错误，使其不会再解析某些股票的时候pos计算错误，导致后续的股票无法解析

1.5
------
* 修复windows下python2中文显示和命令输入问题

1.4
------
* 修复hqget在python2下获取公司信息详情的时候的错误

1.3
------
* 去掉了一个错误的 assert : assert (reversed_bytes1 == -price)

1.2
------
* 修复python2.7下整除的bug ,类似， 感谢dHydra数据群的 流水
    流水  11:07:46
    @徐景-RainX 2.7中这个除法是有问题的
    流水  11:08:19
        def _cal_price1000(self, base_p, diff):
            return (base_p + diff)/1000
        to  return float(base_p + diff)/1000
* 将返回财务数据里的代码转化为字符串类型(bytes -> str)
* 修复了python2 在 读取 byte[pos] 的时候换个python3 行为不同的bug

1.1
------
* 增加多线程支持
* 对disconnect增加了异常捕获

1.0
------
* 初始版本
