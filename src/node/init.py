import click

from utility import get_command_usage, cust_print, init_node


@click.command(cls=get_command_usage("node"))
@click.option('-h', '--hrp', 'hrp', required=True, default='lat',
              type=click.Choice(['atp', 'atx', 'lat', 'lax']),
              help='Address prefix, \'atp/atx\' Are the main network and test network addresses of Alaya network '
                   'respectively; '
                   '\'lat/lax\' Are the primary and test network addresses of PlatON network respectively.')
@click.option('-p', '--private_chain', default=False, help='是否是搭建私链.')
@click.option('-c', '--config', default="", help="genesis block config.")
def init(hrp, private_chain, config):
    """
    this is node submodule init command.
    """

    cust_print("Start initializing nodes.", fg='g')
    init_node(hrp, private_chain, config)
