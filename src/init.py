# _*_ coding:utf-8 _*_
import click

from precompile_lib import Web3, HTTPProvider, Eth, Admin
from utility import get_command_usage, cust_print, init_node, download_genesis_file, download_url_config_file, save_node_conf


@click.option('-w', '--withnode', is_flag=True, default=False, help='Whether to initialize the node？')
@click.option('-p', '--private_chain', is_flag=True, default=False, help='是否是搭建私链？(默认：否).')
@click.option('-h', '--hrp', required=True, default='lat', help='this is params is net type')
@click.option('-c', '--config', default="", help="genesis block config.")
@click.option('-cid', '--chain_id', default="", help="This parameter must be added when the node is not initialized or "
                                                    "needs to be added to the network")
@click.command(help="Initialize the PlatON CLI tool.", cls=get_command_usage("init", False))
def init(withnode, private_chain, hrp, config, chain_id):
    chainId = chain_id
    if withnode:
        # install_node(hrp)
        init_node(hrp, private_chain, config)
    else:
        # init cli
        cust_print("start init platon cli...", fg='g')

        ip = ""
        rpc_port = ""
        # Whether to join the network
        confirm = input('Whether to join the network? [Y|y/N|n]: ')
        if confirm == 'Y' or confirm == 'y':
            cust_print('start to join the network.', fg='b')
            while True:
                # Join the Network (IP, RPC)
                ip = input('Please enter the node IP: ')
                rpc_port = input('Please enter the node rpc port: ')

                url = "http://{}:{}".format(ip, rpc_port)

                # Verify that the nodes are connected properly
                try:
                    w3 = Web3(HTTPProvider(url))
                    platon = Eth(w3)
                    blkNumber = platon.blockNumber
                    cust_print('get block number:{}'.format(blkNumber), fg='g')
                    cust_print('connect to node succeed.', fg='g')
                    # 获取chainid
                    admin = Admin(w3)
                    chainId = admin.nodeInfo.protocols.platon.config.chainId
                    cust_print('get node chainId: {}'.format(chainId), fg='g')
                except Exception as e:
                    # Failure of connection prompts replacement of IP and RPC reconnection
                    cust_print("connect to node failed.", fg='r')
                    cust_print(e, fg='r')
                    confirm = input('Connection exception, Whether to switch node? [Y|y/N|n]: ')
                    if confirm == 'Y' or confirm == 'y':
                        cust_print('Start to switch node.', fg='y')
                        continue
                    else:
                        cust_print('connect to node failed!!!', fg='r')
                        return
                break
        else:
            # 不连节点或无节点可连
            # 下载路径配置文件
            download_url_config_file()
            # 私链，下载创世区块文件
            if private_chain:
                download_genesis_file(hrp)
            else:
                # 离线节点,用于签名交易,需要确认node_config.json中chainId的值
                pass

        # 保存配置文件
        node_conf_path = save_node_conf(ip, rpc_port, hrp, chainId)
        cust_print('generate config file succeed: {}.'.format(node_conf_path), fg='g')
