# cli操作文档

## 基本操作

**注意：命令行中除了钱包文件可以直接填写文件名，参数文件都必须指定为文件的绝对路径**

### 生成版本信息

- 命令

```shell
genVersion
```

- 无参数

打印信息如下：

>生成版本信息文件成功:
>version: 0.1.0
>revision: 9eed8e479af092666414be8f1c1f11f9294422c5
>timestamp: 2020-12-10 10:17:23

执行完成之后在当前目录下生成保存版本信息的文件version，文件内容如上，包括：版本号，最后一次提交的commit id和当前时间。



### 显示版本号信息

- 命令

```shell
platoncli -v
```

- 参数说明

> -v或--version


打印信息如下：

>version: 0.1.0
>revision: 9eed8e479af092666414be8f1c1f11f9294422c5
>timestamp: 2020-12-10 10:17:23



### 显示帮助命令

- 命令

```shell
platoncli -h
```

- 参数说明

> -h或--help

**打印信息如下：**

>Usage: platoncli [Submodule/Command] [COMMAND] [ARGS]...
>
>​	platoncli 工具
>
>​	--help -h          帮助
>​	--version -v     版本号
>
>Submodules:
>    account           钱包管理模块
>    delegate          委托模块
>    government    治理模块
>    hedge              锁仓模块
>    node               节点管理模块
>    query              查询模块
>    staking           质押模块
>    tx                    交易管理模块
>
>Commands:
>    init           Initialize the PlatON CLI tool.



### 初始化cli

- 命令

```shell
platoncli init -h [lat/lax/atp/atx]
```

- 参数说明：

> -h:  地址格式类型，包括：lat/lax/atp/atx，默认lat，分别对应初始的chainid为：100/101/201018/201030；
>
> --private_chain/--no-private_chain：是否是搭建私链，默认为否；
>
> --withnode/-w:是否初始化节点，默认不初始化
>
> --config/-c：指定创世区块的文件（如果不指定，则远端下载）
>
> 如果是连接节点，生成的节点配置文件：node_config.json，格式如下：
>
> ```json
> {"rpcAddress": "http://127.0.0.1:6789:", "hrp": "lat", "chainId": 100}
> ```



## 节点模块

注意：

**在windows系统下执行二进制文件，需要在本地配置bls库的环境变量，路径为：`bls_win/lib`**。



### 初始化节点

- 命令

```shell
platoncli node init -h [lat/lax/atp/atx]
```

- 参数说明

> -h:  地址格式类型，包括：lat/lax/atp/atx，默认lat；
>
> --private_chain/--no-private_chain：是否是搭建私链，默认为否；
>
> --config/-c：指定创世区块的文件（如果不指定，则远端下载）
>
> 如果是连接节点，生成的节点配置文件：node_config.json，格式如下：
>
> ```json
> {"rpcAddress": "http://127.0.0.1:6789:", "hrp": "lat", "chainId": 100}
> ```



### 启动/重启节点

- 命令

```shell
platoncli node start
```

- 参数说明

  无



### 停止节点

- 命令

```shell
platoncli node stop 
```

- 参数说明

  无



### 节点升级

- 命令

```shell
platoncli node upgrade -p $bin_path
```

- 参数说明


> -p/--path：二进制的路径



### 节点回滚

- 命令

```shell
platoncli node rollback -p $data_path
```

- 参数说明

> -p/--path：节点数据所在路径



### 生成nodekey

- 命令

```shell
platoncli node generateNodeKey -p $data_path
```

- 参数说明

> -p/--path：生成nodeKey的到指定目录



### 生成blskey

- 命令

```shell
platoncli node generateBlsKey -p $data_path
```

- 参数说明

> -p/--path：生成blsKey的到指定目录



### 节点升级检测

- 命令

```shell
platoncli node check
```

- 无参数



### 查询当前工作目录下的节点信息

- 命令

```shell
platoncli node info
```

- 无参数



### 导出区块

- 命令

```shell
platoncli node blockexport -p $data_path
```

- 参数说明

> -p/--path：指定区块数据导出路径



### 导入区块

- 命令

```shell
platoncli node blockinput  -p $data_path
```

- 参数说明

> -p/--path：指定数据导入路径，文件为zip包格式；



### 数据迁移

- 命令

```shell
platoncli node move -o $original_path -t $tar_path -m key/data/all
```

- 参数说明

> -o/--original：原数据目录，只需要platon工作目录即可；
>
> -t/--target：迁移目标数据目录，只需要platon工作目录即可；
>
> -m/--movetype：迁移类型，包括：
>
> 	- key ：迁移nodekey和blskey；
> 	- data：迁移区块数据；
> 	- all ：迁移key和data；



## 钱包模块

### 创建钱包

- 命令

```shell
platoncli  account  new -n testWallet.json -h atx
platoncli  account  new  -b 3 -h atx
```

- 参数说明

>-n/--name:钱包名字，如wallet.json
>
>-h/--hrp:网络类型
>
>-b/--batch:批量生成钱包

### 删除钱包

- 命令

~~~
platoncli account  delete -d wallet.json
~~~

- 参数说明

> -d/--address:钱包名字或者钱包地址

### 修改密码

- 命令

~~~
platoncli account changePassword -d wallet.json
~~~

- 参数说明

> -d/--address:钱包名字或者钱包地址

### 查看钱包余额

- 命令

~~~
platoncli account blance -d wallet_address -c node_config.json
~~~

- 参数说明

>-d/--address:钱包地址
>
>-c/--config:节点配置文件（非必填）

### 离线签名

- 命令

~~~
platoncli account sign -d xxxx.csv -a wallet.json
~~~

- 参数说明

>-d/--data:待签名的数据
>
>-a/--address:钱包名字或者钱包地址

### 钱包恢复

- 命令

~~~
platoncli account recovery -t private
~~~

- 参数说明

> -t/types:类型mnemonic or private，目前只支持priveKey进行恢复

## 链基本信息

### 查询块高

- 命令

~~~
platoncli query  blockNumber -c node_config.json
~~~

- 参数说明

> -c/--config:节点配置文件（非必填）

### 根据块高查询区块信息

- 命令

~~~
platoncli query  getBlockByNumber -n 100 -c node_config.json
~~~

- 参数说明

>-c/--config:节点配置文件（非必填）
>
>-n/--number:区块的快高

### 根据区块hash查询区块信息

- 命令

~~~
platoncli query  getBlockByNumber -h <hash> -c node_config.json
~~~

- 参数说明

>-c/--config:节点配置文件（非必填）
>
>-n/--hash:区块的hash

### 查询当前的结算周期的区块奖励

- 命令

```
platoncli query getPackageReward -c node_config.json
```

- 参数说明

> -c/--config:节点配置文件（非必填）

### 查询区块打包的平均时间

- 命令

~~~
platoncli query getAvgPackTime -c node_config.json
~~~

- 参数说明

> -c/--config:节点配置文件（非必填）

## 质押模块

### 质押交易

- 命令

~~~
platoncli staking create -f staking_create_params.json -d staking.json
~~~

- 参数说明

>-f/--file:创建质押交易所需要的参数
>
>-d/--address:钱包名或钱包地址
>
>-t/--template:查看file所需要的参数都有哪些（非必填）
>
>-c/--config:节点配置文件（非必填）
>
>-o/--offline:是否生成待签名文件（离线交易，非必填）
>
>-s/--style:待签名信息存入csv文件还是二维码（默认存入csv文件，非必填）

### 修改质押信息

- 命令

~~~
platoncli staking update -f staking_update_params.json -d staking.json
~~~



- 参数说明

>-f/--file:创建质押交易所需要的参数
>
>-d/--address:钱包名或钱包地址
>
>-t/--template:查看file所需要的参数都有哪些（非必填）
>
>-c/--config:节点配置文件（非必填）
>
>-o/--offline:是否生成待签名文件（离线交易，非必填）
>
>-s/--style:待签名信息存入csv文件还是二维码（默认存入csv文件，非必填）

### 退出质押交易

- 命令

~~~
platoncli staking unStaking -d staking.json -f staking_unStaking_params.json
~~~

- 参数说明

>-f/--file:创建质押交易所需要的参数
>
>-d/--address:钱包名或钱包地址
>
>-c/--config:节点配置文件（非必填）
>
>-o/--offline:是否生成待签名文件（离线交易，非必填）
>
>-s/--style:待签名信息存入csv文件还是二维码（默认存入csv文件，非必填）

### 增持质押交易

- 命令

~~~
platoncli staking increase -d staking.json -f staking_increase_params.json
~~~

- 参数说明

>-f/--file:创建质押交易所需要的参数
>
>-d/--address:钱包名或钱包地址
>
>-t/--template:查看file所需要的参数都有哪些（非必填）
>
>-c/--config:节点配置文件（非必填）
>
>-o/--offline:是否生成待签名文件（离线交易，非必填）
>
>-s/--style:待签名信息存入csv文件还是二维码（默认存入csv文件，非必填）

### 查询

- 命令

依次对应查询当前共识周期验证人列表、查询当前共识周期的验证人列表、查询当前共识周期的验证人列表、查询当前的结算周期的质押奖励、根据nodeid查询节点质押信息

~~~
platoncli staking query -f getVerifierList			
platoncli staking query -f getValidatorList			
platoncli staking query -f getCandidateList			
platoncli staking query -f getCandidateInfo			
platoncli staking query -f getStakingReward -n <nodeid>
~~~

- 参数说明

>-f/--function:查询类型，必填
>
>-n/--nodeid:节点ID，非必填

## 委托模块

### 创建委托

- 命令

~~~
platoncli delegate new -p delegate_new_params.json -d test_delegate.json
~~~

- 参数说明

>-p/--params:创建质押交易所需要的参数
>
>-d/--address:钱包名或钱包地址
>
>-t/--template:查看file所需要的参数都有哪些（非必填）
>
>-c/--config:节点配置文件（非必填）
>
>-o/--offline:是否生成待签名文件（离线交易，非必填）
>
>-s/--style:待签名信息存入csv文件还是二维码（默认存入csv文件，非必填）

### 减持/撤销委托

- 命令

~~~
platoncli delegate unDelegate -p delegate_new_params.json -d test_delegate.json
~~~

- 参数说明

>-p/--params:创建质押交易所需要的参数
>
>-d/--address:钱包名或钱包地址
>
>-t/--template:查看file所需要的参数都有哪些（非必填）
>
>-c/--config:节点配置文件（非必填）
>
>-o/--offline:是否生成待签名文件（离线交易，非必填）
>
>-s/--style:待签名信息存入csv文件还是二维码（默认存入csv文件，非必填）

### 查询账户在各节点未提取委托奖励

- 命令

~~~
platoncli delegate  getDelegateReward -p params.json
~~~

- 参数说明

>-p/--params:创建质押交易所需要的参数
>
>-c/--config:节点配置文件（非必填）

### 提取委托奖励

- 命令

~~~
platoncli delegate withdrawDelegateReward -d wallet.json/atx1mxpyhpmtcdsgy6cg9dv6ze6sajdek4fpt4sdj5（钱包名或钱包地址）
~~~

- 参数说明

>-d/--address:钱包名或钱包地址
>
>-c/--config:节点配置文件（非必填）
>
>-o/--offline:是否生成待签名文件（离线交易，非必填）
>
>-s/--style:待签名信息存入csv文件还是二维码（默认存入csv文件，非必填）

### 查询当前账户地址所委托的节点的NodeId和质押Id

- 命令

~~~
platoncli delegate getRelatedListByDelAddress -d 钱包名或钱包地址
~~~

- 参数说明

>-d/--address:钱包名或钱包地址
>
>-c/--config:节点配置文件（非必填）

## 治理模块

### 提案相关

- 文本提案参数（写入到government.json文件）

~~~
{
  "verifier": "da99eb65da965e24684be1703a25e434a8a2036b19def8b4563cc16a8463b76abf44ef5bf639d790e4ce3a8fcb6697d1fd7e9140ad61438ebb492fba5dd931a2",
  "pIDID": "012345678",
  "transaction_cfg":{"gas":1000000,
                   "gasPrice":3000000000000000,
                   "nonce":null}
}
~~~

- 升级提案（写入到government.json文件）

~~~
{
  "verifier": "da99eb65da965e24684be1703a25e434a8a2036b19def8b4563cc16a8463b76abf44ef5bf639d790e4ce3a8fcb6697d1fd7e9140ad61438ebb492fba5dd931a2",
  "pIDID": "202101041633",
  "endVotingRound": 1,
  "newVersion": 202111,
  "transaction_cfg":{"gas":1000000,
                   "gasPrice":3000000000000000,
                   "nonce":null}
}
~~~

- 参数提案（写入到government.json文件）

~~~
{
  "verifier": "da99eb65da965e24684be1703a25e434a8a2036b19def8b4563cc16a8463b76abf44ef5bf639d790e4ce3a8fcb6697d1fd7e9140ad61438ebb492fba5dd931a2",
  "pIDID": "202101041643",
  "module": "reward",
  "name": "increaseIssuanceRatio",
  "newValue": "700",
  "transaction_cfg": {
    "gas": 1000000,
    "gasPrice": 3000000000000000,
    "nonce": null
  }
}
~~~

- 删除提案（写入到government.json文件）

~~~
{
  "verifier": "da99eb65da965e24684be1703a25e434a8a2036b19def8b4563cc16a8463b76abf44ef5bf639d790e4ce3a8fcb6697d1fd7e9140ad61438ebb492fba5dd931a2",
  "pIDID": "202101041633",
  "endVotingRound": 1,
  "canceledProposalID": "e76954762f11994cd3cb619149f0995a907c09542e8c283aaed3faccc87b8383",
  "transaction_cfg":{"gas":1000000,
                   "gasPrice":3000000000000000,
                   "nonce":null}
}
~~~

- 命令

~~~
platoncli government submitProposal -p D:\project\platoncli\test_params_file\government.json -d atx1gjfg7ajul09r246e
gegr3xqglxdh0r7unnej8h -m TextProposal -o
~~~

- 参数说明

>-p/--params:创建质押交易所需要的参数
>
>-d/--address:钱包名或钱包地址
>
>-m/--module:文本（TextProposal）、升级（VersionProposal）、参数（ParamProposal）、取消提案（CancelProposal）
>
>-t/--template:查看file所需要的参数都有哪些（非必填）
>
>-c/--config:节点配置文件（非必填）
>
>-o/--offline:是否生成待签名文件（离线交易，非必填）
>
>-s/--style:待签名信息存入csv文件还是二维码（默认存入csv文件，非必填

### 查询提案列表

- 命令

~~~
platoncli government listProposal
~~~

- 参数说明

> -c/--config:节点配置文件（非必填）

### 查询治理参数列表

- 命令

~~~
platoncli government listGovernParam
~~~

- 参数说明

> -c/--config:节点配置文件（非必填）

### 根据提案id查询提案信息

- 命令

~~~
platoncli government getProposal -pid xxxxxx
~~~

- 参数说明

>-c/--config:节点配置文件（非必填）
>
>-pid/--proposal_id:提案ID

### 查询最新的治理参数值

- 命令

~~~
platoncli government getGovernParamValue -m xxx -n xxxx
~~~

- 参数说明

>-m/--module:参数模块
>
>-n/--name:参数名字
>
>-c/--config:节点配置文件（非必填）

### 查询节点的链生效版本

- 命令

~~~
platoncli government getActiveVersion
~~~

- 参数说明

> -c/--config:节点配置文件（非必填）

### 查询提案结果

- 命令

platoncli government getTallyResult -pid xxxx

- 参数说明

>-c/--config:节点配置文件（非必填）
>
>-pid/--proposal_id:提案ID

### 查询提案的累计可投票人数

- 命令

~~~
platoncli government getAccuVerifiersCount -h xxxx -pid xxxx
~~~

- 参数说明

>-c/--config:节点配置文件（非必填）
>
>-pid/--proposal_id:提案ID
>
>-h/--hash:The hash of the current latest block

### 查询节点是否已被举报过多签

- 命令

~~~
platoncli government checkDuplicateSign -t 2 -n xxx -b 10000
~~~

- 参数说明

>-t/--type：多签类型，代表双签类型，1：prepareBlock，2：prepareVote，3：viewChange
>
>-n/--nodeid:节点ID
>
>-b/--blocknumber:块高
>
>-c/--config:节点配置文件（非必填）

### 提案投票

### 版本声明

- 命令

~~~
platoncli government declareVersion -p D:\project\platoncli\test_params_file\government.json -d atp155nj3uwdpej7w0jc6hgttskwf4j4gjx948hxjk
~~~

- 参数说明

>-p/--params:创建交易所需要的参数
>
>-d/--address:钱包名或钱包地址
>
>-c/--config:节点配置文件（非必填）
>
>-o/--offline:是否生成待签名文件（离线交易，非必填）
>
>-s/--style:待签名信息存入csv文件还是二维码（默认存入csv文件，非必填）

- 参数文件（写入government.json）

~~~
{
 "activeNode": "19f1c9aa5140bd1304a3260de640a521c33015da86b88cd2ecc83339b558a4d4afa4bd0555d3fa16ae43043aeb4fbd32c92b34de1af437811de51d966dc64365",
  "transaction_cfg": {
    "gas": 1000000,
    "gasPrice": 3000000000000000,
    "nonce": null
  }
}
~~~

### 举报双签

- 命令

~~~
platoncli government reportDoubleSign --address <walletName.json> --param xxxxxxxxxxxxx
~~~

- 参数说明

>-p/--params:创建交易所需要的参数
>
>-d/--address:钱包名或钱包地址
>
>-c/--config:节点配置文件（非必填）
>
>-o/--offline:是否生成待签名文件（离线交易，非必填）
>
>-s/--style:待签名信息存入csv文件还是二维码（默认存入csv文件，非必填）

## 锁仓模块

### 创建锁仓计划

- 命令

~~~
platoncli hedge -p hedge.json -d wallet.json
~~~

- 参数说明

>-p/--params:创建交易所需要的参数
>
>-d/--address:钱包名或钱包地址
>
>-c/--config:节点配置文件（非必填）
>
>-o/--offline:是否生成待签名文件（离线交易，非必填）
>
>-s/--style:待签名信息存入csv文件还是二维码（默认存入csv文件，非必填）

- 参数文件hedge.json

~~~
{
  "account":"atx1ye5mdkq33937cz9xcpa94jgn9k54sqt758cskj",
  "plans": [
    {
      "epoch": 300,
      "amount": 1000
    }
  ]
}
~~~



###  获取锁仓信息

- 命令

~~~
platoncli hedge GetRestrictingInfo -a xxxx
~~~

- 参数说明

>-c/--config:节点配置文件（非必填）
>
>-a/--address:锁仓释放到账账户（必须为钱包地址）