import os
import shutil
import sys

import click

from utility import get_command_usage, cust_print, shutdown_node, PLATON_NAME, \
    get_pid, remove, g_dict_dir_config, get_local_platon_cfg, g_current_dir, startup_node


def rollback_for_platon(dataPath):
    platon_cfg_path = os.path.join(g_dict_dir_config["conf_dir"], 'platon.cfg')
    if not os.path.exists(platon_cfg_path):
        cust_print('The node is not initialized, please check!:{}'.format(g_current_dir), fg='r')
        sys.exit(1)

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
            cust_print('Failed to rollback platon data!:{}'.format(g_current_dir), fg='r')
            return

    confirm = input('Current CLI workspace directory:{},  do you want to continue? [Y|y/N|n]: '.
                    format(g_current_dir))
    # 关闭进程
    if confirm != 'Y' and confirm != 'y':
        cust_print('Failed to rollback platon data!:{}'.format(g_current_dir), fg='r')
        return

    cust_print('start to rollback node data...：{}'.format(g_current_dir), fg='g')
    # delete data dir of platon
    old_data_dir = os.path.join(g_dict_dir_config["platon_dir"], "data")
    remove(old_data_dir)
    shutil.move(dataPath, old_data_dir)

    # 重启节点
    startup_node()
    cust_print("Rollback success...", bg='y')


@click.command(cls=get_command_usage("node"))
@click.option('-p', '--path', 'dataPath', required=True,
              help='Download the path to the block data after the rollback.')
def rollback(dataPath):
    """
    this is node submodule rollback command.
    """
    rollback_for_platon(dataPath)
