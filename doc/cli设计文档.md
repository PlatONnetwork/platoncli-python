## cli设计文档

### 设计目标

- 代码简单，工具易用；
- 功能完善，互相独立；
- 易于维护，便于扩展；



### 依赖库

cli使用的依赖库主要包括两大部分，分别为外部依赖库和内部依赖库python sdk，其中外部依赖库主要包括命令行处理库click和日志处理库logging，内部依赖库为矩阵元内部的python sdk；

- **click**
  - 用于快速创建命令行，简单易用，功能丰富；
  - 可定制化命令集合类，只需要重写`@click.group`命令中的cls参数传入返回自定义命令集合类的函数即可；
  - 自定义命令集合类较简单，只需要重写list_commands，get_command，parse_args接口即可；list_commands：列出满足条件的所有的命令；get_command：获取指定命令的详细说明；parse_args：解析参数接口。
- **logging**
  - 可自定义日志级别，日志格式等；
  - 简单易用；
- **python sdk**
  - 包括PlatON网络的client-sdk-python和Alaya网络的alaya.py；主要用于钱包的创建，rpc命令的调用，交易的签名等；



### 日志模块设计

对应python文件为：logger.py

- 日志级别

  - 由低到高：debug，info，warning，error，critical；

  - 默认日志级别：info；
  - 控制台打印信息颜色对应为：debug对应为蓝色，info为绿色，warning为黄色，error为红色，ctritical为紫色；

  

- 日志内容格式

  > {timestamp} - {loglevel} - Operation: {msg}
  >
  > 如：
  >
  > 2020-05-29 17:07:38 - INFO - Operation: node init, type is: main net

  

- 日志存放

  > 存放路径：当前窗口所在的log子目录下
  >
  > log文件名称：platoncliYYYYMMDD.log，如：platon20200529.log

  

- 设置日志级别接口

  - 接口名：setLogLevel

  - 参数：level

    > - level：日志级别，默认为info

- 保存日志接口

  - 接口名：writeLog

  - 参数：msg，level

    > - msg：操作信息
    > - level：日志级别，默认为info

  - 不保存比初始化的日志级别低的日志记录。



### 命令概要设计

cli命令主要分为如下三种模式：

- **帮助和版本号**

```
platoncli --help/-h
platoncli --version/-v
```

> - --help/-h为帮助命令，显示cli的子模块名和命令名，以及对应的帮助说明，如下：
>
>   ```shell
>   Usage: platoncli [Submodule/Command] [COMMAND] [ARGS]...
>   
>       platoncli 工具
>   
>       --help -h     帮助
>       --version -v  版本号
>   
>   Submodules:
>       account        钱包管理模块
>       delegate       委托模块
>       government     治理模块
>       hedge          锁仓模块
>       node           节点管理模块
>       query          查询模块
>       staking        质押模块
>       tx             交易管理模块
>   
>   Commands:
>       init           Initialize the PlatON CLI tool.
>   ```
>
> - --version/-v为当前工具的版本，包括版本号，commitid和发布工具的时间戳；从发版的version文件读取，如下：
>
>   ```shell
>   version: 0.1.0
>   revision: e7445df88a05487dc42fdfd7178cb034b15c3c15
>   timestamp: 2020-11-17 11:29:40
>   ```

- **command命令模式**

```
platoncli command params
```

> 目前只有init命令是此模式，此命令为初始化cli工具，可使用命令：`platoncli init --help` 查看；

- **submodule+command模式**

```shell
platoncli submodule command params
```

> - submodule：子模块名称，如：
>
>   ```shell
>   account        钱包管理模块
>   delegate       委托模块
>   government     治理模块
>   hedge          锁仓模块
>   node           节点管理模块
>   query          查询模块
>   staking        质押模块
>   tx             交易管理模块
>   ```
>
> - command：子模块对应的命令，如node模块，可使用命令：`platoncli node --help` 查看：
>
>   ```shell
>   Usage: platoncli.exe node COMMAND [ARGS]...
>   
>     节点管理模块
>   
>   Options:
>     --help  Show this message and exit.
>   
>   Commands:
>     blockexport      this is node submodule blockexport command.
>     blockinpute      this is node submodule blockinpute command.
>     check            this is node submodule check command.
>     generateBlsKey   this is node submodule generateBlsKey...
>     generateNodeKey  this is node submodule generateNodeKey...
>     info             this is node submodule info command.
>     init             this is node submodule init command.
>     move             this is node submodule move command.
>     reset            this is node submodule reset command.
>     rollback         this is node submodule rollback command.
>     start            this is node submodule start command.
>     stop             this is node submodule stop command.
>     upgrade          this is node submodule upgrade command.
>   ```
>
>   > commands为对应模块node下的所有命令，<font color=red>对应的命令用法可通过：`platoncli node command --help`查看，</font>其他模块的用法相同。

**<font color=red>命令的详细流程设计，请参考文档：[cli命令流程设计.md](./cli命令流程设计.md)。</font>**



### 框架设计

​	**为了方便扩展和维护，采用每个子模块对应src目录下的一个子目录，每个命令对应一个python文件的方式，模块名和对应的子目录名称相同，命令名和应的文件名相同，子模块之间和命令之间相互独立，可自由的增加和删除**；代码结构设计如下：

> platoncli.py: 主程序入口
>
> precompile_lib.py：使用pyInstaller打包时需要编译到二进制中的库
>
> logger.py：日志系统模块
>
> utility.py：公共接口模块
>
>  src：  命令代码存放路径
>
> ​	|-------- node：节点操作模块，此目录下存放所有此模块的命令和帮助说明文件help
>
> ​	|--------account：钱包管理模块，此目录下存放所有此模块的命令和帮助说明文件help
>
> ​	|--------tx：交易管理模块，此目录下存放所有此模块的命令和帮助说明文件help	
>
> ​	|--------staking：质押模块，此目录下存放所有此模块的命令和帮助说明文件help
>
> ​	|--------delegate：委托模块，此目录下存放所有此模块的命令和帮助说明文件help	
>
> ​	|--------government：治理模块，此目录下存放所有此模块的命令和帮助说明文件help
>
> ​	|--------query：链相关的基本信息查询模块，此目录下存放所有此模块的命令和帮助说明文件help	
>
> ​	|--------hedge：锁仓模块，此目录下存放所有此模块的命令和帮助说明文件help	
>
> ​	|--------init.py：初始化cli工具命令文件	

为了能让程序自动加载命令和模块，后续只需要以打补丁的方式进行发版；启动cli时，加载src目录下的目录和文件，以子目录名为子模块，以.py文件为命令；

工作机制：

- 加载src目录下的模块和命令，（保存在缓存中，用于判断命令是子模块还是命令）
- 根据cli的命令，选择模式；
- 执行对应的命令；



### 发版文件

发版底层二进制时，匹配当前PlatON和Alaya网络底层最后一个版本放到服务器上，以PlatON的0.14.0和Alaya的0.13.1为例：

- 资源下载配置文件：download_conf.json

  ```json
  {
  	"platon_url": "https://github.com/PlatONnetwork/downloads/releases/download/platon/0.14.0",
  	"alaya_url": "https://github.com/PlatONnetwork/downloads/releases/download/alaya/0.13.1"
  }
  ```

  

- 启动命令模板：template/platon_cfg.tmpl

  ```toml
  [platon]
  network = ${network}
  identity = platon
  datadir = ./data
  port = 16789
  rpcaddr = 127.0.0.1
  rpcport = 6789
  rpcapi = db,platon,net,web3,admin,personal
  nodekey = ./nodekey
  blskey = ./blskey
  verbosity = 3
  syncmode = fast
  logfile = ./log/platon.log
  ```

  

- 日志切分模板：template/platon_logrotate.tmpl (Linux系统)

  ```toml
  ${base_dir}/log/platon.log {
      rotate 24
      copytruncate
      missingok
      notifempty
      olddir ${base_dir}/log
      dateext
      dateformat .%Y%m%d-%H
      compress
  }
  
  ${base_dir}/log/platoncli.log {
      rotate 24
      copytruncate
      missingok
      notifempty
      olddir ${base_dir}/log
      dateext
      dateformat .%Y%m%d-%H
      compress
  }
  ```

- 配置切分日志定时任务模板：template/platon_cron.tmpl (Linux系统)

  ```shell
  0 * * * * /usr/sbin/logrotate -s ${base_dir}/log/.status ${base_dir}/conf/.platon_logrotate
  ```

  

- 节点配置文件node_config.json

  ```json
  {"rpcAddress": "http://127.0.0.1:6789:", "hrp": "atp", "chainId": 201018}
  ```

  