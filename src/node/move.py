import os
import shutil

import click
from utility import get_command_usage, cust_print, remove, shutdown_node, un_zip, get_local_platon_cfg, get_pid, \
    PLATON_NAME


def is_continue(platon_cfg, running_dir):
    # 进程是否在运行
    pid = get_pid(PLATON_NAME, int(platon_cfg['rpcport']))
    if pid:
        confirm = input('PlatON is running, rpc port:{}, Whether or not to continue? [Y|y/N|n]: '.
                        format(int(platon_cfg['rpcport'])))
        # 关闭进程
        if confirm == 'Y' or confirm == 'y':
            shutdown_node()
        else:
            cust_print('Failed to move block data!:{}'.format(running_dir), fg='r')
            return False

    return True


@click.command(cls=get_command_usage("node"))
@click.option('-o', '--original', required=True, help='Original block data directory.')
@click.option('-t', '--target', required=True, help='Migrate the target data directory.')
@click.option('-m', '--movetype', required=True, type=click.Choice(['key', 'data', 'all']),
              help='The migration types,\'key\': Migrate NodeKey and BLsKey, '
                   '\'data\': Migrate block data, '
                   '\'all\': Include key and data.')
def move(original, target, movetype):
    """
    this is node submodule move command.
    """
    if not os.path.exists(original):
        cust_print("invalid original path: {}".format(original), fg='r')
        return

    original_cnf_path = "{}/{}/{}".format(original, 'config', 'platon.cfg')
    org_cnf = get_local_platon_cfg(original_cnf_path)

    if not os.path.exists(target):
        cust_print("invalid target path: {}".format(target), fg='r')
        return

    target_cnf_path = "{}/{}/{}".format(target, 'config', 'platon.cfg')
    tag_cnf = get_local_platon_cfg(target_cnf_path)

    # 源节点
    if not is_continue(org_cnf, original):
        return

    # 目标节点
    if not is_continue(tag_cnf, target):
        return

    if "all" == movetype or "key" == movetype:
        cust_print("Start to migrating nodekey and blskey: {}.".format(original), fg='g')
        for key in ['nodeKey', 'blsKey']:
            key_path = "{}/{}/{}".format(original, "platon", key)
            des_path = "{}/{}/{}".format(target, "platon", key)
            remove(des_path)
            shutil.move(key_path, des_path)

        cust_print('migrating key successfully.', fg='g')

    if "all" == movetype or "data" == movetype:
        cust_print("Start to migrating block data: {}.".format(original), fg='g')
        src_path = os.path.join(original, "data")
        des_path = os.path.join(target, "data")
        remove(des_path)
        shutil.move(src_path, des_path)

        cust_print('migrating block data successfully.', fg='g')
