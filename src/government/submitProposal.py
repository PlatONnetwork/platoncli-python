import click
import os
import rlp
import sys
from utility import get_command_usage, cust_print, read_json_file, g_dict_dir_config, get_eth_obj, write_csv, \
    write_QRCode, get_time_stamp
from common import verify_password, un_sign_data, check_dir_exits

method_module = {'CancelProposal': ('submitCancel', 2005), 'ParamProposal': ('submitParam', 2002),
                 'VersionProposal': ('submitVersion', 2001), 'TextProposal': ('submitText', 2000)}


def rlp_params(func, verifier, pip_id, p1='', p2='', p3=''):
    rlp_list = [rlp.encode(int(func)), rlp.encode(bytes.fromhex(verifier)), rlp.encode(pip_id)]
    if p1 == '':
        # TextProposal
        return rlp.encode(rlp_list)
    if p3 != '':
        # submitParam
        spacial = [rlp.encode(p1), rlp.encode(p2), rlp.encode(p3)]
        return rlp.encode(rlp_list + spacial)
    if p2.isdigit():
        # submitVersion
        spacial = [rlp.encode(int(p1)), rlp.encode(int(p2))]
    else:
        # submitCancel
        spacial = [rlp.encode(int(p1)), rlp.encode(bytes.fromhex(p2))]
    return rlp.encode(rlp_list + spacial)


def check_params(args):
    for arg in args:
        if not args[arg] and arg != 'transaction_cfg':
            cust_print('the value of {} is empty'.format(arg), fg='r')
            sys.exit(1)


@click.command(cls=get_command_usage("government"))
@click.option('-p', '--param', required=True, default="", help='The transaction parameter json string, or the '
                                                               'transaction parameter json file path.')
@click.option('-d', '--address', required=True, default="", help='Send the transaction address or name.json')
@click.option('-o', '--offline', is_flag=True, default=False,
              help='Offline transaction or offline transaction offline not input is the default '
                   'for online transaction, and a two-dimensional code picture is generated and '
                   'placed on the desktop, providing ATON offline scanning code signature.')
@click.option('-m', '--module', required=True, type=click.Choice(list(method_module.keys())), help='Proposal type.')
@click.option('-c', '--config', default="",
              help='The configuration file specifying the IP and port of the '
                   'transaction to be sent. If it is configured in the global configuration network file, IP and prot '
                   'can be obtained by specifying the name in the configuration. If the network configuration is not '
                   'filled in.')
@click.option('-s', '--style', default="", help='This parameter is used to determine the type of file to be signed')
def submitProposal(param, address, offline, module, config, style):
    """
    this is government submodule submitProposal command.
    """
    if not os.path.isfile(param):
        cust_print('file {} not exits! please check!'.format(param), fg='r')
        sys.exit(1)
    params = read_json_file(param)
    check_params(params)

    _params = {'verifier': params['verifier'], 'pip_id': params['pIDID']}
    _module, func = method_module[module]
    try:
        if _module == 'submitVersion':
            _params['new_version'] = params['newVersion']
            _params['end_voting_rounds'] = params['endVotingRound']
        if _module == 'submitCancel':
            _params['end_voting_rounds'] = params['endVotingRound']
            _params['tobe_canceled_proposal_id'] = params['canceledProposalID']
        if _module == 'submitParam':
            _params['module'] = params['module']
            _params['name'] = params['name']
            _params['new_value'] = params['newValue']
    except KeyError as e:
        cust_print('{} need params {},but it does not exist,please check!'.format(module, e), fg='r')
        sys.exit(1)

    wallet_dir = g_dict_dir_config["wallet_dir"]
    _, private_key, _, _ = verify_password(address, wallet_dir)
    pip = get_eth_obj(config, 'pip')
    module, func = method_module[module]
    try:
        if offline:
            data = rlp_params(func, *_params.values())
            _params['transaction_cfg'] = params.get('transaction_cfg', None)
            _params['to_type'] = 'pip'
            transaction_dict = un_sign_data(data, _params, pip, private_key[2:])
            unsigned_tx_dir = g_dict_dir_config["unsigned_tx_dir"]
            check_dir_exits(unsigned_tx_dir)
            unsigned_file_csv_name = "unsigned_submitProposal_{}_{}.csv".format(module, get_time_stamp())
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
            tx_result = getattr(pip, module)(*_params.values())
            cust_print('send raw transfer transaction successful, tx result:{}.'.format(tx_result), fg='g')
    except Exception as e:
        cust_print('submitProposal {} send transfer transaction fail,error info:{}'.format(module, e), fg='r')
        sys.exit(1)
