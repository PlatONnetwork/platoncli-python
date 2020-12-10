# coding=utf-8
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import re
import os
import sys
import json
import time
import signal
import shutil
import zipfile
import tarfile
import platform
import subprocess
from configparser import ConfigParser
from string import Template
from logger import writeLog, setLogLevel
import click
import urllib.request as urlrequest
import psutil


# 当前目录
def get_current_dir():
    return os.getcwd()


def get_time_stamp():
    '''
    获取时间戳
    :return:
    时间戳字符串：如：20200528
    '''
    ct = time.time()
    local_time = time.localtime(ct)
    data_head = time.strftime("%Y%m%d%H%M%S", local_time)

    return data_head


g_system = platform.system().lower()
if g_system == "linux":
    import ssl

    ssl._create_default_https_context = ssl._create_unverified_context

# 系统自带的 cmd 和 powershell，在 ANSI 转义序列支持上有一个 Bug，
# 即必须事先使用 os.system("") 之后，才能正常启用转义序列功能
if os.name == "nt":
    os.system("")


# 判断ip是否在中国
def ip_in_china():
    url = 'http://ip-api.com/json'

    try:
        result = json.loads(urlrequest.urlopen(url).read())
    except:
        result = {}

    if result and result['status'] == 'success':
        return result['countryCode'] == 'CN'
    else:
        return False


# cli版本
CLI_VERSION = '0.1.0'
CLI_NAME = 'platoncli'
PLATON_NAME = 'platon'
if "windows" == g_system:
    PLATON_NAME = "platon.exe"
# default_download_url = "https://github.com/PlatONnetwork/downloads/releases/download"  # 默认下载路径
default_download_url = "https://github.com/luo-dahui/downloads/releases/download"  # 默认下载路径

# 下载路径
if ip_in_china():
    default_download_url = 'http://47.91.153.183'

# 当前目录
g_current_dir = get_current_dir()
g_dict_dir_config = {
    "default_download_url": default_download_url,  # 默认下载路径
    "current_dir": g_current_dir,
    "tmpl_dir": os.path.join(g_current_dir, "templates"),  # 模板文件路径
    "conf_dir": os.path.join(g_current_dir, "config"),  # 配置文件路径
    "download_cnf_url": os.path.join(default_download_url, "config"),
    "download_cnf_name": "download_conf.json",  # 下载链接配置文件
    "platon_dir": os.path.join(g_current_dir, "platon"),  # platon目录
    "blskey_dir": os.path.join(os.path.join(g_current_dir, "platon"), "blsKey"),  # blskey目录
    "nodekey_dir": os.path.join(os.path.join(g_current_dir, "platon"), "nodeKey"),  # nodekey目录
    "wallet_dir": os.path.join(g_current_dir, "wallet"),
    "unsigned_tx_dir": os.path.join(g_current_dir, "unsigned_transaction"),
    "signed_tx_dir": os.path.join(g_current_dir, "signed_transaction")
}

for x in ['platon', 'config', 'templates']:
    tmp_dir = os.path.join(g_current_dir, x)
    if not os.path.exists(tmp_dir):
        os.mkdir(tmp_dir)

for x in ['blsKey', 'nodeKey', 'log']:
    tmp_dir = os.path.join(g_dict_dir_config["platon_dir"], x)
    if not os.path.exists(tmp_dir):
        os.mkdir(tmp_dir)

start_time = time.time()


def cust_print(fmt, fg=None, bg=None, style=None, level="", saveLog=True):
    """
    prints table of formatted text format options
    """
    COLCODE = {
        'k': 0,  # black
        'r': 1,  # red
        'g': 2,  # green
        'y': 3,  # yellow
        'b': 4,  # blue
        'm': 5,  # magenta
        'c': 6,  # cyan
        'w': 7  # white
    }

    FMTCODE = {
        'b': 1,  # bold
        'f': 2,  # faint
        'i': 3,  # italic
        'u': 4,  # underline
        'x': 5,  # blinking
        'y': 6,  # fast blinking
        'r': 7,  # reverse
        'h': 8,  # hide
        's': 9,  # strikethrough
    }

    # properties
    props = []
    if isinstance(style, str):
        props = [FMTCODE[s] for s in style]
    if isinstance(fg, str):
        props.append(30 + COLCODE[fg])
    if isinstance(bg, str):
        props.append(40 + COLCODE[bg])

    # display
    props = ';'.join([str(x) for x in props])

    if props:
        print('\x1b[%sm%s\x1b[0m' % (props, fmt))
    else:
        print(fmt)

    if saveLog:
        # logging.info(fmt)
        LOG_LEVEL = {
            None: 'info',
            'k': 'info',  # black
            'g': 'info',  # green
            'b': 'debug',  # blue
            'y': 'warning',  # yellow
            'r': 'error',  # red
            'm': 'critical',  # magenta
            'c': 'info',  # cyan
            'w': 'info'  # white
        }
        # 没有指定日志级别时，以颜色进行界定日志级别
        if level == "":
            level = LOG_LEVEL[fg]
        writeLog(fmt, level)


def set_log_level(level):
    setLogLevel(level)


def get_system_info():
    system = platform.system().lower()
    arch = platform.machine().lower()

    if arch in ['armv5l', 'armv6l', 'armv7l']:
        arch = 'arm'
    elif arch == 'aarch64':
        arch = 'arm64'
    else:
        arch = 'amd64'

    return system, arch


# 获取py文件中的帮助信息
def get_cmd_help_by_file(path):
    help_info = ""
    with open(path, encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            if "@click.command" in line and "help=" in line:
                line = line.replace('"', "'")
                help_info = line[line.find("help='") + 6:line.find("',")]
                # print(help_info)
                break
    return help_info


def get_submodule_help_by_file(path, fileName):
    help_info = ""
    filePath = os.path.join(path, fileName)
    if not os.path.exists(filePath):
        return help_info
    with open(filePath, encoding='utf-8') as f:
        help_info = f.readline()

    return help_info


# 获取命令的usage信息(添加submodule)
def get_command_usage(submodule, isShowSubModule=True):
    class CommandUsage(click.Command):

        def format_usage(self, ctx, formatter):
            if isShowSubModule:
                usage = ctx.parent.command_path + ' ' + submodule + ' ' + ctx.command.name
            else:
                usage = ctx.parent.command_path + ' ' + ctx.command.name
            pieces = self.collect_usage_pieces(ctx)

            formatter.write_usage(usage, ' '.join(pieces))

    return CommandUsage


'''
#############节点模块######################
'''


def get_local_latest_version(version_path, name):
    # version_path = os.path.join(conf_dir, version_cnf_name)
    try:
        with open(version_path, 'r') as load_f:
            version_info = json.load(load_f)
            latest_version = version_info[name]
    except:
        cust_print('Unable to get latest version', fg='r')
        latest_version = '0.0.0'

    return latest_version


'''
# 获取版本号
def get_latest_version(name):
    version_path = os.path.join(conf_dir, version_cnf_name)
    if not os.path.exists(version_path):
        # 从服务器上下载到config目录
        version_url = '{0}/{1}/{2}'.format(g_download_url, 'version', version_cnf_name)
        try:
            cust_print('download version config file: {}'.format(version_url), fg='g')
            resp = urlrequest.urlopen(version_url)
            with open(os.path.join(conf_dir, version_cnf_name), 'wb') as f:
                shutil.copyfileobj(resp, f)
        except:
            cust_print('Unable to download version config file {0}'.format(version_url), fg='r')

    # 从本地的latest.json文件获取
    latest_version = get_local_latest_version(version_path, name)

    return latest_version
'''


def remove(path):
    if os.path.isfile(path) or os.path.islink(path):
        os.remove(path)
    elif os.path.isdir(path):
        shutil.rmtree(path)
    else:
        raise ValueError("{} is not a file or dir.".format(path))


def Schedule(blocknum, blocksize, totalsize):
    speed = (blocknum * blocksize) / (time.time() - start_time)
    # speed_str = " Speed: %.2f" % speed
    speed_str = " Speed: %s" % format_size(speed)
    recv_size = blocknum * blocksize

    # 设置下载进度条
    f = sys.stdout
    pervent = recv_size / totalsize
    if pervent > 1:
        percent_str = "%.2f%%" % 100
    else:
        percent_str = "%.2f%%" % (pervent * 100)
    n = round(pervent * 50)
    s = ('#' * n).ljust(50, '-')
    f.write(percent_str.ljust(8, ' ') + '[' + s + ']' + speed_str)
    f.flush()
    # time.sleep(0.1)
    f.write('\r')


# 字节bytes转化K\M\G
def format_size(bytes):
    try:
        bytes = float(bytes)
        kb = bytes / 1024
    except:
        print("传入的字节格式不对")
        return "Error"
    if kb >= 1024:
        M = kb / 1024
        if M >= 1024:
            G = M / 1024
            return "%.3fG" % G
        else:
            return "%.3fM" % M
    else:
        return "%.3fK" % kb


def download_genesis_file(hrp, bForced=False):
    download_conf_file = os.path.join(g_dict_dir_config["conf_dir"], g_dict_dir_config["download_cnf_name"])
    if not os.path.exists(download_conf_file):
        cust_print("download config file is not exist:{}, please check!".format(download_conf_file), fg='r')
        sys.exit(1)
    try:
        with open(download_conf_file, 'r') as load_f:
            download_info = json.load(load_f)
            download_url = download_info["platon_url"]
            if 'atp' == hrp or 'atx' == hrp:
                download_url = download_info["alaya_url"]

        genesis_name = "{}_genesis.json".format(hrp)
        download_url = os.path.join(download_url, genesis_name)

        # download_file(download_url, g_dict_dir_config["conf_dir"], dest_file_name="genesis.json")
        genesis_tmpl_path = os.path.join(g_dict_dir_config["tmpl_dir"], genesis_name)
        is_download = True
        if os.path.exists(genesis_tmpl_path):
            if not bForced:
                confirm = input('The genesis block template file already exists. Would you like to download it again? ['
                                'Y|y/N|n]: ')
                # 是否重新下载
                if confirm != 'Y' and confirm != 'y':
                    is_download = False
                    return
            # 删除创世区块模板文件
            remove(genesis_tmpl_path)

        if is_download:
            download_file(download_url, g_dict_dir_config["tmpl_dir"])
    except Exception as e:
        cust_print('Failed to download genesis file:{}'.format(e), fg='r')
        sys.exit(1)
    # cust_print('download genesis config file succeed: {}.'.format(download_url), fg='g')


def download_file(download_url, dest_dir_path, dest_file_name=""):
    download_url = download_url.replace("\\", "/")
    _, download_file_name = os.path.split(download_url)

    try:
        cust_print('start to download file:{}'.format(download_url), fg='g')
        # resp = urlrequest.urlopen(platon_url)
        global start_time
        start_time = time.time()
        urlrequest.urlretrieve(download_url, download_file_name, Schedule)
    except Exception as e:
        cust_print('Unable to download file, error message: {}!'.format(e), fg='r')
        sys.exit(1)

    # 指定保存文件的名称
    if "" == dest_file_name:
        dest_file_name = download_file_name
    # 移动文件
    src_path = os.path.join(g_current_dir, download_file_name)
    des_path = os.path.join(dest_dir_path, dest_file_name)
    shutil.move(src_path, des_path)
    cust_print('save file succeed: {}'.format(des_path), fg='g')


# 下载路径
def download_url_config_file():
    download_conf_name = g_dict_dir_config["download_cnf_name"]
    local_file_path = os.path.join(g_dict_dir_config["conf_dir"], download_conf_name)

    if os.path.exists(local_file_path):
        confirm = input('The download_conf.json file is exist，'
                        'Whether to download again the download_conf.json file? [Y|y/N|n]: ')
        # 是否下载路径配置文件
        if confirm != 'Y' and confirm != 'y':
            return local_file_path

    download_conf_url = g_dict_dir_config["download_cnf_url"]
    download_conf_path = os.path.join(download_conf_url, download_conf_name).replace("\\", "/")
    download_file(download_conf_path, g_dict_dir_config["conf_dir"])
    cust_print('download config file succeed: {}.'.format(download_conf_path), fg='g')

    return local_file_path


# 下载二进制包
def download_binary_tar(network_type="PlatON"):
    download_conf_current_path = os.path.join(g_dict_dir_config["conf_dir"],
                                              g_dict_dir_config["download_cnf_name"])
    if not os.path.exists(download_conf_current_path):
        # 是否下载
        confirm = input('The download_conf.json file does not exist，'
                        'Whether to download the download_conf.json file? [Y|y/N|n]: ')
        # 是否下载路径配置文件
        if confirm == 'Y' or confirm == 'y':
            download_url_config_file()
        else:
            cust_print('Unable to download platon binary package, '
                       'error message: The download_conf.json file does not exist!', fg='r')
            sys.exit(1)

    KEY_TOOL_NAME = get_keytool_name(network_type)
    with open(download_conf_current_path, 'r') as load_f:
        download_info = json.load(load_f)
        download_url = download_info["platon_url"]
        if 'alaya' == network_type.lower():
            download_url = download_info["alaya_url"]

    system, arch = get_system_info()
    platon_name = "platon-{}-{}".format(system, arch)
    platon_file = "{}.tar.gz".format(platon_name)
    platon_url = os.path.join(download_url, platon_file).replace("\\", "/")

    try:
        cust_print('download platon binary:{}'.format(platon_url), fg='g')
        # resp = urlrequest.urlopen(platon_url)
        global start_time
        start_time = time.time()
        urlrequest.urlretrieve(platon_url, platon_file, Schedule)
    except Exception as e:
        cust_print('Unable to download platon binary package, error message: {}!'.format(e), fg='r')
        sys.exit(1)

    # 解压
    tar_path = os.path.join(g_current_dir, platon_file)
    unpack_dir = g_dict_dir_config["platon_dir"]
    with tarfile.open(tar_path, mode='r:*') as tar:
        # tar.extractall(g_current_dir)
        tar.extractall(unpack_dir)
        for x in [PLATON_NAME, KEY_TOOL_NAME]:
            # src_path = os.path.join(unpack_dir, x)
            des_path = os.path.join(unpack_dir, x)
            # shutil.move(src_path, des_path)
            os.chmod(des_path, 0o755)

    # 删除tar文件
    remove(tar_path)
    # 删除解压路径
    # remove(unpack_dir)


# 拷贝模板文件
def copy_template_files():
    release_template_path = os.path.join(os.path.split(os.path.realpath(__file__))[0], "templates")
    current_template_path = os.path.join(os.getcwd(), "templates")

    if release_template_path == current_template_path:
        return

    temp_file_list = ['platon_cfg.tmpl']
    sys_type, _ = get_system_info()
    if "linux" == sys_type:
        temp_file_list.append('platon_cron.tmpl')
        temp_file_list.append('platon_logrotate.tmpl')

    # 拷贝模板文件
    for y in temp_file_list:
        src_file = os.path.join(release_template_path, y)
        if not os.path.exists(src_file):
            cust_print('template file {} is not exist, please check!'.format(src_file), fg='r')
        else:
            shutil.copy(src_file, current_template_path)


# 安装节点:二进制文件,模板文件
def install_node(hrp):
    network_type = "PlatON"
    if 'atp' == hrp or 'atx':
        network_type = "Alaya"
    # 判断是否已安装
    isInstall = check_install_valid(network_type)
    whether_install_binary = True
    if isInstall:
        confirm = input('Binary package installed. Do you want to reinstall? [Y|y/N|n]: ')
        if confirm != 'Y' and confirm != 'y':
            whether_install_binary = False

    if whether_install_binary:
        cust_print('Start to install platon binary...', fg='y')
        # 下载二进制包并解压
        download_binary_tar(network_type)
        cust_print('Install platon node successfully.', fg='g')

    # 拷贝模板文件
    isExist = check_platon_tmpl_exist()
    whether_reBuild_tmpl = True
    if isExist:
        confirm = input('The template file already exists. Do you want to rebuild it? [Y|y/N|n]: ')
        if confirm != 'Y' and confirm != 'y':
            whether_reBuild_tmpl = False

    if whether_reBuild_tmpl:
        cust_print('Start to copy platon template files...', fg='y')
        # 拷贝模板文件
        copy_template_files()
        cust_print('copy platon template files successfully.', fg='g')


def check_platon_tmpl_exist():
    count = 0
    check_max_count = 1
    tmpl_file_list = ['platon_cfg.tmpl']
    if 'linux' == g_system:
        tmpl_file_list.append('platon_cron.tmpl')
        tmpl_file_list.append('platon_logrotate.tmpl')
        check_max_count = check_max_count + 2

    for y in tmpl_file_list:
        if os.path.exists('{0}/{1}'.format(g_dict_dir_config["tmpl_dir"], y)):
            count += 1

    flag = False
    if count == check_max_count:
        flag = True

    return flag


# 检查platon二进制,配置文件是否安装成功
def check_install_valid(network_type="PlatON"):
    """
    Check for key files that indicate a valid install that can be updated
    """
    count = 0
    check_max_count = 2

    KEY_TOOL_NAME = get_keytool_name(network_type)
    for x in [PLATON_NAME, KEY_TOOL_NAME]:
        if os.path.exists('{0}/{1}'.format(g_dict_dir_config["platon_dir"], x)):
            count += 1

    flag = False
    if count == check_max_count:
        flag = True
        for x in [PLATON_NAME, KEY_TOOL_NAME]:
            os.chmod(os.path.join(g_dict_dir_config["platon_dir"], x), 0o755)

    return flag


def check_init_keys(blskey_dir=g_dict_dir_config["blskey_dir"],
                    nodeKey_dir=g_dict_dir_config["nodekey_dir"]):
    count = 0
    flag = False

    check_files = {
        'blskey': os.path.join(blskey_dir, 'blskey'),
        'blspub': os.path.join(blskey_dir, 'blspub'),
        'nodeid': os.path.join(nodeKey_dir, 'nodeid'),
        'nodekey': os.path.join(nodeKey_dir, 'nodekey')
    }

    for name, path in check_files.items():
        if os.path.exists(path):
            count += 1

    if len(check_files) == count:
        flag = True

    return flag


def check_init_valid():
    count = 0
    flag = False

    check_files = {
        'blskey': os.path.join(g_dict_dir_config["blskey_dir"], 'blskey'),
        'blspub': os.path.join(g_dict_dir_config["blskey_dir"], 'blspub'),
        'nodeid': os.path.join(g_dict_dir_config["nodekey_dir"], 'nodeid'),
        'nodekey': os.path.join(g_dict_dir_config["nodekey_dir"], 'nodekey')
    }

    for name, path in check_files.items():
        if not os.path.exists(path):
            count += 1

    if count > 0:
        cust_print(
            'You have to initialize platon node, please type `./platoncli init` first', fg='r')
        sys.exit(-1)
    else:
        flag = True

    return flag


def get_pid(pname, new_rpc_port=6789):
    for proc in psutil.process_iter():
        if proc.name() == pname:

            list_cmdline = proc.cmdline()
            bIsFindRpc = False
            for param in list_cmdline:
                if bIsFindRpc:
                    if new_rpc_port == int(param):
                        return proc.pid
                    break
                if '--rpcport' == param:
                    bIsFindRpc = True

    return None


def write_file(path, content):
    with open(path, 'w') as fp:
        fp.write(content)


def get_keytool_name(network_type):
    KEY_TOOL_NAME = "platonkey"
    if "alaya" == network_type.lower():
        KEY_TOOL_NAME = "alayakey"
    if "windows" == g_system:
        KEY_TOOL_NAME = KEY_TOOL_NAME + ".exe"

    return KEY_TOOL_NAME


def generate_nodekey(key_dir, hrp):
    network_type = "PlatON"
    if 'atp' == hrp.lower() or 'atx' == hrp.lower():
        network_type = "Alaya"

    KEY_TOOL_NAME = get_keytool_name(network_type)
    keytool_path = os.path.join(g_dict_dir_config["platon_dir"], KEY_TOOL_NAME)
    if not os.path.exists(keytool_path):
        cust_print('keytool was not installed, Generate key file fail!', fg='r')
        return False

    keypair = subprocess.check_output(
        [keytool_path, 'genkeypair']).decode('utf8').splitlines()

    k_pri = re.findall(r"PrivateKey:(.*)", keypair[0].replace(' ', ''))[0]
    k_pub = re.findall(r"PublicKey:(.*)", keypair[1].replace(' ', ''))[0]

    write_file(os.path.join(key_dir, 'nodekey'), k_pri)
    write_file(os.path.join(key_dir, 'nodeid'), k_pub)

    return True


def generate_blskey(key_dir, hrp):
    network_type = "PlatON"
    if 'atp' == hrp.lower() or 'atx' == hrp.lower():
        network_type = "Alaya"

    KEY_TOOL_NAME = get_keytool_name(network_type)
    keytool_path = os.path.join(g_dict_dir_config["platon_dir"], KEY_TOOL_NAME)
    if not os.path.exists(keytool_path):
        cust_print('{} was not installed, Generate key file fail!'.format(KEY_TOOL_NAME), fg='r')
        return False
    blskeypair = subprocess.check_output(
        [keytool_path, 'genblskeypair']).decode('utf8').splitlines()

    b_pri = re.findall(r"PrivateKey:(.*)",
                       blskeypair[0].replace(' ', ''))[0]
    b_pub = re.findall(r"PublicKey:(.*)",
                       blskeypair[1].replace(' ', ''))[0]

    write_file(os.path.join(key_dir, 'blskey'), b_pri)
    write_file(os.path.join(key_dir, 'blspub'), b_pub)
    return True


def save_node_conf(ip, rpc_port, hrp, chainId):
    # 保存配置文件

    '''
    node_conf = {
        "nodeAddress": ip,
        "rpcPort": rpc_port,
        "hrp": hrp,
        "chainId": chainId
    }
    '''

    node_conf = {
        "rpcAddress": "http://{}:{}".format(ip, rpc_port),
        "hrp": hrp,
        "chainId": chainId
    }

    node_conf_path = os.path.join(g_dict_dir_config["conf_dir"], "node_config.json")
    with open(node_conf_path, 'w') as f:
        f.write(json.dumps(node_conf))

    return node_conf_path


# 初始化创世区块
def init_genesis_block(hrp, genesis_file_path=""):
    # 是否已经初始化
    data_path = os.path.join(g_dict_dir_config["platon_dir"], "data")
    if os.path.exists(data_path):
        confirm = input('The genesis block has been initialized. Is it reinitialized (Y|y/N|n): ')
        if confirm != 'Y' and confirm != 'y':
            return
        else:
            # 删除创世区块文件目录
            remove(data_path)

    if "" == genesis_file_path:
        genesis_file_path = os.path.join(g_dict_dir_config["conf_dir"], "genesis.json")

    # 启动参数配置
    start_config = ConfigParser()
    start_config.read(os.path.join(g_dict_dir_config["conf_dir"], 'platon.cfg'))
    params_dict = dict(start_config.items('platon'))

    if not os.path.exists(genesis_file_path):
        genesis_tmpl_path = os.path.join(g_dict_dir_config["tmpl_dir"], "{}_genesis.json".format(hrp))
        if not os.path.exists(genesis_tmpl_path):
            # 下载genesis模板文件
            download_genesis_file(hrp, True)
        try:
            # get node id
            nodeid_file_path = os.path.join(g_dict_dir_config["nodekey_dir"], "nodeid")
            with open(nodeid_file_path, "r") as f_n:
                nodeid = f_n.read()

            # get blsPublicKey
            blspub_file_path = os.path.join(g_dict_dir_config["blskey_dir"], "blspub")
            with open(blspub_file_path, "r") as f_b:
                blspub = f_b.read()

            # get ip and port
            rpcaddr = params_dict["rpcaddr"]
            port = params_dict["port"]
        except Exception as e:
            cust_print("init genesis block failed, error message:{}".format(e))
            sys.exit(1)

        # 重新写入key等信息
        config = {
            'nodeid': nodeid,
            'ip': rpcaddr,
            "port": port,
            "blsPubKey": blspub
        }

        conf_map = {
            '{}_genesis.json'.format(hrp): 'genesis.json'
        }

        for k, v in conf_map.items():
            with open(os.path.join(g_dict_dir_config["tmpl_dir"], k), 'r') as fp_in:
                src = Template(fp_in.read())

            result = src.substitute(config)

            with open(os.path.join(g_dict_dir_config["conf_dir"], v), 'w') as fp_out:
                fp_out.write(result)

    cmd = '{0}/platon --datadir {1} init {2}'.format(g_dict_dir_config["platon_dir"],
                                                     params_dict['datadir'], genesis_file_path)
    os.system(cmd)

    # 将创世区块文件中的chainid写入node_conf.json文件中
    with open(genesis_file_path, 'r') as load_f:
        genesis_info = json.load(load_f)

    chainId = genesis_info["config"]["chainId"]
    save_node_conf(params_dict["rpcaddr"], params_dict["rpcport"], params_dict["hrp"], chainId)
    cust_print('Initializing genesis block file successfully: {}.'.format(genesis_file_path), fg='g')


# 初始化节点
def init_node(hrp, is_private_chain=False, config_path=""):
    # 安装节点
    install_node(hrp)

    # cust_print('Warning: Initialize node will regenerate keys if you have initialized before.', fg='y')
    confirm = input('Do you want to initialize node (Y|y/N|n): ')
    if confirm == 'Y' or confirm == 'y':
        if not is_private_chain:

            if 'atp' == hrp:
                network = '--alaya'
            elif 'atx' == hrp:
                network = '--alayatestnet'
            elif 'lat' == hrp:
                network = '--mainnet'
            elif 'lax' == hrp:
                network = '--testnet'
            else:
                cust_print('error hrp type:{}!!!'.format(hrp), fg='r')
                sys.exit(1)
        else:
            network = ""
    else:
        return

    config = {
        'base_dir': g_current_dir,
        'network': network,
        'hrp': hrp
    }

    conf_map = {
        'platon_cfg.tmpl': 'platon.cfg'
    }
    if 'linux' == g_system:
        linux_conf_map = {
            'platon_cron.tmpl': '.platon_cron',
            'platon_logrotate.tmpl': '.platon_logrotate'
        }
        conf_map.update(linux_conf_map)

    cust_print('Generate platon configurations.', fg='y')

    try:
        for k, v in conf_map.items():
            with open(os.path.join(g_dict_dir_config["tmpl_dir"], k), 'r') as fp_in:
                src = Template(fp_in.read())

            result = src.substitute(config)

            with open(os.path.join(g_dict_dir_config["conf_dir"], v), 'w') as fp_out:
                fp_out.write(result)

        # linux启动定时任务
        if 'linux' == g_system:
            cmd = '/usr/bin/crontab {0}'.format(
                os.path.join(g_dict_dir_config["conf_dir"], '.platon_cron'))
            os.system(cmd)

        cust_print('Generate platon configurations successfully.', fg='g')
    except Exception as e:
        cust_print('Failed to generate platon configurations:{}.'.format(e), fg='r')

    try:
        gen_key_info = True
        if check_init_keys():
            confirm = input('Blskey and NodeKey are already generated. Do you want to regenerate them? (Y|y/N|n): ')
            if confirm != 'Y' and confirm != 'y':
                gen_key_info = False
            else:
                # 重新生成key信息，删除genesis.json
                genesis_path = os.path.join(g_dict_dir_config["conf_dir"], "genesis.json")
                if is_private_chain and os.path.exists(genesis_path):
                    remove(genesis_path)

        if gen_key_info:
            cust_print('start to generate platon keys...', fg='y')
            generate_nodekey(g_dict_dir_config["nodekey_dir"], hrp)
            generate_blskey(g_dict_dir_config["blskey_dir"], hrp)
            cust_print('Generate platon keys successfully.', fg='g')

        # 私链初始化创始区块
        if is_private_chain:
            init_genesis_block(hrp, config_path)
    except Exception as e:
        cust_print(e, fg='r')
        cust_print('Failed to initialize node, error message:{}!!!'.format(e), fg='r')
        sys.exit(1)

    cust_print('Initialize node successfully', fg='g')


def get_local_platon_cfg(platon_cfg_path=""):
    # 检查启动参数配置文件
    if "" == platon_cfg_path:
        platon_cfg_path = os.path.join(g_dict_dir_config["conf_dir"], 'platon.cfg')
    if not os.path.exists(platon_cfg_path):
        cust_print('The node startup parameter profile does not exist:{}!!!'.format(platon_cfg_path), fg='r')
        sys.exit(1)

    config = ConfigParser()
    config.read(platon_cfg_path)
    platon_cfg = dict(config.items('platon'))

    return platon_cfg


def shutdown_node(needToConfirm=False):
    cfg = get_local_platon_cfg()
    hrp = cfg["hrp"]
    network_type = "PlatON"
    if 'atx' == hrp or 'atp' == hrp:
        network_type = "Alaya"
    if not check_install_valid(network_type):
        cust_print('Binary is not installed, please install and initialize the node first!!!', fg='r')
        sys.exit(1)

    if not check_init_keys():
        cust_print('Blskey and Nodekey are not generated, please enter!!!', fg='r')
        sys.exit(1)

    pid = get_pid(PLATON_NAME, int(cfg['rpcport']))
    if pid:
        if needToConfirm:
            confirm = input('Node process is running, do you want to stop node? (Y|y/N|n): ')
            if confirm != 'Y' and confirm != 'y':
                cust_print('Node process is running, please stop after operation, export failed.',
                           fg='r', level="warning")
                return False

        os.kill(int(pid), signal.SIGTERM)

        time.sleep(2)
        pid = get_pid(PLATON_NAME, int(cfg['rpcport']))
        if pid:
            cust_print('Failed to stop platon, rpc port:{}!'.format(int(cfg['rpcport'])), fg='r')
            return False
        else:
            cust_print('Stop platon successfully, rpc port:{}.'.format(int(cfg['rpcport'])), fg='g')
    else:
        cust_print('PlatON is not running, rpc port:{}.'.format(int(cfg['rpcport'])), fg='g')

    return True


def startup_node():
    r = get_local_platon_cfg()

    pid = get_pid(PLATON_NAME, int(r['rpcport']))
    # 需要通过rpc端口过滤
    if pid:
        cust_print('PlatON is running, pid:{}, rpc port:{}...'.format(pid, int(r['rpcport'])), fg='g')
    else:
        hrp = r["hrp"]
        network_type = "PlatON"
        if 'atx' == hrp or 'atp' == hrp:
            network_type = "Alaya"
        if not check_install_valid(network_type):
            cust_print('Binary is not installed, please install and initialize the node first!!!', fg='r')
            sys.exit(1)

        if not check_init_keys():
            cust_print('Blskey and Nodekey are not generated, please enter!!!', fg='r')
            sys.exit(1)

        network = r["network"]
        data_path = os.path.join(g_dict_dir_config["platon_dir"], "data")
        if "" == network and not os.path.exists(data_path):
            # 私链
            cust_print('The private chain is not initialized, please initialize the genesis.json before '
                       'starting the node.', fg='r')
            sys.exit(1)

        binary_path = os.path.join(g_dict_dir_config["platon_dir"], PLATON_NAME)
        cmd = '{0} --identity {1} {2} --datadir {3} --port {4} --rpcport {5} --rpcapi {6} --rpc ' \
              '--nodekey {7} --cbft.blskey {8} --verbosity {9} --rpcaddr {10} --syncmode {11} > {12} 2>&1 &'.format(
            binary_path, r['identity'], r['network'], r['datadir'], r['port'], r['rpcport'],
            r['rpcapi'], r['nodekey'], r['blskey'], r['verbosity'], r['rpcaddr'], r['syncmode'], r['logfile'])

        if "linux" == g_system:
            cmd = "nohup {0}".format(cmd)
        # print(cmd)
        # os.system(cmd)
        subprocess.Popen(cmd, shell=True)
        time.sleep(1)

        pid = get_pid(PLATON_NAME, int(r['rpcport']))
        if pid:
            start_tail_time = int(get_time_stamp())
            end_tail_time = int(get_time_stamp())
            with open(r['logfile'], "r", encoding="utf8") as fi:
                while (end_tail_time - start_tail_time) < 5:
                    fi.tell()
                    line = fi.readline()
                    if line:
                        print(line)

                    # time.sleep(1)
                    end_tail_time = int(get_time_stamp())

            cust_print('Start platon successfully, pid:{}, rpc port:{}...'.format(pid, int(r['rpcport'])), fg='g')
        else:
            cust_print('Failed to start platon, rpc_port: {}'.format(int(r['rpcport'])), fg='r')


def restart_node():
    check_install_valid()
    check_init_valid()

    shutdown_node()
    time.sleep(1)
    startup_node()


def get_platon_version():
    cmd = "{0}/{1} version | grep '^Version' | awk '{{print $2}}'".format(
        g_dict_dir_config["platon_dir"], PLATON_NAME)

    if "linux" == g_system:
        proc = subprocess.Popen(
            cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
        proc = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    stdout, stderr = proc.communicate()
    ret = proc.poll()

    if ret == 0:
        current_version = re.search(
            r'([\d.]+)', stdout.decode('utf8').strip()).group()
    else:
        current_version = '0.0.0'

    return current_version


def connect_node(rpcAddress, Web3, Eth, HTTPProvider):
    try:
        w3 = Web3(HTTPProvider(rpcAddress))
        platon = Eth(w3)
        blkNumber = platon.blockNumber
        cust_print('get block number:{}'.format(blkNumber), fg='g')
        cust_print('connect to node succeed.', fg='g')

        # 获取chainid
        '''
        admin = Admin(w3)
        chainId = admin.nodeInfo.protocols.platon.config.chainId
        cust_print('get node chainId: {}'.format(chainId), fg='g')
        '''
    except Exception as e:
        cust_print('connect to node falied, error message:{}.'.format(e), fg='r')
        sys.exit(1)

    return platon


def make_zip(source_dir, output_filename):
    """打包目录为zip文件（未压缩）

    Args:
        source_dir: 要打包的目录
        output_filename: 输出的zip文件的名称
    """
    zipf = zipfile.ZipFile(output_filename, 'w')
    pre_len = len(os.path.dirname(source_dir))
    for parent, _, filenames in os.walk(source_dir):
        for filename in filenames:
            pathfile = os.path.join(parent, filename)
            arcname = pathfile[pre_len:].strip(os.path.sep)  # 相对路径
            zipf.write(pathfile, arcname)
    zipf.close()


def un_zip(zip_file, target_dir):
    """解压压缩文件到指定目录

    Args:
        zip_file: 要解压的zip文件名称
        target_dir: 解压后的文件夹放置目录
    Raises:
        Exception：要提取的文件不是以.zip为后缀，抛出异常
    """
    if not zip_file.endswith(".zip"):
        raise Exception("File format error")

    zFile = zipfile.ZipFile(zip_file, "r")
    for fileM in zFile.namelist():
        zFile.extract(fileM, target_dir)
    zFile.close()
