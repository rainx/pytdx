
# 行情连接池 API （实验阶段）

连接池API只针对特定的场景下使用，它还在非常早期的开发阶段

# 描述

它即可以在普通行情api上使用，也可以在扩展行情api中使用，它的基础的逻辑为： 我们需要提供一组ip，他们被划分为3类角色

- 一个正在进行通讯的主连接 我们命名它为M
- 一个热备选连接，它通过心跳包和备选服务器连接, 它为 H
- 一组备选连接池，它们周期性的重拍顺序（可能是根据连接服务器的速度），始终准备替换上面两个连接。 我们命名它们为P

当主连接P的接口调用出现问题时，我们将：

- 热备选连接H 转化为主连接M，重发主连接的请求
- 从连接池P中选出最快的一个连接，重新成为热备选连接H, 并通过心跳包维持服务器的链接
- 连接M回到备选连接池P中。

如此，保证我们的API请求的可靠性

# 例子：

```
from pytdx.hq import TdxHq_API
from pytdx.pool.hqpool import TdxHqPool_API
from pytdx.pool.ippool import AvailableIPPool
from pytdx.config.hosts import hq_hosts
import random
import logging
import pprint

ips = [(v[1], v[2]) for v in hq_hosts]
# 获取5个随机ip作为ip池
random.shuffle(ips)
ips5 = ips[:5]

## IP 池对象
ippool = AvailableIPPool(TdxHq_API, ips5)

## 选出M, H
primary_ip, hot_backup_ip = ippool.sync_get_top_n(2)

print("make pool api")
## 生成hqpool对象，第一个参数为TdxHq_API后者 TdxExHq_API里的一个，第二个参数为ip池对象。
api = TdxHqPool_API(TdxHq_API, ippool)

## connect 函数的参数为M, H 两组 (ip, port) 元组
with api.connect(primary_ip, hot_backup_ip):
    ## 这里的借口和对应TdxHq_API 或者 TdxExHq_API里的一样，我们通过反射调用正确的接口
    ret = api.get_xdxr_info(0, &amp;apos;000001&amp;apos;)
    print("send api call done")
    pprint.pprint(ret)

```
