import click
import json
from utility import get_command_usage, get_eth_obj, cust_print, HexBytes_to_str


@click.command(cls=get_command_usage("query"))
@click.option('-n', '--number', required=True, type=click.INT, help='The block height of the specific query block')
@click.option('-c', '--config', default="",
              help='The configuration file specifying the IP and port of the '
                   'transaction to be sent. If it is configured in the global configuration network file, IP and prot '
                   'can be obtained by specifying the name in the configuration. If the network configuration is not '
                   'filled in.')
def getBlockByNumber(number, config):
    """
    this is query submodule get blockNumber info by number command.
    """
    platon = get_eth_obj(config)
    block_info = dict(platon.getBlock(number))
    HexBytes_to_str(block_info)
    cust_print('{}'.format(json.dumps(block_info, indent=2)), fg='g')
