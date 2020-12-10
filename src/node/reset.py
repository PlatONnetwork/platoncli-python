import os
import sys

import click

from utility import get_command_usage, check_install_valid, cust_print, \
    g_current_dir, shutdown_node, startup_node, g_dict_dir_config, get_local_platon_cfg, get_pid, PLATON_NAME, remove


def reset_node(clearFlag):
    platon_cfg_path = os.path.join(g_dict_dir_config["conf_dir"], 'platon.cfg')
    if not os.path.exists(platon_cfg_path):
        cust_print('The node is not initialized, please check!:{}'.format(g_current_dir), fg='r')
        sys.exit(1)

    platon_cfg = get_local_platon_cfg()
    hrp = platon_cfg['hrp']
    network_type = "PlatON"
    if 'atp' == hrp or 'atx':
        network_type = "Alaya"
    # 判断是否已安装
    if not check_install_valid(network_type):
        cust_print('Node binary not installed, please check!:{}'.format(g_current_dir), fg='r')
        sys.exit(1)

    # 进程是否在运行
    pid = get_pid(PLATON_NAME, int(platon_cfg['rpcport']))
    if pid:
        confirm = input('PlatON is running, rpc port:{}, Whether or not to continue? [Y|y/N|n]: '.
                        format(int(platon_cfg['rpcport'])))
        # 关闭进程
        if confirm == 'Y' or confirm == 'y':
            shutdown_node()
        else:
            cust_print('Failed to reset platon node!:{}'.format(g_current_dir), fg='r')
            return

    # 再次提示
    confirm = input('Whether to consider data backup? [Y|y/N|n]: ')
    if confirm == 'Y' or confirm == 'y':
        cust_print('Please do a manual backup of the data you need.', fg='g')
        return

    # 删除data数据
    data_path = os.path.join(g_dict_dir_config["platon_dir"], "data")
    if os.path.exists(data_path):
        remove(data_path)
        cust_print('The data directory was deleted successfully:{}.'.format(data_path), fg='g')

    if clearFlag:
        # 删除key数据
        nodeKey_path = g_dict_dir_config["nodekey_dir"]
        blsKey_path = g_dict_dir_config["blskey_dir"]
        if os.path.exists(nodeKey_path):
            remove(nodeKey_path)
            cust_print('The nodekey directory was deleted successfully:{}.'.format(nodeKey_path), fg='g')

        if os.path.exists(blsKey_path):
            remove(blsKey_path)
            cust_print('The blskey directory was deleted successfully:{}.'.format(blsKey_path), fg='g')

        # 删除log日志
        log_path = platon_cfg['logfile']
        if os.path.exists(log_path):
            remove(log_path)
            cust_print('The log file was deleted successfully:{}.'.format(log_path), fg='g')
    try:
        cust_print('Reset platon node successfully.', fg='g')
    except Exception as e:
        cust_print('Unable to reset platon node: {}'.format(e), fg='r')

    # 需要重新初始化
    # startup_node()


@click.command(cls=get_command_usage("node"))
@click.option('-c', '--clear', 'clearFlag', is_flag=True,
              help='Fill in this parameter to clear all data from the node')
def reset(clearFlag):
    """
    this is node submodule reset command.
    """
    reset_node(clearFlag)
