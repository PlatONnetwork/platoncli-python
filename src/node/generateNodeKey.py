import os

import click

from utility import get_command_usage, cust_print, generate_nodekey, g_dict_dir_config, get_local_platon_cfg


@click.command(cls=get_command_usage("node"))
@click.option('-p', '--path', 'keyPath', required=True,
              help='Generates nodeKey to the specified directory.')
def generateNodeKey(keyPath):
    """
    this is node submodule generateNodeKey command.
    """
    if not os.path.exists(keyPath):
        cust_print("invalid path:{}".format(keyPath), bg='r')
        return

    nodeIdPath = os.path.join(keyPath, 'nodeid')
    nodeKeyPath = os.path.join(keyPath, 'nodekey')

    if os.path.exists(nodeIdPath) or os.path.exists(nodeKeyPath):
        confirm = input('The key file already exists in the directory. Do you want to overwrite it? [Y|y/N|n]: ')
        if confirm != 'Y' and confirm != 'y':
            cust_print('Generate node key fail!', fg='r')
            return

    platon_cfg_path = os.path.join(g_dict_dir_config["conf_dir"], 'platon.cfg')
    hrp = 'lat'
    if os.path.exists(platon_cfg_path):
        platon_cfg = get_local_platon_cfg()
        hrp = platon_cfg['hrp']
    if generate_nodekey(keyPath, hrp):
        cust_print('Generate node key success:{}.'.format(keyPath), fg='y')
    else:
        cust_print('Generate node key fail!', fg='r')
