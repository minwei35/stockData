#! /usr/local/env python
# -*- encoding: utf-8 -*-

"""
@File  :  SeleniumMiddleware.py
@Time  :  2020-05-15 10:52
@Author  :  jeremesang
@Version :  V1.0
@Desc    :  自定义下载中间件
"""
from scrapy.http import HtmlResponse

from stockSpider.request.SeleniumRequest import SeleniumRequest
from stockSpider.spiders.SeleniumSpider import SeleniumSpider


class SeleniumMiddleware(object):
    """
        下载器中间件
    """

    @classmethod
    def process_request(cls, request, spider):
        # 如果spider为SeleniumSpider的实例，并且request为SeleniumRequest的实例
        # 那么该Request就认定为需要启用selenium来进行渲染html
        if isinstance(spider, SeleniumSpider) and isinstance(request, SeleniumRequest):
            # 控制浏览器打开目标链接
            spider.browser.get(request.url)

            # 在构造渲染后的HtmlResponse之前，做一些事情
            # 1.比如等待浏览器页面中的某个元素出现后，再返回渲染后的html；
            # 2.比如将页面切换进iframe中的页面；
            spider.selenium_func(request)

            # 获取浏览器渲染后的html
            html = spider.browser.page_source

            # 构造Response
            # 这个Response将会被你的爬虫进一步处理
            return HtmlResponse(url=spider.browser.current_url, request=request, body=html.encode(), encoding="utf-8")
