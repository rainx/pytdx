
# 交易相关

## 说明

Pytdx无法直接提供交易功能，目前采用调用网上常见的`trade.dll`的方式实现，trade.dll并不是我开发的，`Please using it at your own risk`

## TdxTradeServer （[https://github.com/rainx/TdxTradeServer](https://github.com/rainx/TdxTradeServer))

为了启动`trade.dll`，我们提供了TdxTradeServer, 将请求封装为 http rest api, 在使用本接口之前，需要用下面的命令

```
&gt; get_tts

```

配置好trade服务（如果要配置多账号版本，建议配置多账号版本的TdxTradeServer)

## 引入交易接口

```
from pytdx.trade import TdxTradeApi

```

## 接口列表

### 初始化客户端

```
api = TdxTradeApi(endpoint="http://10.11.5.175:10092/api", enc_key=b"4f1cf3fec4c84c84", enc_iv=b"0c78abc083b011e7")

```

### api返回数据基本格式

成功

```
{
    "success": true,
    "data": {
        ...
    }
}

```

失败

```
{
    "success": false,
    "error": "...."
}

```

### ping 可用来检测连通性

```
api.ping()

```

### 登入

```
result = api.logon(ip, port, version, yyb_id, account_id, trade_account, jy_passwrod, tx_password)
if result["success"]:
    client_id = result["data"]["client_id"]

```

### 登出

```
api.logoff(client_id):

```

### 查询信息

```
api.query_data(client_id, category)

```

### 查询历史信息

```
api.query_history_data(client_id, category, begin_date, end_date)

```

### 创建订单

```
api.send_order(client_id, category, price_type, gddm, zqdm, price, quantity)

```

### 撤销订单

```
api.cancel_order(client_id, exchange_id, hth)

```

### 获取行情

```
api.get_quote(client_id, code)

```

### 融资融券账户直接还款

```
api.repay(client_id, amount)

```

### 获取所有正在登录的client账号列表

```
api.get_active_clients()

```
