# cli操作文档

## 基本操作

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

