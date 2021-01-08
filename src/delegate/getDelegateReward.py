import click
import os
import json
import sys
from utility import get_command_usage, cust_print, read_json_file, get_eth_obj


@click.command(cls=get_command_usage("delegate"))
@click.option('-p', '--param', required=True, default="", help='The transaction parameter json string, or the '
                                                               'transaction parameter json file path.')
@click.option('-c', '--config', default="",
              help='The configuration file specifying the IP and port of the '
                   'transaction to be sent. If it is configured in the global configuration network file, IP and prot '
                   'can be obtained by specifying the name in the configuration. If the network configuration is not '
                   'filled in.')
def getDelegateReward(param, config):
    """
    this is delegate submodule getDelegateReward command.
    """
    ppos = get_eth_obj(config, 'ppos')
    if not os.path.isfile(param):
        cust_print('file {} not exits! please check!'.format(param), fg='r')
        sys.exit(1)
    params = read_json_file(param)

    _params = {}
    try:
        _params['address'] = params['address']
        _params['node_ids'] = params['nodeIDs']
    except KeyError as e:
        cust_print('Key {} does not exist in file {},please check!'.format(e, params), fg='r')
        sys.exit(1)
    try:
        receive = ppos.getDelegateReward(*_params.values())
        for node in receive['Ret']:
            cust_print('{}'.format(json.dumps(node, indent=2)), fg='g')
    except ValueError as e:
        cust_print('delegate getDelegateReward send transfer transaction fail,error info:{}'.format(e), fg='r')
        sys.exit(1)
