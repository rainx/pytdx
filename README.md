Python通达信数据接口
========

概述
----
使用纯Python类似TradeX的获取通达信行情接口的实现

因为之前TradeX的接口是使用Python扩展的方式调用C++代码实现的，功能上有诸多的限制，如只支持32位的Python， 不支持MacOS, Linux等， 
无奈我自己使用的电脑是Mac系统, 服务器又是基于Linux的，所以只能自己重新实现一份。

更新
---
除了读取行情之外，目前还实现了解析通达信的数据文件的功能，可以查看Reader部分
 
文档
---
用户文档会逐步转移到gitbook上，您可以在

https://rainx.gitbooks.io/pytdx/content/

阅读使用该api接口的详细文档。
 

声明
---
次代码用于个人对网络协议的研究和习作，不对外提供服务，任何人使用本代码遇到问题请自行解决，也可以在github提issue给我，但是我不保证能即时处理。
由于我们连接的是既有的通达信兼容行情服务器，机构请不要使用次代码，对此造成的任何问题本人概不负责。

兼容性
---
目前已经验证在如下的Python版本下成功运行，并在Windows,Mac,Linux各个系统下进行了测试

```bash
Python2.7+
Python3.6+
```

安装
--

```bash
> pip install pytdx

或者

> pip install git+https://github.com/rainx/pytdx
```

命令行
---
我提供了一个命令行工具来实现简单的交互和功能演示，在安装之后，应该可以直接使用 ```hqget``` 命令调用， hqget分为交互模式和单命令模式，
您可以随时使用 hqget --help 获取接口的使用规则。

### 交互模式

直接输入 ```hqget``` 即可进入交互模式，进入之后，先选择要连接的服务器类型，然后选择要执行的功能，选择菜单里面最后一项退出交互模式。

选择服务器
```bash
-->rainx@JingdeMacBook-Pro:~/dev/pytdx [master]$ hqget
连接中....
请选择服务器
--------------------
[1] :招商证券深圳行情 (119.147.212.81:7709)
[2] :华泰证券(南京电信) (221.231.141.60:7709)
[3] :华泰证券(上海电信) (101.227.73.20:7709)
[4] :华泰证券(上海电信二) (101.227.77.254:7709)
[5] :华泰证券(深圳电信) (14.215.128.18:7709)
[6] :华泰证券(武汉电信) (59.173.18.140:7709)
[7] :华泰证券(天津联通) (60.28.23.80:7709)
[8] :华泰证券(沈阳联通) (218.60.29.136:7709)
[9] :华泰证券(南京联通) (122.192.35.44:7709)
[10] :华泰证券(南京联通) (122.192.35.44:7709)
--------------------
请输入序号  [1]:
```
 
 选择功能
 
```bash
连接成功！
--------------------
功能列表：
1 : 获取股票行情
2 : 获取k线
3 : 获取市场股票数量
4 : 获取股票列表
5 : 获取指数k线
6 : 查询分时行情
7 : 查询历史分时行情
8 : 查询分笔成交
9 : 查询历史分笔成交
10 : 查询公司信息目录
11 : 读取公司信息详情
12 : 读取除权除息信息
13 : 读取财务信息
14 : 退出断开连接
--------------------
请输入要使用的功能:
```

```1.9版本更新``` ： 增加了--all参数，可以获取更多服务器列表 

输入参数并获取结果

```bash

参数：市场代码， 股票代码， 如： 0,000001 或 1,600300
请输入参数  [0,000001]:
--------------------
   market    code  active1  price  last_close  open  high   low  \
0       0  000001     2801   9.18        9.25  9.23  9.27  9.16

       reversed_bytes0  reversed_bytes1   ...     ask5  bid_vol5  ask_vol5  \
0  [178, 174, 231, 12]             -918   ...     9.23      4171      6140

   reversed_bytes4  reversed_bytes5  reversed_bytes6  reversed_bytes7  \
0             5689                1               17               82

   reversed_bytes8  reversed_bytes9  active2
0               21            65526     2801

[1 rows x 44 columns]
```

输出结果默认会使用pandas Dataframe格式输出，在内容较多时会省略部分列或行的记录，这个时候可以使用 ```--no-df``` 参数，让其用原始数据格式输出。

如启动时

```bash
> hqget --no-df
```
然后进行之前的操作，结果为：

```python
参数：市场代码， 股票代码， 如： 0,000001 或 1,600300
请输入参数  [0,000001]:
--------------------
[OrderedDict([('market', 0),
              ('code', '000001'),
              ('active1', 2864),
              ('price', 9.19),
              ('last_close', 9.25),
              ('open', 9.23),
              ('high', 9.27),
              ('low', 9.16),
              ('reversed_bytes0', bytearray(b'\xbd\xc9\xec\x0c')),
              ('reversed_bytes1', -919),
              ('vol', 428899),
              ('cur_vol', 30),
              ('amount', 395218880.0),
              ('s_vol', 284703),
              ('b_vol', 144196),
              ('reversed_bytes2', 1),
              ('reversed_bytes3', 698),
              ('bid1', 9.18),
              ('ask1', 9.19),
              ('bid_vol1', 1078),
              ('ask_vol1', 5236),
              ('bid2', 9.17),
              ('ask2', 9.2),
              ('bid_vol2', 8591),
              ('ask_vol2', 3027),
              ('bid3', 9.16),
              ('ask3', 9.21),
              ('bid_vol3', 12638),
              ('ask_vol3', 3557),
              ('bid4', 9.15),
              ('ask4', 9.22),
              ('bid_vol4', 13234),
              ('ask_vol4', 2615),
              ('bid5', 9.14),
              ('ask5', 9.23),
              ('bid_vol5', 5377),
              ('ask_vol5', 6033),
              ('reversed_bytes4', 5768),
              ('reversed_bytes5', 1),
              ('reversed_bytes6', 16),
              ('reversed_bytes7', 83),
              ('reversed_bytes8', 20),
              ('reversed_bytes9', 0),
              ('active2', 2864)])]
```

### 单命令模式

脚本也可以使用命令模式进行， 这个时候，需要通过输入 ```-f/--function``` 参数来选择要执行的命令

如：

```bash
> hqget -f 1 
```

### 保存文件
在但命令模式下，可以通过设定 ```-o/--output``` 参数来选择将命令结果保存到文件中，这个时候根据 ```--df/--no-df``` 参数的结果不同，会保存为不同的格式，
如果没有设置或者设置为 ```--df```, 则通过pandas Dataframe保存为csv格式，如果选择了 ```--no-df``` 则把结果保存为Python Pickle序列化的格式。

### 默认连接服务器
我们可以通过设定选项 ```-s/--server```来指定其默认连接的服务器，格式是 [ip]:[port], 如：

```bash
> hqget -f 1 -s 119.147.212.81:7709
```


行情接口API
---
下面是如何在程序里面调用本接口

首先需要引入

```python
from pytdx.hq import TdxHq_API
```

然后，创建对象

```python
api = TdxHq_API()
```

之后，通常是如下的格式

```python
if api.connect('119.147.212.81', 7709):
    # ... same codes...
    api.disconnect()

```

当然，我们也支持with 语法,可以省略```disconnect()```语句

```python
with api.connect('119.147.212.81', 7709):
    # some codes
```

我们的数据获取届接口一般返回list结构，如果需要转化为pandas Dataframe接口，可以使用 ```api.to_df``` 进行转化
如：
```python
data = api.get_security_bars(9, 0, '000001', 0, 10) #返回普通list
data = api.to_df(api.get_security_bars(9, 0, '000001', 0, 10)) # 返回DataFrame
```

可以使用的api方法有下列的几个。

### api方法列表

#### 参数一般性约定

一般来说，股票代码和文件名称使用字符串类型，其它参数都使用数值类型


#### 1 : 获取股票行情
可以获取**多**只股票的行情信息

需要传入一个列表，每个列表由一个市场代码， 一个股票代码构成的元祖构成
```[ (市场代码1， 股票代码1)，(市场代码2， 股票代码2) ... (市场代码n， 股票代码n) ]```

如：
```python
api.get_security_quotes([(0, '000001'), (1, '600300')])
```

#### 2 : 获取k线

* category-> 
```
K线种类
0 5分钟K线 1 15分钟K线 2 30分钟K线 3 1小时K线 4 日K线
5 周K线
6 月K线
7 1分钟
8 1分钟K线 9 日K线
10 季K线
11 年K线
```
* market -> 市场代码 0:深圳，1:上海
* stockcode -> 证券代码;
* start -> 指定的范围开始位置;
* count -> 用户要请求的 K 线数目，最大值为 800

如： 

```python
api.get_security_bars(9,0, '000001', 4, 3)
```

#### 3 : 获取市场股票数量
0 - 深圳， 1 - 上海
```python
api.get_security_count(0)
```
#### 4 : 获取股票列表
参数：市场代码, 起始位置， 数量  如： 0,0 或 1,100

```python
api.get_security_list(1, 0)
```

#### 5 : 获取指数k线
* category-> 
```
K线种类
0 5分钟K线 1 15分钟K线 2 30分钟K线 3 1小时K线 4 日K线
5 周K线
6 月K线
7 1分钟
8 1分钟K线 9 日K线
10 季K线
11 年K线
```
* market -> 市场代码 0:深圳，1:上海
* stockcode -> 证券代码;
* start -> 指定的范围开始位置;
* count -> 用户要请求的 K 线数目，最大值为 800

如： 

```python
api.get_index_bars(9,1, '000001', 1, 2)
```
#### 6 : 查询分时行情
参数：市场代码， 股票代码， 如： 0,000001 或 1,600300
```python
api.get_minute_time_data(1, '600300')
```
#### 7 : 查询历史分时行情
参数：市场代码， 股票代码，时间 如： 0,000001,20161209 或 1,600300,20161209
```python
api.get_history_minute_time_data(TDXParams.MARKET_SH, '600300', 20161209)
```

注意，在引入 TDXParams 之后， （```from pytdx.params import TDXParams```）
我们可以使用 TDXParams.MARKET_SH , TDXParams.MARKET_SZ 常量来代替 1 和 0 作为参数

#### 8 : 查询分笔成交

参数：市场代码， 股票代码，起始位置， 数量 如： 0,000001,0,10
```python
api.get_transaction_data(TDXParams.MARKET_SZ, '000001', 0, 30)
```

#### 9 : 查询历史分笔成交

参数：市场代码， 股票代码，起始位置，日期 数量 如： 0,000001,0,10,20170209

```python
api.get_history_transaction_data(TDXParams.MARKET_SZ, '000001', 0, 10, 20170209)
```
#### 10 : 查询公司信息目录
参数：市场代码， 股票代码， 如： 0,000001 或 1,600300
```python
api.get_company_info_category(TDXParams.MARKET_SZ, '000001')
```

#### 11 : 读取公司信息详情

参数：市场代码， 股票代码, 文件名, 起始位置， 数量, 如：0,000001,000001.txt,2054363,9221
```python
api.get_company_info_content(0, '000001', '000001.txt', 0, 100)
```

注意这里的 起始位置， 数量 参考上面接口的返回结果。

#### 12 : 读取除权除息信息
参数：市场代码， 股票代码， 如： 0,000001 或 1,600300
```python
api.get_xdxr_info(1, '600300')
```

#### 13 : 读取财务信息
参数：市场代码， 股票代码， 如： 0,000001 或 1,600300
```python
api.get_finance_info(0, '000001')
```

#### 14 : 读取k线信息
参数：市场代码， 开始时间， 结束时间
```python
get_k_data('000001','2017-07-03','2017-07-10')
```
参考 https://github.com/rainx/pytdx/issues/5

### 多线程支持

由于Python的特性，一般情况下，不太建议使用多线程代码，如果需要并发访问，建议使用多进程来实现，如果要使用多线程版本，请在初始化时设置multithread参数为True

```python
api = TdxHq_API(multithread=True)
```

### 心跳包

由于长时间不与服务器交互，服务器将关闭连接，所以我们实现了心跳包的机制，可以通过
```python
api = TdxHq_API(heartbeat=True)
```
设置心跳包，程序会启动一个心跳包发送线程，在空闲状态下隔一段时间发送一个心跳包，注意，打开heartbeat=True选项的同时会自动打开multithread=True

### 调试模式

如果您需要调试本代码，监控传输过程中的数据包传输情况，可以使用调试模式，使用方法是设定环境变量 TDX_DEBUG 为 1 如

```bash
> TDX_DEBUG=1 hqget -f 1 
```

### 行情服务器列表

为了方便连接服务器，我把一些常用的服务器列表整理到到 ```hosts.py``` 文件中. 在程序中可以通过

```python
from pytdx.config.hosts import hq_hosts
```
获取列表, 列表里的数据参考了 https://github.com/rainx/pytdx/issues/3

欢迎补充并发送pr

## Reader接口

### 读取通达信的日K线

通过下面的接口，我们可以解析通达信的日K线文件，该文件可以通过读取通达信的软件本地目录导出的数据获取，也可以从通达信的官网上下载，
如果您安装了通达信的终端，可以在安装目录下找到 ```vipdoc``` 子目录。

比如我的通达信客户端安装在 ```c:\new_tdx``` 下，
 
即

* ```c:\new_tdx\vipdoc\sz\lday\``` 下是深圳的日k线数据
* ```c:\new_tdx\vipdoc\sh\lday\``` 下是上海的日k线数据

该目录下每个股票为一个文件，如 ```sz000001.day``` 为深圳的日k行情，

读取行情的接口非常简单

```python
from pytdx.reader import TdxDailyBarReader, TdxFileNotFoundException
reader = TdxDailyBarReader()
df = reader.get_df("/Users/rainx/tmp/vipdoc/sz/lday/sz000001.day")

df 是pandas 的DateFrame格式， 输出为：

             open   high    low  close        amount     volume
date
1991-12-23  27.70  27.90  27.60  27.80  3.530600e+06     127000
1991-12-24  27.90  29.30  27.00  29.05  3.050250e+06     105000
1991-12-25  29.15  30.00  29.10  29.30  6.648170e+06     226900
1991-12-26  29.30  29.30  28.00  28.00  5.370400e+06     191800
1991-12-27  28.00  28.50  28.00  28.45  5.988725e+06     210500
...           ...    ...    ...    ...           ...        ...
2017-06-22   9.15   9.40   9.14   9.25  1.325211e+09  142695815
2017-06-23   9.23   9.27   9.16   9.25  5.383036e+08   58400441
2017-06-26   9.26   9.40   9.26   9.30  6.637629e+08   71076995

[6031 rows x 6 columns]

# 可以通过pandas将它保存为csv 等文件, 如:

df.to_csv("/tmp/000001.csv")

```

### 读取通达信的分钟K线（目前支持1，5分钟k线）
```
from pytdx.reader import TdxMinBarReader, TdxFileNotFoundException
reader = TdxMinBarReader()
df = reader.get_df("/Users/rainx/Downloads/sh000001.5")

In [2]: df
Out[2]:
                        open     high      low    close        amount  \
date
2015-07-09 09:35:00  3432.45  3454.14  3374.32  3423.61  6.189348e+10
2015-07-09 09:40:00  3420.56  3424.16  3395.07  3396.33  2.341652e+10

                        volume
date
2015-07-09 09:35:00  618934736
2015-07-09 09:40:00  234165181
```

## 其它

欢迎对量化交易感兴趣的朋友互相交流，可以来我们的智矿社区看看 http://zhikuang.org
