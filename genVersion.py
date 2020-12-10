# _*_ coding:utf-8 _*_
import subprocess
import time

from utility import CLI_VERSION


def get_time_stamp():
    '''
    获取时间戳
    :return:
    时间戳字符串：如：20200428
    '''
    ct = time.time()
    local_time = time.localtime(ct)
    data_head = time.strftime("%Y-%m-%d %H:%M:%S", local_time)

    return data_head


if __name__ == '__main__':
    commitid = str(subprocess.check_output(['git', 'rev-parse', 'HEAD']), encoding="utf-8")

    version_file = "version"
    version_info = ""
    with open(version_file, 'w') as pf:
        version = "version: " + CLI_VERSION + '\n'
        version_info = version
        pf.write(version)

        revision = "revision: " + commitid
        version_info = version_info + revision
        pf.write(revision)

        timestamp = "timestamp: " + get_time_stamp()
        version_info = version_info + timestamp
        pf.write(timestamp)

    print("生成版本信息文件成功:")
    print(version_info)
