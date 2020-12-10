import json
import os
import sys

import click

from utility import get_command_usage, get_platon_version, cust_print, get_local_platon_cfg, \
    g_current_dir, g_dict_dir_config
from precompile_lib import Web3, HTTPProvider, Eth
# 治理地址
dict_gov_contractAddr = {
    "lat": "lat1zqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq93t3hkm",
    "lax": "lax1zqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq97wrcc5",
    "atp": "atp1zqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq9ga80f5",
    "atx": "atx1zqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq9zmm967"
}


def platon_call(url, to_addr="atp1zqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq9ga80f5", data="0xc483820837"):
    w3 = Web3(HTTPProvider(url))
    platon = Eth(w3)
    recive = platon.call({
        "to": to_addr,
        "data": data
    })

    recive = str(recive, encoding="utf8")
    recive = recive.replace('\\', '').replace('"{', '{').replace('}"', '}')
    recive = json.loads(recive)

    return recive


def formatVersion(intVersion):
    if intVersion == 0:
        return "0.0.0"

    major = intVersion >> 16 & 0xff
    minor = intVersion >> 8 & 0xff
    patch = intVersion & 0xff

    return "{}.{}.{}".format(major, minor, patch)


def versionToNum(strVersion):
    if strVersion == "":
        return 0
    info_list = strVersion.split(".")
    if 3 != len(info_list):
        return 0

    major = int(info_list[0])
    minor = int(info_list[1])
    patch = int(info_list[2])

    return major << 16 | minor << 8 | patch


@click.command(cls=get_command_usage("node"))
def check():
    """
    this is node submodule check command.
    """
    platon_cfg_path = os.path.join(g_dict_dir_config["conf_dir"], 'platon.cfg')
    platon_cfg = get_local_platon_cfg(platon_cfg_path)
    url = "http://{}:{}".format(platon_cfg["rpcaddr"], platon_cfg["rpcport"])
    cust_print("connect node: {}".format(url), fg='g')

    hrp = platon_cfg["hrp"]
    cust_print("get hrp:{} from platon_cfg file: {}".format(hrp, platon_cfg_path), fg='g')
    # get platon version on chain
    try:
        ret = platon_call(url, dict_gov_contractAddr[hrp])
        platon_version = ret["Ret"]
        cust_print("platon version on chain: {}".format(formatVersion(platon_version)), fg='g')

        # get platon current version
        current_version = get_platon_version()
        cust_print("platon current version on local: {}".format(current_version), fg='g')

        if platon_version > versionToNum(current_version):
            cust_print(
                "The current version is not the latest version. It is recommended that the user change the version "
                "of platon. Please provide the latest download address according to the official and use the "
                "command: platoncli node upgrade --path.", fg='r', level="warning")
        else:
            cust_print("The current binary is the latest version and does not need to be updated: {}".
                       format(g_current_dir), fg='g')

    except Exception as e:
        cust_print("Failed to get version: {}".format(e), fg='r')
        sys.exit(1)
