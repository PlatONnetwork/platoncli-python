import click
import json
import sys
from utility import get_command_usage, cust_print, get_eth_obj

query_list = ['getVerifierList', 'getValidatorList', 'getCandidateList', 'getStakingReward', 'getCandidateInfo']


@click.command(cls=get_command_usage("query"))
@click.option('-f', '--function', type=click.Choice(query_list), required=True,
              help="getVerifierList/getValidatorList/getCandidateList/getStakingReward/getCandidateInfo")
@click.option('-n', '--nodeid', default="", help="The node id of the node to be queried")
@click.option('-c', '--config', default="",
              help='The configuration file specifying the IP and port of the '
                   'transaction to be sent. If it is configured in the global configuration network file, IP and prot '
                   'can be obtained by specifying the name in the configuration. If the network configuration is not '
                   'filled in.')
@click.option('-d', '--fromaddress', default="", help="fromaddress")
def query(function, nodeid, config, fromaddress):
    """
    this is staking submodule query command.
    """
    fromaddress = None if fromaddress.replace(" ", "") == "" else fromaddress
    ppos = get_eth_obj(config, 'ppos')
    try:
        if function == 'getCandidateInfo':
            info = getattr(ppos, function)(nodeid, fromaddress)
            cust_print('node info:\n{}'.format(json.dumps(info['Ret'], indent=2)), fg='g')
        elif function == 'getStakingReward':
            reward = ppos.w3.fromWei(getattr(ppos, function)()['Ret'], "ether")
            cust_print('Pledge rewards for the current settlement cycle is:{}'.format(reward), fg='g')
        else:
            for obj in getattr(ppos, function)(fromaddress)['Ret']:
                cust_print('{}'.format(json.dumps(obj, indent=2)), fg='g')
    except Exception as e:
        cust_print('Query exception,{}'.format(e), fg='r')
        sys.exit(1)
