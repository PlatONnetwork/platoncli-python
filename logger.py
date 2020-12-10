# _*_ coding:utf-8 _*_
"""
日志系统
"""
import os
import logging
from logging import Handler, FileHandler, StreamHandler
import time


def log_file_name_format():
    '''
    获取时间戳
    :return:
    时间戳字符串：如：20200528
    '''
    ct = time.time()
    local_time = time.localtime(ct)
    data_head = time.strftime("%Y%m%d", local_time)

    return data_head


class PathFileHandler(FileHandler):
    def __init__(self, path, filename, mode='a', encoding=None, delay=False):

        filename = os.fspath(filename)
        if not os.path.exists(path):
            os.mkdir(path)
        self.baseFilename = os.path.join(path, filename)
        self.mode = mode
        self.encoding = encoding
        self.delay = delay
        if delay:
            Handler.__init__(self)
            self.stream = None
        else:
            StreamHandler.__init__(self, self._open())


class Loggers(object):
    # 日志级别关系映射
    level_relations = {
        'debug': logging.DEBUG, 'info': logging.INFO, 'warning': logging.WARNING,
        'error': logging.ERROR, 'critical': logging.CRITICAL
    }

    def __init__(self, filename='platoncli{date}.log'.format(date=log_file_name_format()), level='info', log_dir='log'):
        fmt = '%(asctime)s - %(levelname)s - Operation: %(message)s'
        self.logger = logging.getLogger(filename)
        # abspath = os.path.dirname(os.path.abspath(__file__))
        # cli工具所在目录
        abspath = os.getcwd()
        self.directory = os.path.join(abspath, log_dir)
        format_str = logging.Formatter(fmt, "%Y-%m-%d %H:%M:%S")  # 设置日志格式
        self.logger.setLevel(self.level_relations.get(level))  # 设置日志级别
        # stream_handler = logging.StreamHandler()  # 往屏幕上输出
        # stream_handler.setFormatter(format_str)
        file_handler = PathFileHandler(path=self.directory, filename=filename, mode='a')
        file_handler.setFormatter(format_str)
        # self.logger.addHandler(stream_handler)
        self.logger.addHandler(file_handler)


g_logger = Loggers(level='info')


def setLogLevel(level="info"):
    g_logger.logger.setLevel(g_logger.level_relations.get(level))


# 写日志接口
def writeLog(msg, level="info"):
    if level == "info":
        g_logger.logger.info(msg)
    elif level == "debug":
        g_logger.logger.debug(msg)
    elif level == "warning":
        g_logger.logger.warning(msg)
    elif level == "error":
        g_logger.logger.error(msg)
    elif level == "critical":
        g_logger.logger.critical(msg)
    else:
        print("level:{} is invalid.".format(level))


if __name__ == "__main__":
    txt = "this is log test!"

    g_logger.logger.info(txt)
    g_logger.logger.debug(txt)
    g_logger.logger.error(txt)
