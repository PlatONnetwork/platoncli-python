import os
import sys
import shutil
import click

from utility import get_command_usage, cust_print, PLATON_NAME, g_dict_dir_config, \
    get_local_platon_cfg, g_current_dir, get_pid, shutdown_node, remove, startup_node


def update_for_platon(bin_path):
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
            cust_print('Failed to upgrade platon node!:{}'.format(g_current_dir), fg='r')
            return

    # 开始下载，替换
    # download_file(download_path, g_dict_dir_config["platon_dir"])

    # 已下载到本地，直接替换
    old_bin_dir = os.path.join(g_dict_dir_config["platon_dir"], PLATON_NAME)
    remove(old_bin_dir)
    shutil.move(bin_path, g_dict_dir_config["platon_dir"])
    # 重启节点
    startup_node()


@click.command(cls=get_command_usage("node"))
@click.option('-p', '--path', 'bin_path', required=True,
              help='Download the corresponding PlatON client file path.')
def upgrade(bin_path):
    """
    this is node submodule upgrade command.
    """
    update_for_platon(bin_path)
