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
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class SeleniumSpider(scrapy.Spider):
    """
    Selenium专用spider

    一个spider开一个浏览器

    各大浏览器webdriver地址可参见：https://docs.seleniumhq.org/download/
    Firefox：https://github.com/mozilla/geckodriver/releases/
    Chrome：http://chromedriver.storage.googleapis.com/index.html
    """

    def parse(self, response):
        pass

    # 浏览器是否设置无头模式，仅测试时可以为False
    SetHeadless = False

    # 是否允许浏览器使用cookies
    EnableBrowserCookies = True

    def __init__(self, *args, **kwargs):
        super(SeleniumSpider, self).__init__(*args, **kwargs)

        # 获取浏览器操控权
        self.browser = self._get_browser()

    def _get_browser(self):
        """
        返回浏览器实例
        """
        # 设置selenium与urllib3的logger的日志等级为ERROR
        # 如果不加这一步，运行爬虫过程中将会产生一大堆无用输出
        logging.getLogger('selenium').setLevel('ERROR')
        logging.getLogger('urllib3').setLevel('ERROR')

        # selenium已经放弃了PhantomJS，开始支持firefox与chrome的无头模式
        return self._use_chrome()

    def _use_chrome(self):
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
        if self.SetHeadless:
            # 无头模式，无UI
            options.add_argument('-headless')

        # 禁用gpu加速
        options.add_argument('--disable-gpu')

        return webdriver.Chrome(options=options)

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
