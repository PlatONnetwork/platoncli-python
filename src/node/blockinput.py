import os

import click
from utility import get_command_usage, cust_print, remove, shutdown_node, un_zip, g_dict_dir_config, \
    get_local_platon_cfg, get_pid, PLATON_NAME, g_current_dir


@click.command(cls=get_command_usage("node"))
@click.option('-p', '--path', 'zipFile', required=True,
              help='Specifies the path to import the block data.')
def blockinput(zipFile):
    """
    this is node submodule blockinput command.
    """
    if not os.path.exists(zipFile) or not zipFile.endswith(".zip"):
        cust_print("Invalid address, please enter zip file path: {}".format(zipFile), fg='r')
        return

    platon_cfg = get_local_platon_cfg()
    # 进程是否在运行
    pid = get_pid(PLATON_NAME, int(platon_cfg['rpcport']))
    if pid:
        confirm = input('PlatON is running, rpc port:{}, Whether or not to continue? [Y|y/N|n]: '.
                        format(int(platon_cfg['rpcport'])))
        # 关闭进程
        if confirm == 'Y' or confirm == 'y':
            shutdown_node()
        else:
            cust_print('Failed to input block data!:{}'.format(g_current_dir), fg='r')
            return

    # node is deploy
    data_dir = os.path.join(g_dict_dir_config["platon_dir"], "data")
    if os.path.exists(data_dir):
        # delete old chain data
        cust_print("start to remove old chain data: {}.".format(data_dir), fg='g')
        remove(data_dir)
        cust_print("remove old chain data succeed.", fg='g')

    cust_print('start to input the block data:{}.'.format(zipFile), fg='g')
    # unzip
    un_zip(zipFile, g_dict_dir_config["platon_dir"])

    cust_print('input the block data successfully.', fg='g')
