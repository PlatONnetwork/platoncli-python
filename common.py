import sys
import os
from utility import cust_print, get_dir_by_name, g_system, get_wallet_file_by_address, input_passwd_for_linux, \
    input_passwd_for_win, get_private_key_from_wallet_file, g_dict_dir_config, read_json_file


def verify_password(address, wallet_dir, passwd=None):
    if address.endswith(".json"):
        config = os.path.join(g_dict_dir_config["conf_dir"], "node_config.json")
        info = read_json_file(config)
        find, wallet_file_path = get_dir_by_name(wallet_dir, address)
        if not find:
            cust_print('The wallet file of {} could not be found on {}'.format(address, wallet_dir),fg='r')
            sys.exit(1)
        try:
            hrp = info['hrp']
        except:
            cust_print('the wallet {} is not alaya or platon,please check!'.format(wallet_file_path), fg='r')
            sys.exit(1)
    elif 42 != len(address):
        cust_print("Wrong address parameter: --address {}".format(address), fg='r')
        sys.exit(1)
    else:
        # 根据地址找钱包
        hrp = address[:3]
        net_type = "mainnet"
        if hrp == 'lax' or hrp == 'atx':
            net_type = 'testnet'
        find, wallet_file_path, fileName = get_wallet_file_by_address(wallet_dir, address, net_type)
        if not find:
            cust_print('The wallet file of {} could not be found on {}'.format(fileName, wallet_dir),fg='r')
            sys.exit(1)
        check_name = fileName
        check_address = address
        cust_print("Name:{}, Address:{}".format(check_name, check_address), fg='g')
    if not passwd:
        if 'windows' == g_system:
            passwd = b''.join(input_passwd_for_win()).decode()
        else:
            passwd = input_passwd_for_linux()
    if 'lat' == hrp or 'lax' == hrp:
        from precompile_lib import Account, keys
    else:
        from precompile_lib import Alaya_Account as Account, Alaya_keys as keys
    privateKey = get_private_key_from_wallet_file(Account, keys, wallet_file_path, passwd)
    return wallet_file_path, privateKey, hrp, Account


def confirm_password():
    method_name = sys._getframe(1).f_code.co_name
    prompt_message1 = 'input new password:' if method_name == 'changePassword' else 'input password:'
    prompt_message2 = 'confirm new password:' if method_name == 'changePassword' else 'input password again:'
    if 'windows' == g_system:
        passwd1 = b''.join(input_passwd_for_win(prompt_message1)).decode()
        if len(passwd1) < 6:
            cust_print('Password length must be greater than or equal to 6!', fg='r')
            sys.exit(1)
        passwd2 = b''.join(input_passwd_for_win(prompt_message2)).decode()
    else:
        passwd1 = input_passwd_for_linux(prompt_message1)
        if len(passwd1) < 6:
            cust_print('Password length must be greater than or equal to 6!', fg='r')
            sys.exit(1)
        passwd2 = input_passwd_for_linux(prompt_message2)
    if passwd1 != passwd2:
        cust_print('The password is not the same twice!', fg='r')
        sys.exit(1)
    return passwd1


def un_sign_data(data, params, ppos, private_key):
    transaction_dict = {}
    transaction_cfg = params['transaction_cfg']
    to_type = '{}Address'.format(params['to_type'])
    to_address = getattr(ppos.web3, to_type)
    if transaction_cfg is None:
        transaction_cfg = {}
    if transaction_cfg.get("gasPrice", None) is None:
        transaction_dict["gasPrice"] = ppos.web3.platon.gasPrice
    else:
        transaction_dict["gasPrice"] = transaction_cfg["gasPrice"]
    public_key_obj = ppos.datatypes.PrivateKey(bytes.fromhex(private_key)).public_key
    from_address = ppos.web3.pubkey_to_address(public_key_obj)
    if transaction_cfg.get("nonce", None) is None:
        transaction_dict["nonce"] = ppos.web3.platon.getTransactionCount(from_address)
    else:
        transaction_dict["nonce"] = transaction_cfg["nonce"]
    if transaction_cfg.get("gas", None) is None:
        transaction_data = {"to": to_address, "data": data, "from": from_address}
        transaction_dict["gas"] = ppos.web3.platon.estimateGas(transaction_data)
    else:
        transaction_dict["gas"] = transaction_cfg["gas"]
    transaction_dict["chainId"] = ppos.web3.chainId
    transaction_dict["to"] = to_address
    transaction_dict["data"] = data
    transaction_dict["from"] = from_address
    if transaction_cfg.get("value", 0) > 0:
        transaction_dict["value"] = int(transaction_cfg.get("value", 0))
    return transaction_dict


def bech32_address_bytes(hrp):
    if hrp in ['atp', 'atx']:
        from alaya.packages.platon_account.internal.transactions import bech32_address_bytes
        return bech32_address_bytes
    if hrp in ['lat', 'lax']:
        from alaya.packages.platon_account.internal.transactions import bech32_address_bytes
        return bech32_address_bytes


def check_dir_exits(dir_str):
    try:
        if not os.path.exists(dir_str):
            os.makedirs(dir_str)
    except Exception as e:
        cust_print('create {} fail!,Exception info:{}'.format(dir_str, e))
