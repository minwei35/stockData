#! /usr/local/env python
# -*- encoding: utf-8 -*-

"""
@File  :  component.py
@Time  :  2020-05-25 16:45
@Author  :  jeremesang
@Version :  V1.0
@Desc    :  函数执行组合的基类
"""


class Component:
    def __init__(self, name):
        self.composite_name = name

    def add(self, com):
        pass

    def run(self):
        pass
