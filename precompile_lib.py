# _*_ coding:utf-8 _*_

##############使用pyInstaller打包时需要编译到二进制中的库#######################
# 外部引用（pyinstaller编译platoncli.py时将sdk打包到二进制和动态库中）
from client_sdk_python import HTTPProvider as HTTPProvider, Web3 as Web3
from client_sdk_python.eth import Eth as Eth
from client_sdk_python.admin import Admin as Admin
from client_sdk_python.packages.platon_account import Account as Account
from client_sdk_python.packages.platon_keys import keys as keys, datatypes
from client_sdk_python.packages.platon_account.datastructures import AttributeDict
from client_sdk_python.ppos import Ppos
from client_sdk_python.pip import Pip
from client_sdk_python.utils.encoding import tobech32address
from crypto import HDPrivateKey, HDKey