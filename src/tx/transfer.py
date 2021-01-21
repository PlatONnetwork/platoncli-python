import json
import os
import sys

import click

from utility import get_command_usage, g_dict_dir_config, cust_print, get_address_by_file_name, \
    get_wallet_file_by_address, get_time_stamp, write_csv, g_system, input_passwd_for_win, input_passwd_for_linux, \
    get_private_key_from_wallet_file, sign_one_transaction_by_prikey, send_transaction, connect_node,write_QRCode
from bech32_addr import decode
from precompile_lib import Web3, HTTPProvider, Eth, Account, keys


def show_params():
    print('''
      类型\t     必填性\t  参数名称\t   参数解释\t
    String\t  optional\t     from\t   交易发送方,由--address参数指定
    String\t      must\t       to\t   交易接收方
    int   \t  optional\t      gas\t   本次交易gas用量上限
    int   \t  optional\t gasPrice\t   Gas价格
    int   \t      must\t    value\t   转账金额，单位LAT/LAX/ATP/ATX
    String\t  optional\t     data\t   上链数据
    ''')


# 生成未签名交易
def transfer_unsign(from_address, to_address, gasPrice, gas, value, nonce, chain_id) -> dict:
    transaction_dict = {
        'from': from_address,
        "to": to_address,
        "gasPrice": gasPrice,  # 1000000000,
        "gas": gas,  # 4700000,
        "nonce": nonce,
        "data": "",
        "chainId": chain_id,
        "value": value,
    }
    return transaction_dict


@click.command(cls=get_command_usage("tx"))
@click.option('-p', '--param', required=True, default="", help='The transaction parameter json string, or the '
                                                               'transaction parameter json file path.')
@click.option('-d', '--address', required=True, default="", help='Send the transaction address or name.json')
@click.option('-o', '--offline', is_flag=True, default=False,
              help='Offline transaction or offline transaction offline not input is the default '
                   'for online transaction, and a two-dimensional code picture is generated and '
                   'placed on the desktop, providing ATON offline scanning code signature.')
@click.option('-t', '--template', is_flag=True, default=False,
              help='View the transaction parameter template. It is '
                   'not effective to coexist with other parameters.')
@click.option('-c', '--config', default="",
              help='The configuration file specifying the IP and port of the '
                   'transaction to be sent. If it is configured in the global configuration network file, IP and prot '
                   'can be obtained by specifying the name in the configuration. If the network configuration is not '
                   'filled in.')
@click.option('-s', '--style', default="", help='This parameter is used to determine the type of file to be signed')
def transfer(param, address, offline, template, config, style):
    """
    this is tx submodule transfer command.
    """
    if template:
        show_params()
        return

    if param.endswith(".json"):
        try:
            with open(param, 'r') as f:
                dict_param = json.load(f)
        except:
            cust_print(
                "Params json file not exists or json file saved data is not json data,Please check {}".format(param),
                fg='r')
            sys.exit(1)
    else:
        param = param.replace("\'", "\"")
        # 交易参数
        dict_param = json.loads(param)
    if "to" not in dict_param or "value" not in dict_param or 42 != len(dict_param["to"]):
        cust_print("The transaction parameter is wrong, please check: {}.".format(param), fg='r')
        sys.exit(1)

    # 节点配置文件
    if "" == config:
        config = os.path.join(g_dict_dir_config["conf_dir"], "node_config.json")
    if not os.path.exists(config):
        cust_print("The node profile exists:{}, please check it.".format(config), fg='r')
        sys.exit(1)

    with open(config, 'r') as load_f:
        node_conf_info = json.load(load_f)
        hrp = node_conf_info["hrp"]
        chainId = node_conf_info["chainId"]
        rpcAddress = node_conf_info["rpcAddress"]

    w3 = Web3(HTTPProvider(rpcAddress))
    platon = connect_node(w3, Eth)

    if dict_param["to"][:3] != hrp:
        cust_print("To address is not in the right format:{}. What you want is {}.".
                   format(dict_param["to"], hrp), fg='r')
        sys.exit(1)

    # 检查to地址是否合法
    if not decode(hrp, dict_param["to"]):
        cust_print("The to address is a non-BECh32 format address {}.".
                   format(dict_param["to"]), fg='r')
        sys.exit(1)

    # 检查from地址是否合法
    wallet_dir = g_dict_dir_config["wallet_dir"]
    wallet_file_path = ""
    net_type = "mainnet"
    if 'lax' == hrp or 'atx' == hrp:
        net_type = "testnet"
    if address.endswith(".json"):
        from_address, wallet_file_path = get_address_by_file_name(wallet_dir, address, net_type)
    elif 42 != len(address):
        cust_print("Wrong address parameter: --address {}".format(address), fg='r')
        sys.exit(1)
    else:
        # 在线直接发送交易,需要钱包文件
        if not offline:
            find, wallet_file_path, fileName = get_wallet_file_by_address(wallet_dir, address)
            if not find:
                cust_print('hrp:{}, The wallet file of address:{} could not be found on {}'.
                           format(hrp, address, wallet_dir), fg='r')
                sys.exit(1)
        from_address = address

    # 检查from地址是否合法
    if not decode(hrp, from_address):
        cust_print("The from address is a non-BECh32 format address {}.".
                   format(from_address), fg='r')
        sys.exit(1)

    # w3 = Web3(HTTPProvider(rpcAddress))
    # platon = Eth(w3)

    # 查询余额
    free = platon.getBalance(from_address)
    if float(free) <= float(dict_param["value"]):
        free_amount = w3.fromWei(free, "ether")
        cust_print("The balance is insufficient for the transfer, balance: {} {}.".
                   format(free_amount, hrp), fg='r')
        sys.exit(1)

    nonce = platon.getTransactionCount(from_address)
    value = w3.toWei(str(dict_param["value"]), "ether")
    gas = 4700000
    gasPrice = 1000000000
    if "gas" in dict_param:
        gas = int(dict_param["gas"])
    if "gasPrice" in dict_param:
        gasPrice = int(dict_param["gasPrice"])

    dict_transfer_tx = transfer_unsign(from_address, dict_param["to"], gasPrice, gas, value, nonce, chainId)

    # 离线方式
    if offline:
        try:
            unsigned_tx_dir = g_dict_dir_config["unsigned_tx_dir"]
            if not os.path.exists(unsigned_tx_dir):
                os.mkdir(unsigned_tx_dir)
            unsigned_file_csv_name = "unsigned_tx_transfer_{}.csv".format(get_time_stamp())
            unsigned_file_path = os.path.join(unsigned_tx_dir, unsigned_file_csv_name)
            all_transaction = [dict_transfer_tx]
            # 生成待签名文件
            if style == '':
                write_csv(unsigned_file_path, all_transaction)
            else:
                unsigned_file_path = unsigned_file_path.replace('csv','jpg')
                write_QRCode(all_transaction, unsigned_file_path)
            cust_print('unsigned_file save to:{}'.format(unsigned_file_path), fg='g')
        except Exception as e:
            print('{} {}'.format('exception: ', e))
            cust_print('generate unsigned transfer transaction file failure:{}!!!'.format(e), fg='r')
            sys.exit(1)

        else:
            cust_print('generate unsigned transfer transaction file successful:{}'.format(unsigned_file_path), fg='g')
    else:
        try:
            # 输入钱包密码，解锁私钥
            prompt_message = "Enter password:"
            if 'windows' == g_system:
                passwd = b''.join(input_passwd_for_win(prompt_message)).decode()
            else:
                passwd = input_passwd_for_linux(prompt_message)

            # 获取私钥
            privateKey = get_private_key_from_wallet_file(Account, keys, wallet_file_path, passwd)
            # 签名交易
            rawTransaction, _ = sign_one_transaction_by_prikey(Account, None, dict_transfer_tx, hrp, privateKey)
            # print(rawTransaction)
            # 发送交易
            txhash, _ = send_transaction(platon, rawTransaction)

        except Exception as e:
            cust_print('send transfer transaction failure, chainid:{}, error message:{}!!!'.format(chainId, e), fg='r')
            sys.exit(1)
        else:
            cust_print('send transfer transaction successful, tx hash:{}.'.format(txhash), fg='g')
