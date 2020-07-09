"""
author comger@gmail.com
统一日志处理
* 标准日志输出
    * Debug 模式下输出为控制台
    * 非Debug 模式下输出为文件及控制台
    * 日志文件可以自动按日志大小切分
"""
import os
import logging
import logging.handlers
from cms.core import config


# 最大日志保留数
B_COUNT = 8

# 日志等级
LEVELS = {'debug': logging.DEBUG,
          'info': logging.INFO,
          'warning': logging.WARNING,
          'error': logging.ERROR,
          'critical': logging.CRITICAL}


class Logger:
    """
    封装logging类
    >>level 可以输出的最低级别
    >>type    0:输出到前台和文件 1:输出到文件
    """

    def __init__(self, name='output', level=logging.DEBUG, type=0):
        path = os.getcwd() + "/logs"
        if not os.path.exists(path):
            os.mkdir(path)

        log_file = f"{path}/{name}.log"
        self._log = logging.getLogger(log_file)

        self._log.setLevel(level)
        lfh = logging.handlers.RotatingFileHandler(
            log_file, maxBytes=config.LOG_MAX_BYTES, backupCount=config.LOG_MAX_NUM)

        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s")

        lfh.setFormatter(formatter)

        self._log.addHandler(lfh)

        if type == 0:
            ch = logging.StreamHandler()
            ch.setFormatter(formatter)
            self._log.addHandler(ch)

    def getLogger(self):
        return self._log


logger = Logger().getLogger()