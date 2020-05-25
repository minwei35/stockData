#! /usr/local/env python
# -*- encoding: utf-8 -*-

"""
@File  :  stockData.py
@Time  :  2020-05-25 9:36
@Author  :  jeremesang
@Version :  V1.0
@Desc    :  主体入口
"""
from schedule import stockScheduler
import click
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version='1.0')
def cli():
    """stockData cli工具"""


@cli.command(name="test")
def test():
    click.echo('进入test方法')


@cli.command(name="schedule")
def schedule():
    click.echo('开始启动定时服务')
    stockScheduler.runScheduler()


if __name__ == '__main__':
    cli()
