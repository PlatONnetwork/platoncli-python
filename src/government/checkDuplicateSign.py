import click
import sys
from utility import get_command_usage, get_eth_obj, cust_print


@click.command(cls=get_command_usage("government"))
@click.option('-t', '--type', required=True,
              type=click.Choice(['1', '2', '3']), help="Double sign type")
@click.option('-n', '--nodeid', required=True, help="node id")
@click.option('-b', '--blocknumber', required=True, help="block number")
@click.option('-c', '--config', default="",
              help='The configuration file specifying the IP and port of the '
                   'transaction to be sent. If it is configured in the global configuration network file, IP and prot '
                   'can be obtained by specifying the name in the configuration. If the network configuration is not '
                   'filled in.')
@click.option('-f', '--fromaddress', default="", help="fromaddress")
def checkDuplicateSign(type, nodeid, blocknumber, config, fromaddress):
    """
    this is government submodule checkDuplicateSign command.
    """
    try:
        fromaddress = None if fromaddress.replace(" ", "") == "" else fromaddress
        ppos = get_eth_obj(config, 'ppos')
        result = ppos.checkDuplicateSign(int(type), nodeid, blocknumber, fromaddress)
        cust_print('{}'.format(result), fg='g')
    except Exception as e:
        cust_print('government checkDuplicateSign exception,error info:{}'.format(e), fg='r')
        sys.exit(1)
