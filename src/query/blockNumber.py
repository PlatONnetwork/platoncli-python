import click
from utility import get_command_usage, get_eth_obj, cust_print


@click.command(cls=get_command_usage("query"))
@click.option('-c', '--config', default="",
              help='The configuration file specifying the IP and port of the '
                   'transaction to be sent. If it is configured in the global configuration network file, IP and prot '
                   'can be obtained by specifying the name in the configuration. If the network configuration is not '
                   'filled in.')
def blockNumber(config):
    """
    this is query submodule get blockNumber command.
    """
    platon = get_eth_obj(config)
    block_number = platon.blockNumber
    cust_print('{}'.format(block_number), fg='g')
