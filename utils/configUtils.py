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
    def chrome_driver(self):
        return SELENIUM.get("CHROME_DRIVER", "chromedriver.exe")

    @LazyProperty
    def headless(self):
        return SELENIUM.get("HEADLESS", True)

    @LazyProperty
    def logger_level(self):
        return LOGGER.get("LEVEL", logging.INFO)

    @LazyProperty
    def log_path(self):
        return LOGGER.get("LOG_PATH", logging.INFO)

    @LazyProperty
    def day_k_data_time(self):
        return int(COMMON.get("DAY_K_DATA_TIME", 18))

    @LazyProperty
    def minute_k_data_time(self):
        return int(COMMON.get("MINUTE_K_DATA_TIME", 21))

    @LazyProperty
    def pool_count(self):
        return int(COMMON.get("POOL_COUNT", 8))

    @LazyProperty
    def concept_url(self):
        return SELENIUM.get("CONCEPT_URL", '')


config = Config()

if __name__ == '__main__':
    print(config.db_type)
    print(config.db_url)
    print(config.db_password)
