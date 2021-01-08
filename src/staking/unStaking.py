import click
import re
import rlp
import sys
import os
from utility import get_command_usage, cust_print, g_dict_dir_config, get_eth_obj, read_json_file, write_csv, \
    get_time_stamp, write_QRCode
from common import verify_password, un_sign_data, check_dir_exits


def check_node_id(node_id):
    if len(node_id) > 128:
        cust_print('node id length more than the 128.', fg='r')
        sys.exit(1)
    if not node_id.isalnum():
        cust_print('node id contains illegal characters,please check.', fg='r')
        sys.exit(1)
    _re = re.compile(u'[\u4e00-\u9fa5]', re.UNICODE)
    match = re.search(_re, node_id)
    if match:
        cust_print('node id contains chinese characters', fg='r')
        sys.exit(1)


@click.command(cls=get_command_usage("staking"))
@click.option('-d', '--address', help='wallet address or wallet name xxxx.json.')
@click.option('-f', '--file', help='The file is save params.')
@click.option('-c', '--config', default="",
              help='The configuration file specifying the IP and port of the '
                   'transaction to be sent. If it is configured in the global configuration network file, IP and prot '
                   'can be obtained by specifying the name in the configuration. If the network configuration is not '
                   'filled in.')
@click.option('-o', '--offline', is_flag=True, default=True,
              help='Offline transaction or offline transaction offline not input is the default '
                   'for online transaction, and a two-dimensional code picture is generated and '
                   'placed on the desktop, providing ATON offline scanning code signature.')
@click.option('-s', '--style', default="", help='This parameter is used to determine the type of file to be signed')
def unStaking(address, file, config, offline, style):
    """
    this is staking submodule unStaking command.
    """
    params = read_json_file(file)
    node_id = params['node_id']
    transaction_cfg = params['transaction_cfg']

    check_node_id(node_id)
    wallet_dir = g_dict_dir_config["wallet_dir"]
    _, private_key, _, _ = verify_password(address, wallet_dir)
    private_key = private_key[2:]

    ppos = get_eth_obj(config, 'ppos')
    try:
        if offline:
            unsigned_tx_dir = g_dict_dir_config["unsigned_tx_dir"]
            check_dir_exits(unsigned_tx_dir)
            unsigned_file_csv_name = "unsigned_staking_unStaking_{}.csv".format(get_time_stamp())
            unsigned_file_path = os.path.join(unsigned_tx_dir, unsigned_file_csv_name)
            data = rlp.encode([rlp.encode(int(1003)), rlp.encode(bytes.fromhex(node_id))])
            params['to_type'] = 'staking'
            transaction_dict = un_sign_data(data, params, ppos, private_key)
            if style == '':
                write_csv(unsigned_file_path, [transaction_dict])
            else:
                unsigned_file_path = unsigned_file_path.replace('csv', 'jpg')
                write_QRCode(transaction_dict, unsigned_file_path)
            cust_print('unsigned_file save to:{}'.format(unsigned_file_path), fg='g')
        else:
            tx_hash = ppos.withdrewStaking(node_id, private_key, transaction_cfg)
            cust_print('withdrewStaking send transfer transaction successful, tx hash:{}.'.format(tx_hash), fg='g')
    except ValueError as e:
        cust_print('unStaking send transfer transaction fail,error info:{}'.format(e),fg='r')
        sys.exit(1)
