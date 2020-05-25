#! /usr/local/env python
# -*- encoding: utf-8 -*-

"""
@File  :  stockComposite.py
@Time  :  2020-05-25 16:48
@Author  :  jeremesang
@Version :  V1.0
@Desc    :  股票类组合
"""
from composite import component


class StockComposite(component):
    def __init__(self, name):
        self.composite_name = name
        self.list = []

    def add(self, com):
        self.list.append(com)

    def run(self):
        for param in self.list:
            param.run()
