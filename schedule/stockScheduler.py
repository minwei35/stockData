#! /usr/local/env python
# -*- encoding: utf-8 -*-

"""
@File  :  stockScheduler.py
@Time  :  2020-05-25 11:05
@Author  :  jeremesang
@Version :  V1.0
@Desc    :  stockData定时器
"""
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

from composite.stockComposite import StockComposite
from utils import stockLogger
from utils.configUtils import config

user = config.db_user_name
password = config.db_password
url = config.db_url


def k_data_scheduler():
    # stock_composite = StockComposite("k_data_scheduler")
    # stock_composite.run()
    print('进入到k线数据获取模式啦')


def runScheduler():
    # 定义定时器的logger
    scheduler_log = stockLogger("scheduler_log")
    # 使用sqlAlchemy把定时的job持久化到数据库中
    job_store = SQLAlchemyJobStore(url='oracle://{user}:{password}@{url}?encoding=utf-8&nencoding=utf-8'.format(user=user, password=password, url=url))
    scheduler = BlockingScheduler(jobstores=job_store, logger=scheduler_log)

    scheduler.add_job(k_data_scheduler, 'cron', day_of_week='mon-fri', hour=config.day_k_data_time, name="定时获取K线数据")
    # scheduler.add_job(k_data_scheduler, 'cron', day_of_week='mon-fri', hour=config.day_k_data_time, name="定时获取K线数据")
    # scheduler.add_job(usefulProxyScheduler, 'interval', minutes=1, id="useful_proxy_check", name="useful_proxy定时检查")
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass
