import click

from utility import get_command_usage, startup_node


@click.command(cls=get_command_usage("node"))
def start():
    """
    启动节点命令.
    """
    startup_node()
