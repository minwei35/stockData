#! /usr/local/env python
# -*- encoding: utf-8 -*-

"""
@File  :  stockComposite.py
@Time  :  2020-05-25 16:48
@Author  :  jeremesang
@Version :  V1.0
@Desc    :  股票类组合
"""
from composite.component import Component
from service import stockService, stockKDataService


class StockComposite(Component):
    def __init__(self, name):
        self.composite_name = name
        self.list = []

    def add(self, com):
        self.list.append(com)

    def run(self):
        for param in self.list:
            param.run()


class StockBasicComposite(Component):
    def __init__(self, name):
        self.composite_name = name

    def add(self, com):
        pass

    @staticmethod
    def run():
        # 执行更新股票基础信息
        stockService.update_stock_all()


class StockKDataComposite(Component):
    def __init__(self, name):
        self.composite_name = name

    def add(self, com):
        pass

    @staticmethod
    def run():
        # 执行更新股票K线信息
        stockKDataService.update_k_data()


stockRunComposite = StockComposite('股票执行组合')
stockRunComposite.add(StockBasicComposite('股票基础信息'))
stockRunComposite.add(StockKDataComposite('股票K线信息'))

