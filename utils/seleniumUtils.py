#! /usr/local/env python
# -*- encoding: utf-8 -*-

"""
@File  :  seleniumUtils.py
@Time  :  2020-05-20 15:10
@Author  :  jeremesang
@Version :  V1.0
@Desc    :  selenium工具类
"""
import logging
from selenium import webdriver
from utils.configUtils import config

# 浏览器是否设置无头模式，仅测试时可以为False
SetHeadless = config.headless

# 是否允许浏览器使用cookies
EnableBrowserCookies = True


def get_browser():
    """
    返回浏览器实例
    """
    # 设置selenium与urllib3的logger的日志等级为ERROR
    # 如果不加这一步，运行爬虫过程中将会产生一大堆无用输出
    logging.getLogger('selenium').setLevel('ERROR')
    logging.getLogger('urllib3').setLevel('ERROR')

    # selenium已经放弃了PhantomJS，开始支持firefox与chrome的无头模式
    return use_chrome()


def use_chrome():
    """
    使用selenium操作谷歌浏览器
    """
    options = webdriver.ChromeOptions()

    # 下面一系列禁用操作是为了减少selenium的资源耗用，加速scrapy

    profile = {
        'profile.default_content_setting_values': {
            # 禁用图片
            'images': 2,
            # 禁用浏览器弹窗
            'notifications': 2
        }
    }
    options.add_experimental_option('prefs', profile)

    # 默认是无头模式，意思是浏览器将会在后台运行，也是为了加速scrapy
    # 调试的时候可以把SetHeadless设为False，看一下跑着爬虫时候，浏览器在干什么
    if SetHeadless:
        # 无头模式，无UI
        options.add_argument('-headless')

    # 禁用gpu加速
    options.add_argument('--disable-gpu')

    return webdriver.Chrome(executable_path="chromedriver.exe", options=options)
