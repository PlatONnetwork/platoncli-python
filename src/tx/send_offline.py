import os
import sys
import ast
import click
from utility import get_command_usage, g_dict_dir_config, cust_print, send_transaction, get_eth_obj


@click.command(cls=get_command_usage("tx"))
@click.option('-d', '--data', required=True, help='The transaction signature data.')
@click.option('-c', '--config', default="",
              help='The configuration file specifying the IP and port of the '
                   'transaction to be sent. If it is configured in the global configuration network file, IP and prot '
                   'can be obtained by specifying the name in the configuration. If the network configuration is not '
                   'filled in.')
def send_offline(data, config):
    """
    this is tx submodule send_offline command.
    """
    signed_tx_dir = g_dict_dir_config["signed_tx_dir"]
    abspath = os.path.join(signed_tx_dir, data)
    if not os.path.isfile(abspath):
        cust_print('{} not exists,please check!'.format(abspath), fg='r')
        sys.exit(1)
    try:
        with open(abspath, 'r') as f:
            result = f.read()
            sign_data = ast.literal_eval(result)
    except:
        cust_print('analytical exception,please check!', fg='r')
        sys.exit(1)

    try:
        # 发送交易
        platon = get_eth_obj(config)
        tx_hash_list = []
        for data in sign_data:
            txhash, _ = send_transaction(platon, data)
            tx_hash_list.append(txhash)
        txhash = ','.join(tx_hash_list)
    except Exception as e:
        cust_print('send raw transfer transaction failure, error message:{}!!!'.format(e), fg='r')
        sys.exit(1)
    else:
        dir_name = os.path.dirname(abspath)
        base_name = os.path.basename(abspath)
        new_base_name = base_name + '.done'
        os.rename(abspath, os.path.join(dir_name, new_base_name))
        cust_print('send raw transfer transaction successful, tx hash:{}.'.format(txhash), fg='g')
        cust_print('send raw transfer transaction successful, {} to {}'.format(base_name, new_base_name), fg='g')
