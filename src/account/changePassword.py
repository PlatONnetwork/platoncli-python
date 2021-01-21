import json
import click
import os
import crypto
from utility import get_command_usage, g_dict_dir_config, cust_print, get_time_stamp
from common import verify_password, confirm_password


@click.command(cls=get_command_usage("account"))
@click.option('-d', '--address', required=True, help='Change password by wallet address or name')
def changePassword(address):
    """
        this is account submodule change password command.
        """
    wallet_dir = g_dict_dir_config["wallet_dir"]
    cust_print("Start change wallet password...", fg='g')

    wallet_file_path, private_key, hrp, _ = verify_password(address, wallet_dir)  # verify old password
    new_password = confirm_password()  # confirm new password
    print('private_key:{}'.format(private_key))
    private_key_obj = crypto.PrivateKey.from_hex(private_key[2:])
    keystores = private_key_obj.to_keyfile_json(new_password, hrp)
    public_key = private_key_obj.public_key.to_hex()
    public_address = private_key_obj.public_key.address(hrp)

    old_wallet_name = os.path.basename(wallet_file_path).split('.')[0]
    new_wallet_name = '{old_name}_{timestamp}.json'.format(old_name=old_wallet_name, timestamp=get_time_stamp())
    if not os.path.exists(wallet_dir):
        os.makedirs(wallet_dir)
    new_wallet_path = os.path.join(wallet_dir, new_wallet_name)
    with open(new_wallet_path, 'w') as f:
        json.dump(keystores, f)

    verify_password(new_wallet_name, wallet_dir, new_password)  # verify new password is change successful
    os.remove(wallet_file_path)

    cust_print("Congratulations on your successful password modification,old wallet {} already delete!".format(
        new_wallet_name), fg='g')
    cust_print("New WalletName:{}".format(new_wallet_name), fg='g')
    cust_print("PublicKey:{}".format(public_key), fg='g')
    cust_print("Addresss:{}".format(public_address), fg='g')
    cust_print("Path:{}".format(new_wallet_path), fg='g')
