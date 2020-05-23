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


class StockLogger:
    logger = None

    def __init__(self, class_name):
        self.logger = logging.getLogger(class_name)
        self.logger.setLevel(logging.DEBUG)
        # 建立一个streamHandler来把日志打在CMD窗口上
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        # 设置日志格式
        formatter = logging.Formatter('[%(asctime)s] %(filename)s->%(funcName)s line:%(lineno)d [%(levelname)s]%(message)s')
        ch.setFormatter(formatter)
        # 将相应的handler添加在logger对象中
        self.logger.addHandler(ch)

    def get_logger(self):
        return self.logger
