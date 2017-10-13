# Pytdx - Python tdx数据接口

[![Build Status](https://travis-ci.org/rainx/pytdx.svg?branch=master)](https://travis-ci.org/rainx/pytdx)

文档
---
用户文档会逐步转移到gitbook上，您可以在

https://rainx.gitbooks.io/pytdx/content/

阅读使用该api接口的详细文档。

概述
---

Pytdx 是一款纯Python语言开发的类似TradeX的行情数据接口的实现。

特点
---
* 纯python实现，无须引入动态连接库```.dll/.so```文件
* 支持```python2.7+```/```3.5+```， 以及全平台```Windows/MacOS/Linux```
* 可以通过设置参数提供```线程安全```接口调用
* 实现```心跳包```机制,可以在长时间没有交互的情况下保持不断线
* (试验）支持多连接构成的连接池机制，和failover处理机制，保证稳定性。
* 可以自定义的自动重连策略

安装
---

```
pip install pytdx
```

接口实现
---
### 标准行情 pytdx.hq
用于读取标准行情信息

### 扩展行情 pytdx.exhq

用于读取扩展行情（外盘，期权，期货等）

### 数据文件读取 pytdx.reader
用于读取行情软件导出的k线数据

### pytdx.pool (试验性质)
用于实现备用连接池以及failover支持的行情接口


命令行
---
我们提供了方便命令行调试和导出数据的命令行工具 `hqget` 以及`hqreader` 具体使用方法请参考这里。

缘起
---

因为之前TradeX的接口是使用Python扩展的方式调用C++代码实现的，功能上有诸多的限制，如只支持32位的Python， 不支持MacOS, Linux等，
无奈我自己使用的电脑是Mac系统, 服务器又是基于Linux的，所以只能自己重新实现一份。

声明
---
此代码用于个人对网络协议的研究和习作，不对外提供服务，任何人使用本代码遇到问题请自行解决，也可以在github提issue给我，但是我不保证能即时处理。
由于我们连接的是既有的行情软件兼容行情服务器，机构请不要使用此代码，对此造成的任何问题本人概不负责。

## 其它

欢迎对量化交易感兴趣的朋友互相交流，可以来我们的智矿社区看看 http://zhikuang.org
