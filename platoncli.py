# _*_ coding:utf-8 _*_
import os
import sys
import platform
import subprocess

import click
from click import echo
from utility import cust_print, get_cmd_help_by_file, get_submodule_help_by_file
import precompile_lib

# cli二进制/platoncli.py所在目录(多节点目录下执行时，需要通过绝对路径搜索子模块，子命令文件)
cli_bin_path = os.path.dirname(os.path.realpath(sys.argv[0]))
platoncli_py = os.path.join(cli_bin_path, 'platoncli.py')
if not os.path.isfile(platoncli_py):
    cmd = "where platoncli" if platform.system().lower() == "windows" else "which platoncli"
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()
    ret = proc.poll()
    if 0 == ret:
        cli_bin_path, _ = os.path.split(stdout.decode('utf8').strip())

# 源码目录名称
code_dir_name = "{}/src".format(cli_bin_path)
# 命令py文件存放目录
cmd_path = ""
# 帮助信息
short_help = ""
help_info = ""
# submodule对应名称
options_metavar = ""
isSubModule = False
isCmd = False

subModList = []
cmdList = []
dict_cmd_help = {}
# 打印帮助信息的空格数
min_num_spaces = 5
# 子模块和命令中最大的名称长度
max_name_len = 0


# 加载子模块和命令
def load_cmd_and_subMod():
    global max_name_len
    fileList = os.listdir(code_dir_name)
    for s in fileList:
        path = os.path.join(code_dir_name, s)
        if os.path.isdir(path) and (not s.startswith("__") or not s.endswith("__")):
            subModList.append(s)
            if len(s) > max_name_len:
                max_name_len = len(s)
            subMod_help_info = get_submodule_help_by_file(path, "help")
            dict_cmd_help[s] = subMod_help_info

        elif os.path.isfile(path) and s.endswith(".py"):
            s = s.split(".py")[0]
            cmdList.append(s)
            if len(s) > max_name_len:
                max_name_len = len(s)
            cmd_help_info = get_cmd_help_by_file(path)
            dict_cmd_help[s] = cmd_help_info
            # print(help_info)


# 获取指定目录下group组命令
# 如：platoncli module command
def list_subMod_cmds_by_folderName(group_folder_name):
    folder = os.path.join(os.path.dirname(__file__), group_folder_name)

    # 判断是否子模块命令说明
    def is_show_submodule_cmds_help(args):
        if args is None or len(args) <= 1 or (len(args) == 2 and args[1] == "--help"):
            return True
        return False

    # 定义命令集合类
    class FolderCommands(click.MultiCommand):
        # 重写列出命令接口（查询指定目录下的所有以.py结尾的文件）
        def list_commands(self, ctx):
            return sorted(
                f[:-3] for f in os.listdir(folder) if f.endswith('.py'))

        # 重写获取命令接口（根据命令名查找对应的py文件，命令名和文件名需要匹配）
        def get_command(self, ctx, name):
            namespace = {}
            command_file = os.path.join(folder, name + '.py')
            if not os.path.exists(command_file):
                cust_print("command:【{}】 is not exist, please check.".format(name), fg='r')
                show_help()
                sys.exit(1)
            with open(command_file, encoding='utf-8') as f:
                code = compile(f.read(), command_file, 'exec')
                eval(code, namespace, namespace)
            return namespace[name.replace('-', '_')]

        # 重写解析参数接口
        def parse_args(self, ctx, args):
            # 判断是否展示子模块的命令说明
            if not is_show_submodule_cmds_help(args):
                tmpArgs = []
                for i in range(1, len(args)):
                    tmpArgs.append(args[i])
                # 调用原解析参数接口
                click.MultiCommand.parse_args(self, ctx, tmpArgs)
            else:
                # 展示子模块说明，直接返回
                echo(ctx.get_help(), color=ctx.color)
                ctx.exit()
                return ctx.args

    return FolderCommands


# 获取指定目录下group组命令
# 如：platoncli init
def get_cmd_by_fileName(group_folder_name, cmd_name):
    folder = os.path.join(os.path.dirname(__file__), group_folder_name)

    # 定义命令集合类
    class FileCommands(click.MultiCommand):
        # 重写列出命令接口（查询指定目录下指定命令的py文件）
        def list_commands(self, ctx):
            file_name = "{}.py".format(cmd_name)
            return sorted(
                f[:-3] for f in os.listdir(folder) if f.endswith(file_name))

        # 重写获取命令接口（根据命令名查找对应的py文件，命令名和文件名需要匹配）
        def get_command(self, ctx, name):
            namespace = {}
            command_file = os.path.join(folder, name + '.py')
            if not os.path.exists(command_file):
                cust_print("command:【{}】 is not exist, please check.".format(name), fg='r')
                show_help()
                sys.exit(1)
            with open(command_file, encoding='utf-8') as f:
                # print("command_file:", command_file)
                code = compile(f.read(), command_file, 'exec')
                eval(code, namespace, namespace)
            return namespace[name.replace('-', '_')]

    return FileCommands


# 获取并判断是否是正确的子模块名称或者命令名称
def is_submodule_or_cmd(args="node"):
    return args in subModList, args in cmdList


# 帮助
def show_help():
    print('''Usage: platoncli [Submodule/Command] [COMMAND] [ARGS]...

    platoncli 工具

    --help -h     帮助
    --version -v  版本号''')

    pre_num_spaces = 4
    print('\nSubmodules:')
    for subMod in subModList:
        num_space = int(max_name_len - len(subMod) + min_num_spaces)

        if subMod in dict_cmd_help and "" != dict_cmd_help[subMod]:
            subMod_help = dict_cmd_help[subMod]
            print("{}{}{}{}".format(pre_num_spaces * " ", subMod, " " * num_space, subMod_help))
        else:
            print("{}{}{}this is {} submodule.".format(pre_num_spaces * " ", subMod, " " * num_space, subMod))

    print('\nCommands:')
    for cmd in cmdList:
        num_space = int(max_name_len - len(cmd) + min_num_spaces)
        if cmd in dict_cmd_help and "" != dict_cmd_help[cmd]:
            cmd_help = dict_cmd_help[cmd]
            print("{}{}{}{}".format(pre_num_spaces * " ", cmd, " " * num_space, cmd_help))
        else:
            print("{}{}{}this is {} cmd.".format(pre_num_spaces * " ", cmd, " " * num_space, cmd))


# 版本号
def show_version():
    version_file_path = os.path.join(cli_bin_path, "version")
    with open(version_file_path, 'r') as pf:
        lines = pf.readlines()
        for line in lines:
            print(line.replace("\n", ""))


# 初始化group参数
def initGroupParams(args):
    global cmd_path
    global short_help
    global help_info
    global options_metavar
    global isSubModule
    global isCmd

    isSubModule, isCmd = is_submodule_or_cmd(args)
    # 初始化cli
    if isCmd:
        cmd_path = "{}/".format(code_dir_name)
    elif isSubModule:
        # submodule
        cmd_path = "{}/{}/".format(code_dir_name, args)

        if args in dict_cmd_help and "" != dict_cmd_help[args]:
            help_info = dict_cmd_help[args]
        else:
            help_info = "this is " + args + " submodule."
        options_metavar = args
    else:
        cust_print("submodule or command :【{}】 not found, please check!\n".format(sys.argv[1]), fg='r')
        show_help()
        sys.exit(1)


# 加载cmd和submodule
load_cmd_and_subMod()

# 子模块
if len(sys.argv) == 1:
    show_help()
    sys.exit(0)
elif len(sys.argv) == 2:
    if sys.argv[1] == "--version" or sys.argv[1] == "-v":
        show_version()
        sys.exit(0)
    elif sys.argv[1] == "--help" or sys.argv[1] == "-h":
        show_help()
        sys.exit(0)

# 初始化命令参数
initGroupParams(sys.argv[1])


# command group -------------------------------------------------------- ###
# 获取子模块命令
@click.group(cls=list_subMod_cmds_by_folderName(cmd_path),
             short_help=short_help,
             help=help_info,
             options_metavar=options_metavar)
def platon_cli_submodule():
    pass


# 直接获取命令
@click.group(cls=get_cmd_by_fileName(cmd_path, sys.argv[1]),
             short_help=short_help,
             help=help_info,
             options_metavar=options_metavar)
def platon_cli_cmd():
    pass


if __name__ == '__main__':
    if isSubModule:
        platon_cli_submodule()
    elif isCmd:
        platon_cli_cmd()
    else:
        pass
