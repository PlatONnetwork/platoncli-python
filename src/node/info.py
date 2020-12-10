
import click
from utility import get_command_usage, get_local_platon_cfg, cust_print, PLATON_NAME, get_pid
from precompile_lib import Web3, HTTPProvider, Admin


@click.command(cls=get_command_usage("node"))
def info():
    """
    this is node submodule info command.
    """
    platon_cfg = get_local_platon_cfg()
    pid = get_pid(PLATON_NAME, int(platon_cfg['rpcport']))
    if not pid:
        cust_print("The node is not started, rpc port:{}, please check!...".
                   format(int(platon_cfg['rpcport'])), fg='r')
        return

    url = "http://{}:{}".format(platon_cfg["rpcaddr"], platon_cfg["rpcport"])

    w3 = Web3(HTTPProvider(url))
    # 获取节点信息
    admin = Admin(w3)
    nodeId = admin.nodeInfo.id
    cust_print("NodeId:{}".format(nodeId), fg='g')

    # NodeName
    NodeName = ""
    cust_print("NodeName:{}".format(NodeName), fg='g')

    # BenefitAddress
    BenefitAddress = ""
    cust_print("BenefitAddress:{}".format(BenefitAddress), fg='g')
