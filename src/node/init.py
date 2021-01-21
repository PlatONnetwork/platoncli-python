import click

from utility import get_command_usage, cust_print, init_node


@click.command(cls=get_command_usage("node"))
@click.option('-h', '--hrp', required=True, default='lat', help='this is params is net type')
@click.option('-p', '--private_chain', is_flag=True, default=False, help='是否是搭建私链.')
@click.option('-c', '--config', default="", help="genesis block config.")
def init(hrp, private_chain, config):
    """
    this is node submodule init command.
    """
    cust_print("Start initializing nodes.", fg='g')
    init_node(hrp, private_chain, config)
