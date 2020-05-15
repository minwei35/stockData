#! /usr/local/env python
# -*- encoding: utf-8 -*-

"""
@File  :  SeleniumRequest.py
@Time  :  2020-05-15 15:26
@Author  :  jeremesang
@Version :  V1.0
@Desc    :  用来在DownloadMiddleware中定义会使用selenium进行解析的请求
"""

import scrapy


class SeleniumRequest(scrapy.Request):
    """
    selenium专用Request类
    """
    pass
