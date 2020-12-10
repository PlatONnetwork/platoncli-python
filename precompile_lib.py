# _*_ coding:utf-8 _*_

##############使用pyInstaller打包时需要编译到二进制中的库#######################
# 外部引用（pyinstaller编译platoncli.py时将sdk打包到二进制和动态库中）
# PlatON网络sdk
from client_sdk_python import HTTPProvider as HTTPProvider, Web3 as Web3
from client_sdk_python.eth import Eth as Eth
from client_sdk_python.admin import Admin as Admin
from client_sdk_python.packages.platon_account import Account as Account
from client_sdk_python.packages.platon_keys import keys as keys
from client_sdk_python.packages.platon_account.datastructures import AttributeDict

# Alaya网络sdk
from alaya import HTTPProvider as Alaya_HTTPProvider, Web3 as Alaya_Web3
from alaya.eth import Eth as Alaya_Eth
from alaya.admin import Admin as Alaya_Admin
from alaya.packages.platon_account import Account as Alaya_Account
from alaya.packages.platon_keys import keys as Alaya_keys
from crypto import HDPrivateKey, HDKey
###################################################
