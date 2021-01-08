import click
import sys
import json
from utility import get_command_usage, get_eth_obj, cust_print, HexBytes_to_str


@click.command(cls=get_command_usage("tx"))
@click.option('-h', '--hash', required=True, help='Transaction hash.')
@click.option('-c', '--config', default="",
              help='The configuration file specifying the IP and port of the '
                   'transaction to be sent. If it is configured in the global configuration network file, IP and prot '
                   'can be obtained by specifying the name in the configuration. If the network configuration is not '
                   'filled in.')
def getTransaction(hash, config):
    """
    this is tx submodule get transaction command.
    """
    platon = get_eth_obj(config)
    try:
        # 交易信息
        transaction = dict(platon.getTransaction(hash))
        HexBytes_to_str(transaction)
        # 交易回执信息
        transaction_receipt = dict(platon.getTransactionReceipt(hash))
        HexBytes_to_str(transaction_receipt)
    except Exception as e:
        cust_print('Failed to query transaction information,error message:{}.'.format(e))
        sys.exit(1)
    cust_print('query transaction information successful!', fg='g')
    info = "transaction:\n"
    info += "{}\n".format(json.dumps(dict(transaction), indent=2))
    info += "\n\ntransaction receipt:\n"
    info += "{}".format(json.dumps(dict(transaction_receipt), indent=2))
    cust_print('{}'.format(info), fg='g')
