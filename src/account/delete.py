import sys
import os
import click
from common import verify_password
from utility import get_command_usage, g_dict_dir_config, cust_print


@click.command(cls=get_command_usage("account"))
@click.option('-d', '--address', required=True,
              help='Specify a wallet name query or specify an address query and delete wallet.')
def delete(address):
    """
    this is account submodule delete command.
    """
    wallet_dir = g_dict_dir_config["wallet_dir"]
    cust_print("Start delete wallet file...", fg='g')
    wallet_file_path, _, _, _ = verify_password(address, wallet_dir)
    try:
        os.remove(wallet_file_path)
    except:
        cust_print('delete wallet {} fail!!!'.format(wallet_file_path), fg='r')
        sys.exit(1)
