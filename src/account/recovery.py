import click
import sys
import crypto
import json
import os
from utility import get_command_usage, g_dict_dir_config, g_system, input_passwd_for_linux, input_passwd_for_win, \
    cust_print, get_time_stamp


@click.command(cls=get_command_usage("account"))
@click.option('-t', '--types', required=True, type=click.Choice(['mnemonic', 'private']),
              help='By mnemonic or private key')
def recovery(types):
    """
    this is account submodule recovery wallet command.
    """
    message = 'Private key:' if types == 'private' else 'Mnemonic code:'
    if 'windows' == g_system:
        mp = b''.join(input_passwd_for_win(message)).decode()
        password = b''.join(input_passwd_for_win()).decode()
    else:
        mp = input_passwd_for_linux(message)
        password = input_passwd_for_linux()
    if types == 'private':
        check_private_key = mp[2:] if mp.startswith('0x') else mp
        try:
            private_key_obj = crypto.PrivateKey.from_hex(check_private_key)
            keystores = private_key_obj.to_keyfile_json(password)
        except Exception as e:
            cust_print('Incorrect private key or password recovery failed!,exception info:{}'.format(e), fg='r')
            sys.exit(1)
        recovery_path = g_dict_dir_config['wallet_recovery_dir']
        if not os.path.exists(recovery_path):
            os.makedirs(recovery_path)
        wallet_name = 'recovery_wallet_{}.json'.format(get_time_stamp())
        wallet_path = os.path.join(recovery_path, wallet_name)
        with open(wallet_path, 'w') as f:
            json.dump(keystores, f)
        cust_print('recovery successful!', fg='g')
        cust_print('recovery to {}.'.format(wallet_path), fg='g')
    else:
        # Todo
        pass
