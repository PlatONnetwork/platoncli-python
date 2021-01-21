import click
import sys
import crypto
import json
import os
from utility import get_command_usage, g_dict_dir_config, g_system, input_passwd_for_linux, input_passwd_for_win, \
    cust_print, get_time_stamp


def check_hrp(hrp):
    config = os.path.join(g_dict_dir_config["conf_dir"], "node_config.json")
    try:
        with open(config, 'r') as f:
            config_hrp = json.load(f)['hrp']
    except:
        config_hrp = ''
    config_hrp = config_hrp.lower()
    hrp_list = [config_hrp, hrp]
    result = hrp
    if all(hrp_list):
        if config_hrp != hrp:
            cust_print('HRP in node_config.json is {},the HRP value you specify {}'.format(config_hrp, hrp), fg='g')
            hrp = input('Please confirm which HRP you want to choose, use the one you specify by default[{}]:'.format(hrp))
            result = hrp.replace('', '').lower()
    if any(hrp_list):
        result = hrp if hrp else config_hrp
    else:
        while not hrp:
            hrp = input('Please enter the network type HRP: ')
            result = hrp.replace('', '').lower()
    return result


@click.command(cls=get_command_usage("account"))
@click.option('-t', '--types', required=True, type=click.Choice(['mnemonic', 'private']),
              help='By mnemonic or private key')
@click.option('-h', '--hrp', default='', help='this is params is net type')
def recovery(types, hrp):
    """
    this is account submodule recovery wallet command.
    """
    message = 'Private key:' if types == 'private' else 'Mnemonic code:'
    hrp = hrp.lower()
    if types == 'private':
        hrp = check_hrp(hrp)
        if 'windows' == g_system:
            password = b''.join(input_passwd_for_win()).decode()
            mp = b''.join(input_passwd_for_win(message)).decode()
        else:
            password = input_passwd_for_linux()
            mp = input_passwd_for_linux(message)
        check_private_key = mp[2:] if mp.startswith('0x') else mp
        try:
            private_key_obj = crypto.PrivateKey.from_hex(check_private_key)
            keystores = private_key_obj.to_keyfile_json(password, hrp)
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
