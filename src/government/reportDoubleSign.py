import click
import os
import rlp
import sys
from utility import get_command_usage, cust_print, read_json_file, g_dict_dir_config, get_eth_obj, write_csv, \
    write_QRCode, get_time_stamp
from common import verify_password, un_sign_data, check_dir_exits


@click.command(cls=get_command_usage("government"))
@click.option('-p', '--param', required=True, default="", help='The transaction parameter json string, or the '
                                                               'transaction parameter json file path.')
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
def reportDoubleSign(param, address, offline, config, style):
    """
    this is government submodule reportDoubleSign command.
    """
    if not os.path.isfile(param):
        cust_print('file {} not exits! please check!'.format(param), fg='r')
        sys.exit(1)
    params = read_json_file(param)
    wallet_dir = g_dict_dir_config["wallet_dir"]
    _, private_key, _, _ = verify_password(address, wallet_dir)
    ppos = get_eth_obj(config, 'ppos')
    try:
        _params = {'typ': params['type'], 'data': params['data']}
    except KeyError as e:
        cust_print('reportDoubleSign need params {},but it does not exist,please check!'.format(e), fg='r')
        sys.exit(1)
    try:
        if offline:
            data = rlp.encode([rlp.encode(int(3000)), rlp.encode(params['type']), rlp.encode(params['data'])])
            _params['transaction_cfg'] = params.get('transaction_cfg', None)
            _params['to_type'] = 'penalty'
            transaction_dict = un_sign_data(data, _params, ppos, private_key[2:])
            unsigned_tx_dir = g_dict_dir_config["unsigned_tx_dir"]
            check_dir_exits(unsigned_tx_dir)
            unsigned_file_csv_name = "unsigned_government_reportDoubleSign_{}.csv".format(get_time_stamp())
            unsigned_file_path = os.path.join(unsigned_tx_dir, unsigned_file_csv_name)
            if style == '':
                write_csv(unsigned_file_path, [transaction_dict])
            else:
                unsigned_file_path = unsigned_file_path.replace('csv', 'jpg')
                write_QRCode(transaction_dict, unsigned_file_path)
            cust_print('unsigned_file save to:{}'.format(unsigned_file_path), fg='g')
        else:
            _params['pri_key'] = private_key[2:]
            _params['transaction_cfg'] = params.get('transaction_cfg', None)
            txhash = ppos.reportDuplicateSign(*_params.values())
            cust_print('send raw transfer transaction successful, tx hash:{}.'.format(txhash), fg='g')
    except Exception as e:
        cust_print('government send transfer transaction fail,error info:{}'.format(e), fg='r')
        sys.exit(1)
