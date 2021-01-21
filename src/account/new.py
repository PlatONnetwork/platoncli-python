# _*_ coding:utf-8 _*_
import json
import os
import sys

import click

from precompile_lib import HDPrivateKey, HDKey
from utility import get_command_usage, g_dict_dir_config, cust_print
from common import confirm_password


def batch_generate_wallet(password="", wallet_count=1,
                          wallet_type="ordinary", hrp_type='lat'):
    keystores = {}
    privateKeys = {}
    publicKeys = {}
    address_list = []
    if "ordinary" == wallet_type:
        for i in range(wallet_count):
            # 生成助记
            master_key, mnemonic = HDPrivateKey.master_key_from_entropy()
            # [mnemonic]

            root_keys = HDKey.from_path(master_key, "m/44'/206'/0'")
            acct_priv_key = root_keys[-1]
            # 钱包
            keys = HDKey.from_path(acct_priv_key, '{change}/{index}'.format(change=0, index=0))
            private_key = keys[-1]
            public_address = private_key.public_key.address(hrp_type)
            address_list.append(public_address)

            publicKeys[public_address] = private_key.public_key._key.get_public_key()

            keystores[public_address] = json.dumps(private_key._key.to_keyfile_json(password,hrp_type))
            privateKeys[public_address] = private_key._key.get_private_key()

    return address_list, publicKeys, keystores


@click.command(cls=get_command_usage("account"))
@click.option('-n', '--name', 'wallet_name', default="", help='Wallet file name.')
@click.option('-b', '--batch', type=int, default=1, help='Batch generated wallet number.')
@click.option('-h', '--hrp', required=True, default='lat', help='this is params is net type')
def new(wallet_name, batch, hrp):
    """
    this is account submodule new command.
    """
    wallet_dir = g_dict_dir_config["wallet_dir"]
    if not os.path.exists(wallet_dir):
        os.mkdir(wallet_dir)

    wallet_path = ""
    if "" != wallet_name:
        wallet_path = os.path.join(wallet_dir, "{}.json".format(wallet_name))
        if os.path.exists(wallet_path):
            cust_print("The wallet file already exists：{}, Failed to generate wallet file!".
                       format(wallet_path), fg='r')
            sys.exit(1)

    cust_print("Start generating wallet files...", fg='g')

    passwd1 = confirm_password()

    address_list, publicKeys, keystores = \
        batch_generate_wallet(password=passwd1, wallet_count=batch, hrp_type=hrp)

    if 1 == len(address_list):
        new_address = address_list[0]
        if "" == wallet_path:
            wallet_name = "{}.json".format(new_address)
            wallet_path = os.path.join(wallet_dir, wallet_name)
            if os.path.exists(wallet_path):
                cust_print("The wallet file already exists：{}, Failed to generate wallet file!".
                           format(wallet_path), fg='r')
                sys.exit(1)
        else:
            wallet_name = "{}.json".format(wallet_name)

        with open(wallet_path, 'w') as f:
            f.write(keystores[new_address])

        cust_print("WalletName:{}".format(wallet_name), fg='g')
        cust_print("PublicKey:{}".format(publicKeys[new_address]), fg='g')
        cust_print("Addresss:{}".format(new_address), fg='g')
        cust_print("Path:{}".format(wallet_path), fg='g')

    else:
        cust_print("Path:{}".format(wallet_dir), fg='g')
        index = 1
        for address in address_list:
            wallet_name = "{}.json".format(address)
            wallet_path = os.path.join(wallet_dir, wallet_name)
            with open(wallet_path, 'w') as f:
                f.write(keystores[address])
            cust_print("WalletName:{} ------ {}".format(wallet_name, index), fg='g')
            index = index + 1
