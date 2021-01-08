import click
from utility import get_command_usage, cust_print, get_eth_obj


@click.command(cls=get_command_usage("query"))
@click.option('-c', '--config', default="",
              help='The configuration file specifying the IP and port of the '
                   'transaction to be sent. If it is configured in the global configuration network file, IP and prot '
                   'can be obtained by specifying the name in the configuration. If the network configuration is not '
                   'filled in.')
def getAvgPackTime(config):
    """
    this is query submodule getAvgPackTime command.
    """
    ppos = get_eth_obj(config, 'ppos')
    average_time = ppos.getAvgPackTime()
    cust_print('Average time for block packaging:{}s'.format(average_time['Ret'] / 1000), fg='g')
