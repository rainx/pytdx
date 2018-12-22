
## 命令行

我提供了一个命令行工具来实现简单的交互和功能演示，在安装之后，应该可以直接使用 `hqget` 命令调用， hqget分为交互模式和单命令模式，
您可以随时使用 hqget --help 获取接口的使用规则。

### 交互模式

直接输入 `hqget` 即可进入交互模式，进入之后，先选择要连接的服务器类型，然后选择要执行的功能，选择菜单里面最后一项退出交互模式。

选择服务器

```
--&gt;rainx@JingdeMacBook-Pro:~/dev/pytdx [master]$ hqget
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

```
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

`1.9版本更新` ： 增加了--all参数，可以获取更多服务器列表

输入参数并获取结果

```

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

输出结果默认会使用pandas Dataframe格式输出，在内容较多时会省略部分列或行的记录，这个时候可以使用 `--no-df` 参数，让其用原始数据格式输出。

如启动时

```
&gt; hqget --no-df

```

然后进行之前的操作，结果为：

```
参数：市场代码， 股票代码， 如： 0,000001 或 1,600300
请输入参数  [0,000001]:
--------------------
[OrderedDict([(&amp;apos;market&amp;apos;, 0),
              (&amp;apos;code&amp;apos;, &amp;apos;000001&amp;apos;),
              (&amp;apos;active1&amp;apos;, 2864),
              (&amp;apos;price&amp;apos;, 9.19),
              (&amp;apos;last_close&amp;apos;, 9.25),
              (&amp;apos;open&amp;apos;, 9.23),
              (&amp;apos;high&amp;apos;, 9.27),
              (&amp;apos;low&amp;apos;, 9.16),
              (&amp;apos;reversed_bytes0&amp;apos;, bytearray(b&amp;apos;\xbd\xc9\xec\x0c&amp;apos;)),
              (&amp;apos;reversed_bytes1&amp;apos;, -919),
              (&amp;apos;vol&amp;apos;, 428899),
              (&amp;apos;cur_vol&amp;apos;, 30),
              (&amp;apos;amount&amp;apos;, 395218880.0),
              (&amp;apos;s_vol&amp;apos;, 284703),
              (&amp;apos;b_vol&amp;apos;, 144196),
              (&amp;apos;reversed_bytes2&amp;apos;, 1),
              (&amp;apos;reversed_bytes3&amp;apos;, 698),
              (&amp;apos;bid1&amp;apos;, 9.18),
              (&amp;apos;ask1&amp;apos;, 9.19),
              (&amp;apos;bid_vol1&amp;apos;, 1078),
              (&amp;apos;ask_vol1&amp;apos;, 5236),
              (&amp;apos;bid2&amp;apos;, 9.17),
              (&amp;apos;ask2&amp;apos;, 9.2),
              (&amp;apos;bid_vol2&amp;apos;, 8591),
              (&amp;apos;ask_vol2&amp;apos;, 3027),
              (&amp;apos;bid3&amp;apos;, 9.16),
              (&amp;apos;ask3&amp;apos;, 9.21),
              (&amp;apos;bid_vol3&amp;apos;, 12638),
              (&amp;apos;ask_vol3&amp;apos;, 3557),
              (&amp;apos;bid4&amp;apos;, 9.15),
              (&amp;apos;ask4&amp;apos;, 9.22),
              (&amp;apos;bid_vol4&amp;apos;, 13234),
              (&amp;apos;ask_vol4&amp;apos;, 2615),
              (&amp;apos;bid5&amp;apos;, 9.14),
              (&amp;apos;ask5&amp;apos;, 9.23),
              (&amp;apos;bid_vol5&amp;apos;, 5377),
              (&amp;apos;ask_vol5&amp;apos;, 6033),
              (&amp;apos;reversed_bytes4&amp;apos;, 5768),
              (&amp;apos;reversed_bytes5&amp;apos;, 1),
              (&amp;apos;reversed_bytes6&amp;apos;, 16),
              (&amp;apos;reversed_bytes7&amp;apos;, 83),
              (&amp;apos;reversed_bytes8&amp;apos;, 20),
              (&amp;apos;reversed_bytes9&amp;apos;, 0),
              (&amp;apos;active2&amp;apos;, 2864)])]

```

### 单命令模式

脚本也可以使用命令模式进行， 这个时候，需要通过输入 `-f/--function` 参数来选择要执行的命令

如：

```
&gt; hqget -f 1

```

### 保存文件

在但命令模式下，可以通过设定 `-o/--output` 参数来选择将命令结果保存到文件中，这个时候根据 `--df/--no-df` 参数的结果不同，会保存为不同的格式，
如果没有设置或者设置为 `--df`, 则通过pandas Dataframe保存为csv格式，如果选择了 `--no-df` 则把结果保存为Python Pickle序列化的格式。

如：

```
hqget -o all.csv -s 119.147.212.81:7709 -f 4

```

察看`all.csv`

<img alt="all.csv" src="assets/hqget-097b5.png"/>

### 默认连接服务器

我们可以通过设定选项 `-s/--server`来指定其默认连接的服务器，格式是 [ip]:[port], 如：

```
&gt; hqget -f 1 -s 119.147.212.81:7709

```
