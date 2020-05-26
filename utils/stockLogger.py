#! /usr/local/env python
# -*- encoding: utf-8 -*-

"""
@File  :  stockLogger.py
@Time  :  2020-05-21 14:21
@Author  :  jeremesang
@Version :  V1.0
@Desc    :  日志输出模块
"""

import logging
import os
from logging.handlers import TimedRotatingFileHandler

from utils.configUtils import config

LOG_PATH = config.log_path
formatter = logging.Formatter('[%(asctime)s] %(filename)s->%(funcName)s line:%(lineno)d [%(levelname)s] %(message)s')
# 不存在日志目录就创建一个
if not os.path.exists(LOG_PATH):
    os.mkdir(LOG_PATH)


class StockLogger(logging.Logger):

    def __init__(self, name, level=config.logger_level, stream=True, file=True):
        self.name = name
        self.level = level
        logging.Logger.__init__(self, self.name, level=level)
        if stream:
            self.__setStreamHandler__()
        if file:
            self.__setFileHandler__()

    def __setFileHandler__(self, level=None):
        """
        设置日志保存的handler
        :param level:
        :return:
        """
        file_name = os.path.join(LOG_PATH, '{name}.log'.format(name=self.name))
        # 设置日志回滚, 保存在log目录, 一天保存一个文件, 保留15天
        file_handler = TimedRotatingFileHandler(filename=file_name, when='D', interval=1, backupCount=15)
        file_handler.suffix = '%Y%m%d.log'
        if not level:
            file_handler.setLevel(self.level)
        else:
            file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        self.file_handler = file_handler
        self.addHandler(file_handler)

    def __setStreamHandler__(self, level=None):
        """
        设置命令行日志
        :param level:
        :return:
        """
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        if not level:
            stream_handler.setLevel(self.level)
        else:
            stream_handler.setLevel(level)
        self.addHandler(stream_handler)
