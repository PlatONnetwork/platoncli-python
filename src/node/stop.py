
import click
from utility import get_command_usage, g_current_dir, shutdown_node


@click.command(cls=get_command_usage("node"))
def stop():
    """
    this is node submodule stop command.
    """
    confirm = input('Current workspace: {}, continue Y/N? (Y|y/N|n): '.format(g_current_dir))

    if confirm == 'Y' or confirm == 'y':
        shutdown_node()
