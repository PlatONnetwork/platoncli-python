import click
import os
import sys
import rlp
from hexbytes import HexBytes
from utility import get_command_usage, get_eth_obj, cust_print, g_dict_dir_config, read_json_file, write_QRCode, \
    write_csv, get_time_stamp
from common import verify_password, un_sign_data, check_dir_exits
from client_sdk_python.packages.platon_account.internal.transactions import bech32_address_bytes


def show_params():
    print('''
    类型      必填性         参数名称             参数解释
    int       must          typ                 金额类型
    String    must          benifit_address     收益账户
    String    optional      node_id             节点ID
    String    optional      external_id         外部ID            
    String    optional      node_name           节点名字
    String    optional      website             节点的第三方主页
    String    optional      details             节点的描述
    int       must          amount              质押的von
    int       optional      program_version     程序的真实版本  
    String    optional      program_version_sign程序的真实版本签名       
    String    optional      bls_pubkey          bls的公钥
    String    optional      bls_proof           bls的证明 
    int       must          reward_per          从佣金中获得的奖励份额的比例
    dict      optional      transaction_cfg     交易基本配置
    ''')


def rlp_params(args, hrp):
    typ, benifit_address, node_id, external_id, node_name, website, details, amount, program_version, \
    program_version_sign, bls_pubkey, bls_proof, _, reward_per, _ = args

    benifit_address = bech32_address_bytes(hrp)(benifit_address)
    if program_version_sign[:2] == '0x':
        program_version_sign = program_version_sign[2:]
    data = HexBytes(rlp.encode([rlp.encode(int(1000)), rlp.encode(typ), rlp.encode(benifit_address),
                                rlp.encode(bytes.fromhex(node_id)), rlp.encode(external_id), rlp.encode(node_name),
                                rlp.encode(website), rlp.encode(details),
                                rlp.encode(amount), rlp.encode(reward_per), rlp.encode(program_version),
                                rlp.encode(bytes.fromhex(program_version_sign)), rlp.encode(bytes.fromhex(bls_pubkey)),
                                rlp.encode(bytes.fromhex(bls_proof))])).hex()
    return data


@click.command(cls=get_command_usage("staking"))
@click.option('-f', '--file', help='The file is save params.')
@click.option('-d', '--address', help='wallet address.')
@click.option('-t', '--template', is_flag=True, default=False, help='View the create staking parameter template. It is '
                                                                    'not effective to coexist with other parameters.')
@click.option('-c', '--config', default="",
              help='The configuration file specifying the IP and port of the '
                   'transaction to be sent. If it is configured in the global configuration network file, IP and prot '
                   'can be obtained by specifying the name in the configuration. If the network configuration is not '
                   'filled in.')
@click.option('-o', '--offline', is_flag=True, default=False,
              help='Offline transaction or offline transaction offline not input is the default '
                   'for online transaction, and a two-dimensional code picture is generated and '
                   'placed on the desktop, providing ATON offline scanning code signature.')
@click.option('-s', '--style', default="", help='This parameter is used to determine the type of file to be signed')
def create(file, address, template, config, offline, style):
    """
    this is staking submodule create command.
    """
    if template:
        show_params()
        return

    if not os.path.isfile(file):
        cust_print('file {} not exits! please check!'.format(file), fg='r')
        sys.exit(1)
    params = read_json_file(file)
    wallet_dir = g_dict_dir_config["wallet_dir"]
    wallet_file_path, private_key, hrp, _ = verify_password(address, wallet_dir)

    ppos = get_eth_obj(config, 'ppos')
    msg = ppos.admin.getProgramVersion()

    bls_pubkey = ppos.admin.nodeInfo.blsPubKey
    bls_proof = ppos.admin.getSchnorrNIZKProve()
    program_version = msg['Version']
    program_version_sign = msg['Sign']
    _params = {}
    try:
        _params['typ'] = params['typ']
        _params['benifit_address'] = params['benifit_address']
        _params['node_id'] = params['node_id'] or ppos.admin.nodeInfo.id

        _params['external_id'] = params['external_id']
        _params['node_name'] = params['node_name']
        _params['website'] = params['website']
        _params['details'] = params['details']

        _params['amount'] = ppos.w3.toWei(str(params['amount']), "ether")
        _params['program_version'] = params['program_version'] or program_version
        _params['program_version_sign'] = params['program_version_sign'] or program_version_sign
        _params['bls_pubkey'] = params['bls_pubkey'] or bls_pubkey
        _params['bls_proof'] = params['bls_proof'] or bls_proof
        _params['pri_key'] = private_key[2:]
        _params['reward_per'] = params['reward_per']
        if isinstance(params['transaction_cfg'], dict):
            _params['transaction_cfg'] = params['transaction_cfg']
    except KeyError as e:
        cust_print('Key {} does not exist in file {},please check!'.format(e, file), fg='r')
        sys.exit(1)
    try:
        if offline:
            data = rlp_params(tuple(_params.values()), hrp)
            params['to_type'] = 'staking'
            transaction_dict = un_sign_data(data, params, ppos, _params['pri_key'])
            unsigned_tx_dir = g_dict_dir_config["unsigned_tx_dir"]
            check_dir_exits(unsigned_tx_dir)
            unsigned_file_csv_name = "unsigned_staking_create_{}.csv".format(get_time_stamp())
            unsigned_file_path = os.path.join(unsigned_tx_dir, unsigned_file_csv_name)
            if style == '':
                write_csv(unsigned_file_path, [transaction_dict])
            else:
                unsigned_file_path = unsigned_file_path.replace('csv', 'jpg')
                write_QRCode(transaction_dict, unsigned_file_path)
            cust_print('unsigned_file save to:{}'.format(unsigned_file_path), fg='g')
        else:
            tx_result = ppos.createStaking(*_params.values())
            cust_print('createStaking send transfer transaction successful, tx result:{}.'.format(tx_result), fg='g')
    except ValueError as e:
        cust_print('createStaking send transfer transaction fail,error info:{}'.format(e))
        sys.exit(1)
