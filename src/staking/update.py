import click
import os
import sys
import rlp
from hexbytes import HexBytes
from utility import get_command_usage, get_eth_obj, cust_print, g_dict_dir_config, read_json_file, write_QRCode, \
    write_csv, get_time_stamp
from common import verify_password, un_sign_data, bech32_address_bytes, check_dir_exits
from client_sdk_python.packages.platon_account.internal.transactions import bech32_address_bytes


def rlp_params(args, hrp):
    benifit_address, node_id, external_id, node_name, website, details, _, reward_per, _ = args
    benifit_address = bech32_address_bytes(hrp)(benifit_address)
    data = HexBytes(rlp.encode([rlp.encode(int(1001)), rlp.encode(benifit_address), rlp.encode(bytes.fromhex(node_id)),
                                rlp.encode(reward_per),
                                rlp.encode(external_id), rlp.encode(node_name), rlp.encode(website),
                                rlp.encode(details)])).hex()
    return data


def show_params():
    print('''
       类型      必填性         参数名称             参数解释
       String    must          benifit_address     收益账户
       String    optional      node_id             节点ID
       String    optional      external_id         外部ID            
       String    optional      node_name           节点名字
       String    optional      website             节点的第三方主页
       String    optional      details             节点的描述
       int       must          reward_per          从佣金中获得的奖励份额的比例
       dict      optional      transaction_cfg     交易基本配置
       ''')


@click.command(cls=get_command_usage("staking"))
@click.option('-f', '--file', help='The file is save params.')
@click.option('-d', '--address', help='wallet address.')
@click.option('-t', '--template', is_flag=True, default=False, help='View the update staking parameter template. It is '
                                                                    'not effective to coexist with other parameters.')
@click.option('-c', '--config', default="",
              help='The configuration file specifying the IP and port of the '
                   'transaction to be sent. If it is configured in the global configuration network file, IP and prot '
                   'can be obtained by specifying the name in the configuration. If the network configuration is not '
                   'filled in.')
@click.option('-o', '--offline', is_flag=True, default=False,
              help='Offline transaction or offline transaction offline not input is the default '
                   'for online transaction, and a two-dimensional code picture is generated and '
                   'placed on the desktop, providing ATON offline scanning code signature.')
@click.option('-s', '--style', default="", help='This parameter is used to determine the type of file to be signed')
def update(file, address, template, config, offline, style):
    """
    this is staking submodule update command.
    """
    if template:
        show_params()
        return
    if not os.path.isfile(file):
        cust_print('file {} not exits! please check!'.format(file), fg='r')
        sys.exit(1)
    params = read_json_file(file)
    wallet_dir = g_dict_dir_config["wallet_dir"]
    wallet_file_path, private_key, hrp, _ = verify_password(address, wallet_dir)

    ppos = get_eth_obj(config, 'ppos')
    _params = {}
    try:
        _params['benifit_address'] = params['benifit_address']
        _params['node_id'] = params['node_id'] or ppos.admin.nodeInfo.id
        _params['external_id'] = params['external_id']
        _params['node_name'] = params['node_name']
        _params['website'] = params['website']
        _params['details'] = params['details']
        _params['pri_key'] = private_key[2:]
        _params['reward_per'] = params['reward_per']
        if isinstance(params['transaction_cfg'], dict):
            _params['transaction_cfg'] = params['transaction_cfg']
    except KeyError as e:
        cust_print('Key {} does not exist in file {},please check!'.format(e, file), fg='r')
        sys.exit(1)
    try:
        if offline:
            data = rlp_params(tuple(_params.values()), hrp)
            params['to_type'] = 'staking'
            transaction_dict = un_sign_data(data, params, ppos, _params['pri_key'])
            unsigned_tx_dir = g_dict_dir_config["unsigned_tx_dir"]
            check_dir_exits(unsigned_tx_dir)
            unsigned_file_csv_name = "unsigned_staking_update_{}.csv".format(get_time_stamp())
            unsigned_file_path = os.path.join(unsigned_tx_dir, unsigned_file_csv_name)
            if style == '':
                write_csv(unsigned_file_path, [transaction_dict])
            else:
                unsigned_file_path = unsigned_file_path.replace('csv', 'jpg')
                write_QRCode(transaction_dict, unsigned_file_path)
            cust_print('unsigned_file save to:{}'.format(unsigned_file_path), fg='g')
        else:
            tx_hash = ppos.editCandidate(*_params.values())
            cust_print('updateStaking send transfer transaction successful, tx hash:{}.'.format(tx_hash), fg='g')
    except ValueError as e:
        cust_print('updateStaking send transfer transaction fail,error info:{}'.format(e))
        sys.exit(1)
