import click
import sys
import os
import json
from utility import get_command_usage, cust_print, g_dict_dir_config, connect_node
from precompile_lib import Web3, HTTPProvider, Eth


@click.command(cls=get_command_usage("account"))
@click.option('-d', '--address', required=True, help='wallet address.')
@click.option('-c', '--config', default="",
              help='The configuration file specifying the IP and port of the '
                   'transaction to be sent. If it is configured in the global configuration network file, IP and prot '
                   'can be obtained by specifying the name in the configuration. If the network configuration is not '
                   'filled in.')
def balance(address, config):
    if 42 != len(address):
        cust_print("Wrong address parameter: --address {}".format(address), fg='r')
        sys.exit(1)
    hrp = address[:3]

    # 节点配置文件
    if "" == config:
        config = os.path.join(g_dict_dir_config["conf_dir"], "node_config.json")
    if not os.path.exists(config):
        cust_print("The node profile exists:{}, please check it.".format(config), fg='r')
        sys.exit(1)
    try:
        with open(config, 'r') as f:
            rpcAddress = json.load(f)['rpcAddress']
    except:
        cust_print('{} data is incorrect format!!!'.format(config))
        sys.exit(1)
    try:
        w3 = Web3(HTTPProvider(rpcAddress))
        platon = connect_node(w3, Eth)
        free = platon.getBalance(address)
        convert_free = w3.fromWei(free, "ether")
        cust_print('{} remaining balance:{} {}'.format(address, convert_free, hrp.upper()), fg='g')
    except Exception as e:
        cust_print('balance send transfer transaction fail,error info:{}'.format(e), fg='r')
        sys.exit(1)
