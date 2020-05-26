#! /usr/local/env python
# -*- encoding: utf-8 -*-

"""
@File  :  SeleniumSpider.py
@Time  :  2020-05-15 15:21
@Author  :  jeremesang
@Version :  V1.0
@Desc    :  None
"""
import functools
import logging
import scrapy
from selenium import webdriver
from utils import seleniumUtils
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class SeleniumSpider(scrapy.Spider):
    """
    Selenium专用spider

    一个spider开一个浏览器

    各大浏览器webdriver地址可参见：https://docs.seleniumhq.org/download/
    Firefox：https://github.com/mozilla/geckodriver/releases/
    国内源： http://npm.taobao.org/mirrors/geckodriver/
    Chrome：http://chromedriver.storage.googleapis.com/index.html
    国内源：http://npm.taobao.org/mirrors/chromedriver/
    """

    def parse(self, response):
        pass

    # 浏览器是否设置无头模式，仅测试时可以为False
    SetHeadless = True

    # 是否允许浏览器使用cookies
    EnableBrowserCookies = True

    def __init__(self, *args, **kwargs):
        super(SeleniumSpider, self).__init__(*args, **kwargs)

        # 获取浏览器操控权
        self.browser = seleniumUtils.get_browser()

    def selenium_func(self, request):
        """
        在返回浏览器渲染的html前做一些事情
            1.比如等待浏览器页面中的某个元素出现后，再返回渲染后的html；
            2.比如将页面切换进iframe中的页面；

        在需要使用的子类中要重写该方法，并利用self.browser操作浏览器
        """
        pass

    def closed(self, reason):
        # 在爬虫关闭后，关闭浏览器的所有tab页，并关闭浏览器
        self.browser.quit()

        # 日志记录一下
        self.logger.info("selenium已关闭浏览器...")

    def waitFor(browser, select_arg, select_method, timeout=2):

        """
        阻塞等待某个元素的出现直到timeout结束

        :param browser:浏览器实例
        :param select_method:所使用的选择器方法
        :param select_arg:选择器参数
        :param timeout:超时时间
        :return:
        """
        element = WebDriverWait(browser, timeout).until(
            EC.presence_of_element_located((select_method, select_arg))
        )

    # 用xpath选择器等待元素
    waitForXpath = functools.partial(waitFor, select_method=By.XPATH)

    # 用css选择器等待元素
    waitForCss = functools.partial(waitFor, select_method=By.CSS_SELECTOR)
