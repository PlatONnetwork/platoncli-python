import json
import os
import sys

import click

from utility import get_command_usage, g_dict_dir_config, cust_print, get_address_by_file_name, \
    get_wallet_file_by_address


def get_all_wallet_file_on_dir(dir_path, net_type):

    dict_all_wallet = {}
    for root, _, files in os.walk(dir_path):
        for name in files:
            if name.endswith(".json"):
                full_path = os.path.join(root, name)
                with open(full_path, 'r') as load_f:
                    wallet_info = json.load(load_f)
                    dict_all_wallet[full_path] = wallet_info["address"][net_type]
    return dict_all_wallet


@click.command(cls=get_command_usage("account"))
@click.option('-d', '--address', default="", help='Specify a name query or specify an address query.')
@click.option('-t', '--test_net', is_flag=True, default=False, help='是否是测试网地址？(默认：否).')
def check(address, test_net):
    """
    this is account submodule check command.
    """
    wallet_dir = g_dict_dir_config["wallet_dir"]
    net_type = "mainnet"
    if test_net:
        net_type = "testnet"
    cust_print("Start check wallet files...", fg='g')
    if "" != address:
        if address.endswith(".json"):
            check_name = address
            check_address, _ = get_address_by_file_name(wallet_dir, address, net_type)
        elif 42 != len(address):
            cust_print("Wrong address parameter: --address {}".format(address), fg='r')
            sys.exit(1)
        else:
            find, _, fileName = get_wallet_file_by_address(wallet_dir, address, net_type)
            if not find:
                cust_print('The wallet file of {} could not be found on {}'.format(fileName, wallet_dir),fg='r')
                sys.exit(1)
            check_name = fileName
            check_address = address
        cust_print("Name:{}, Address:{}".format(check_name, check_address), fg='g')
    else:
        dict_all_wallet = get_all_wallet_file_on_dir(wallet_dir, net_type)
        for k in dict_all_wallet:
            cust_print("Name:{}, Address:{}".format(k, dict_all_wallet[k]), fg='g')
