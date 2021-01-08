import click
import json
import sys
from utility import get_command_usage, cust_print, get_eth_obj


@click.command(cls=get_command_usage("delegate"))
@click.option('-d', '--address', required=True, help='The height of the block when the pledge is initiated')
@click.option('-c', '--config', default="",
              help='The configuration file specifying the IP and port of the '
                   'transaction to be sent. If it is configured in the global configuration network file, IP and prot '
                   'can be obtained by specifying the name in the configuration. If the network configuration is not '
                   'filled in.')
@click.option('-f', '--fromaddress', default="", help="fromaddress")
def getRelatedListByDelAddress(address, config, fromaddress):
    """
    this is delegate submodule getRelatedListByDelAddr command.
    """
    try:
        ppos = get_eth_obj(config, 'ppos')
        fromaddress = None if fromaddress.replace(" ", "") == "" else fromaddress
        result = ppos.getRelatedListByDelAddr(address, fromaddress)
        for obj in result['Ret']:
            cust_print('{}'.format(json.dumps(obj, indent=2)), fg='g')
    except Exception as e:
        cust_print('Query exception,{}'.format(e), fg='r')
        sys.exit(1)
