import os

import click
from utility import get_command_usage, cust_print, get_pid, PLATON_NAME, shutdown_node, \
    make_zip, get_time_stamp, g_dict_dir_config, get_local_platon_cfg, g_current_dir


@click.command(cls=get_command_usage("node"))
@click.option('-p', '--path', 'savePath', required=True,
              help='Specifies the export block data path.')
def blockexport(savePath):
    """
    this is node submodule blockexport command.
    """
    if not os.path.exists(savePath):
        cust_print("invalid path: {}".format(savePath), fg='r')
        return

    # 节点数据
    data_dir = os.path.join(g_dict_dir_config["platon_dir"], "data")
    if not os.path.exists(data_dir):
        cust_print("Data file not found: {}".format(data_dir), fg='r')
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
            cust_print('Failed to export block data!:{}'.format(g_current_dir), fg='r')
            return

    cust_print('Start exporting the block data.', fg='g')
    # make zip
    zip_name = "data_" + get_time_stamp() + ".zip"
    zip_path = os.path.join(savePath, zip_name)
    make_zip(data_dir, zip_path)

    cust_print('Export block data successfully.', fg='g')
