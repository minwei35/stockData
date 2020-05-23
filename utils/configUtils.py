#! /usr/local/env python
# -*- encoding: utf-8 -*-

"""
@File  :  configUtils.py
@Time  :  2020-05-21 16:37
@Author  :  jeremesang
@Version :  V1.0
@Desc    :  获取配置项
"""
from config.setting import *
from utils.annotation import LazyProperty


class Config(object):
    """
    get config
    """

    def __init__(self):
        pass

    @LazyProperty
    def db_type(self):
        return DATABASES.get("TYPE", "ORACLE")

    @LazyProperty
    def db_user_name(self):
        return DATABASES.get("USERNAME", "")

    @LazyProperty
    def db_url(self):
        return DATABASES.get("URL", "")

    @LazyProperty
    def db_password(self):
        return DATABASES.get("PASSWORD", "")

    @LazyProperty
    def headless(self):
        return SELENIUM.get("HEADLESS", True)


config = Config()

if __name__ == '__main__':
    print(config.db_type)
    print(config.db_url)
    print(config.db_password)
