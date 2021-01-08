import click
import sys
import json
from utility import get_command_usage, get_eth_obj, cust_print


@click.command(cls=get_command_usage("hedge"))
@click.option('-a', '--address', required=True, help="Release locked position to account address,only account address")
@click.option('-c', '--config', default="",
              help='The configuration file specifying the IP and port of the '
                   'transaction to be sent. If it is configured in the global configuration network file, IP and prot '
                   'can be obtained by specifying the name in the configuration. If the network configuration is not '
                   'filled in.')
@click.option('-f', '--fromaddress', default="", help="fromaddress")
def GetRestrictingInfo(address, config, fromaddress):
    """
    this is hedge submodule GetRestrictingInfo command.
    """
    try:
        fromaddress = None if fromaddress.replace(" ", "") == "" else fromaddress
        ppos = get_eth_obj(config, 'ppos')
        result = ppos.getRestrictingInfo(address, fromaddress)
        cust_print('{}'.format(json.dumps(result['Ret'], indent=2)), fg='g')
    except Exception as e:
        cust_print('hedge GetRestrictingInfo exception,error info:{}'.format(e), fg='r')
        sys.exit(1)
