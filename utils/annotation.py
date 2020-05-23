#! /usr/local/env python
# -*- encoding: utf-8 -*-

"""
@File  :  annotation.py
@Time  :  2020-05-22 16:30
@Author  :  jeremesang
@Version :  V1.0
@Desc    :  注解类
"""


class LazyProperty(object):
    """
    LazyProperty
    懒加载机制，避免多次访问
    """

    def __init__(self, func):
        self.func = func

    def __get__(self, instance, owner):
        if instance is None:
            return self
        else:
            value = self.func(instance)
            setattr(instance, self.func.__name__, value)
            return value

