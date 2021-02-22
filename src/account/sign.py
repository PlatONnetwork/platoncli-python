import csv
import os
import sys
import ast
import click
from utility import g_dict_dir_config, cust_print, get_command_usage, sign_one_transaction_by_prikey, get_time_stamp
from common import verify_password, check_dir_exits


def read_file(data_file):
    """
    :param data_file: xxxxxx.csv or xxxx.jpg
    :return:
    """
    unsigned_tx_dir = g_dict_dir_config["unsigned_tx_dir"]
    # unsigned_tx_dir = r'D:\project\platoncli\unsigned_transaction'
    abspath = os.path.join(unsigned_tx_dir, data_file)
    if not os.path.isfile(abspath):
        cust_print('No {} file found in the {} directory please check!'.format(data_file, unsigned_tx_dir), fg='r')
        sys.exit(1)
    result = []
    _, suffix = os.path.splitext(data_file)
    if suffix == '.csv':
        with open(abspath, 'r') as f:
            reader = csv.DictReader(f)
            for v in reader:
                if v.get('value', None):
                    v['value'] = int(ast.literal_eval(v['value']))
                if v.get('data', None):
                    v['data'] = ast.literal_eval(v['data'])
                result.append(dict(v))
    else:
        cust_print('{} illegal,please check!suffix is:{}'.format(data_file, suffix), fg='r')
        sys.exit(1)
    if len(result) == 0:
        cust_print('{} class content is empty,please check!'.format(data_file), fg='r')
        sys.exit(1)
    return result


# read_csv_file('unsigned_transfer_tx_20201221104038.csv')
@click.command(cls=get_command_usage("account"))
@click.option('-d', '--data', required=True, help='example xxxxx.csv or xxxxx.jpg')
@click.option('-a', '--address', required=True, help='Change password by wallet address or name')
def sign(data, address):
    """
    this is account submodule offline sign command.
    """
    wait_sign_data = read_file(data)
    wallet_dir = g_dict_dir_config["wallet_dir"]
    wallet_file_path, private_key, hrp, account = verify_password(address, wallet_dir)

    sign_data = []
    for _wait_sign_data in wait_sign_data:
        rawTransaction, _ = sign_one_transaction_by_prikey(account, None, _wait_sign_data, hrp, private_key)
        sign_data.append(rawTransaction)
    signed_tx_dir = g_dict_dir_config["signed_tx_dir"]
    check_dir_exits(signed_tx_dir)
    name = 'signed_transfer_tx_{}.txt'.format(get_time_stamp())
    abspath = os.path.join(signed_tx_dir, name)
    with open(abspath, 'w', encoding='utf-8') as f:
        f.write(str(sign_data))
    cust_print('sign successful!', fg='g')
    cust_print('sign after data save to {}'.format(abspath), fg='g')
