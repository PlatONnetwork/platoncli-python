import click
from utility import get_command_usage, cust_print, get_eth_obj


@click.command(cls=get_command_usage("query"))
@click.option('-c', '--config', default="",
              help='The configuration file specifying the IP and port of the '
                   'transaction to be sent. If it is configured in the global configuration network file, IP and prot '
                   'can be obtained by specifying the name in the configuration. If the network configuration is not '
                   'filled in.')
def getPackageReward(config):
    """
    this is query submodule get Package Reward command.
    """
    ppos = get_eth_obj(config, 'ppos')
    package_reward = ppos.getPackageReward()
    result = '{} {}'.format(ppos.w3.fromWei(package_reward['Ret'], "ether"), ppos.hrp.upper())
    cust_print('Block rewards for the current settlement cycle:{}'.format(result), fg='g')
