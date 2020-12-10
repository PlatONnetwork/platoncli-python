import os

import click

from utility import get_command_usage, cust_print, generate_blskey, get_local_platon_cfg, g_dict_dir_config


@click.command(cls=get_command_usage("node"))
@click.option('-p', '--path', 'keyPath', required=True,
              help='Generates blskey to the specified directory.')
def generateBlsKey(keyPath):
    """
    this is node submodule generateBlsKey command.
    """
    if not os.path.exists(keyPath):
        cust_print("invalid path:{}".format(keyPath), bg='r')
        return

    blskey_path = os.path.join(keyPath, 'blskey')
    blspub_path = os.path.join(keyPath, 'blspub')
    if os.path.exists(blskey_path) or os.path.exists(blspub_path):
        confirm = input('The bls key file already exists in the directory. Do you want to overwrite it? [Y|y/N|n]: ')
        if confirm != 'Y' and confirm != 'y':
            cust_print('Generate bls key fail!', fg='r')
            return

    platon_cfg_path = os.path.join(g_dict_dir_config["conf_dir"], 'platon.cfg')
    hrp = 'lat'
    if os.path.exists(platon_cfg_path):
        platon_cfg = get_local_platon_cfg()
        hrp = platon_cfg['hrp']

    if generate_blskey(keyPath, hrp):
        cust_print('Generate bls key success{}.'.format(keyPath), fg='g')
    else:
        cust_print('Generate bls key failed!', fg='r')
