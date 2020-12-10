## cli命令流程设计

### 初始化cli

- 命令

```shell
platoncli init -h [lat/lax/atp/atx]
```

- 参数说明：

> -h:  地址格式类型，包括：lat/lax/atp/atx，默认lat，分别对应初始的chainid为：100/101/201018/201030；
>
> --private_chain/--no-private_chain：是否是搭建私链，默认为否；



- 主要实现功能

  生成主要的配置文件：

  - 节点配置文件：node_config.json；
  - 资源下载路径配置文件：download_conf.json；（从服务器中下载，保证二进制有更新时，用户通过初始化cli可以拿到最新的文件）
  - 创世区块配置文件：genesis.json （如果部署私链）。



- 执行过程

  流程图如下：

  ![初始化cli](.\img\初始化cli.png)

- 过程详解

> 执行过程：分两种情况：
>
> - 情况一：加入网络，表示节点已创建，生成连接信息配置文件即可，模板如下：
>
>   ```json
>  {
>   	"nodeAddress": "192.168.21.46",
>  	"rpcPort": "6789",
>   	"hrp": "atp",
>  	"chainId": 201018
>   }
>   ```
>   
>   > 其中：chainId通过rpc接口获取；hrp类型根据实际情况修改；
>   
>   
>   
> - 情况二：不加入网络，表明：cli用于离线签名或无节点可连接，通过是否生成下载资源配置文件模板来区分这两种情况：
>
>   - 如果不需要下载即表示cli用于离线签名，直接生成签名信息配置文件即可，如下：
>
>     ```json
>   {
>     	"nodeAddress": "",
>    	"rpcPort": "",
>     	"hrp": "atp",
>    	"chainId": 201018
>     }
>     ```
>
>   - 如果需要下载，则从服务器中下载（保证二进制有更新时，用户通过初始化cli可以拿到最新的文件）`download_conf.json`文件，放到当前config目录下， 注意：底层二进制发版时，需要将download_conf.json文件同步更新到服务器上，其中下载路径匹配当前PlatON和Alaya网络底层对应的最后一个发行版本，以PlatON的0.13.0和Alaya的0.13.1为例：
>
>     ```json
>     {
>         "platon_binary_url": "https://github.com/PlatONnetwork/downloads/releases/download/platon/0.13.0/binaries/platon-linux-amd64.tar.gz",
>     	"platon_genesis_url": "https://github.com/PlatONnetwork/downloads/releases/download/platon/0.13.0/genesis/genesis.json",
>     	"alaya_binary_url": "https://github.com/PlatONnetwork/downloads/releases/download/alaya/0.13.1/binaries/platon-linux-amd64.tar.gz",
>         "alaya_genesis_url": "https://github.com/PlatONnetwork/downloads/releases/download/alaya/0.13.1/genesis/genesis.json"
>     }
>     ```
>
>      > platon_binary_url：PlatON网络二进制下载路径；
>      >
>      > platon_genesis_url：PlatON网络创世区块文件模块。
>      >
>      > alaya_binary_url：Alaya网络二进制下载路径；
>      >
>      > alaya_genesis_url：Alaya网络创世区块文件模块。
>      >
>
>       **<font color=red>如果生成的配置文件版本号不对或者用户想自己指定版本号，请手动修改当前config目录下的download_conf.json。</font>**
>
>     最后同样生成节点信息配置文件node_config.json。
>



### 初始化节点

- 命令

```shell
platoncli node init -h [lat/lax/atp/atx]
```

- 参数说明

> -h:  地址格式类型，包括：lat/lax/atp/atx，默认lat；
>
> --private_chain/--no-private_chain：是否是搭建私链，默认为否；



- 主要实现功能
  - 下载资源：二进制等；
  - 生成blskey和nodekey，如果是私链，写入创世区块文件，并初始化创世区块；（platonkey/alayakey）
  - 生成启动参数模板文件，并保存在cli当前路径的template目录下；



- 执行过程

![初始化节点](.\img\初始化节点.png)

> 判断是否已经初始化：
>
> - 二进制是否存在
> - key是否生成（4个）
> - 如果是私链的话，判断创世区块是否已经初始化

### 启动/重启节点

- 命令

```shell
platoncli node start
```

- 参数说明

  无



- 主要实现功能
  - 校验节点启动条件，获取参数启动或重启节点；



- 执行过程

![启动节点](.\img\启动节点.png)

>说明：
>
>- 是否初始化依据：
>
>  指定目录下是否有platon二进制文件；
>
>- 是否部署私链：
>
>  template/platon_cfg.tmpl的网络类型字段`NetWork`为空即为私链；
>
>- 是否已部署依据：
>
>  是否有有data数据；
>
>- 节点是否启动依据：
>
>  是否有进程的占用端口号与template/platon_cfg.tmpl一致；