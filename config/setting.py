#! /usr/local/env python
# -*- encoding: utf-8 -*-

"""
@File  :  setting.py
@Time  :  2020-05-22 17:31
@Author  :  jeremesang
@Version :  V1.0
@Desc    :  配置项
"""
import logging
import os

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
ROOT_PATH = os.path.join(CURRENT_PATH, os.pardir)
LOG_PATH = os.path.join(ROOT_PATH, 'log')

""" 数据库配置 """
DATABASES = {
    "TYPE": "ORACLE",
    "URL": "192.168.10.80:1521/orcl",
    "USERNAME": "stock",
    "PASSWORD": "stock"
}

""" 通用配置 """
COMMON = {
    # baostock的api在当前交易日17:30，完成日K线数据入库；本程序则是18点后进行日k数据入库
    "DAY_K_DATA_TIME": "18",
    # baostock的api在当前交易日20:30，完成分钟K线数据入库；本程序则是21点后进行分钟K数据入库
    "MINUTE_K_DATA_TIME": "21",
    # 多进程池的进程数
    "POOL_COUNT": "8"
}

""" selenium配置项 """
SELENIUM = {
    "HEADLESS": True,
    "CONCEPT_URL": 'http://q.10jqka.com.cn/gn/detail/code/',
    "CHROME_DRIVER": "chromedriver.exe"
}

""" 日志配置项 """
LOGGER = {
    "LEVEL": logging.DEBUG,
    "LOG_PATH": LOG_PATH
}

""" 函数执行顺序 """
FUNCTION_GETTER = {
    "test"
}
