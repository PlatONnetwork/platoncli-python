import click
import os
import rlp
import sys
from utility import get_command_usage, cust_print, g_dict_dir_config, get_eth_obj, write_csv, \
    write_QRCode, get_time_stamp
from common import verify_password, un_sign_data, check_dir_exits


@click.command(cls=get_command_usage("delegate"))
@click.option('-d', '--address', required=True, default="", help='Send the transaction address or name.json')
@click.option('-o', '--offline', is_flag=True, default=False,
              help='Offline transaction or offline transaction offline not input is the default '
                   'for online transaction, and a two-dimensional code picture is generated and '
                   'placed on the desktop, providing ATON offline scanning code signature.')
@click.option('-c', '--config', default="",
              help='The configuration file specifying the IP and port of the '
                   'transaction to be sent. If it is configured in the global configuration network file, IP and prot '
                   'can be obtained by specifying the name in the configuration. If the network configuration is not '
                   'filled in.')
@click.option('-s', '--style', default="", help='This parameter is used to determine the type of file to be signed')
def withdrawDelegateReward(address, offline, config, style):
    """
    this is delegate submodule withdrawDelegateReward command.
    """
    wallet_dir = g_dict_dir_config["wallet_dir"]
    wallet_file_path, private_key, hrp, _ = verify_password(address, wallet_dir)

    ppos = get_eth_obj(config, 'ppos')
    _params = {'pri_key': private_key[2:], 'transaction_cfg': None}
    try:
        if offline:
            data = rlp.encode([rlp.encode(int(5000))])
            _params['to_type'] = 'delegateReward'
            transaction_dict = un_sign_data(data, _params, ppos, _params['pri_key'])
            unsigned_tx_dir = g_dict_dir_config["unsigned_tx_dir"]
            check_dir_exits(unsigned_tx_dir)
            unsigned_file_csv_name = "unsigned_delegate_withdrawDelegateReward_{}.csv".format(get_time_stamp())
            unsigned_file_path = os.path.join(unsigned_tx_dir, unsigned_file_csv_name)
            if style == '':
                write_csv(unsigned_file_path, [transaction_dict])
            else:
                unsigned_file_path = unsigned_file_path.replace('csv', 'jpg')
                write_QRCode(transaction_dict, unsigned_file_path)
        else:
            tx_result = ppos.withdrawDelegateReward(*_params.values())
            cust_print('delegate withdrawDelegateReward send transfer transaction successful, tx result:{}.'.format(tx_result),fg='g')
    except ValueError as e:
        cust_print('delegate withdrawDelegateReward send transfer transaction fail,error info:{}'.format(e), fg='r')
        sys.exit(1)
