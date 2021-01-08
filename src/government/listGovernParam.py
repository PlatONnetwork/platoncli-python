import click
import sys
import json
from utility import get_command_usage, get_eth_obj, cust_print


@click.command(cls=get_command_usage("government"))
@click.option('-m', '--module', default=None, help="params module")
@click.option('-c', '--config', default="",
              help='The configuration file specifying the IP and port of the '
                   'transaction to be sent. If it is configured in the global configuration network file, IP and prot '
                   'can be obtained by specifying the name in the configuration. If the network configuration is not '
                   'filled in.')
@click.option('-f', '--fromaddress', default="", help="fromaddress")
def listGovernParam(module, config, fromaddress):
    """
    this is government submodule listGovernParam command.
    """
    try:
        fromaddress = None if fromaddress.replace(" ", "") == "" else fromaddress
        pip = get_eth_obj(config, 'pip')
        result = pip.listGovernParam(module, fromaddress)
        for obj in result['Ret']:
            cust_print('{}'.format(json.dumps(obj, indent=2)), fg='g')
    except Exception as e:
        cust_print('government listGovernParam exception,error info:{}'.format(e), fg='r')
        sys.exit(1)
