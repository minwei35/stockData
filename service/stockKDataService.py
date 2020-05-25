#! /usr/local/env python
# -*- encoding: utf-8 -*-

"""
@File  :  stockKDataService.py
@Time  :  2020-05-25 16:21
@Author  :  jeremesang
@Version :  V1.0
@Desc    :  股票K线数据服务类
"""

import time
import traceback
from multiprocessing import Pool, Manager

import baostock as bs
import pandas as pd
from sqlalchemy import func

from database import sqlUtils
from domain.stock import StockBasic, StockDataUpdateRecord, StockKData
from utils import dateUtils, stringUtils
from utils.stockLogger import StockLogger
from utils.configUtils import config

logger = StockLogger('stockService').get_logger()


def update_day_stock_by_code(queue):
    bs.login()
    today = dateUtils.get_day_k_data_time()
    count = 0
    while not queue.empty():
        try:
            session = sqlUtils.get_sqlalchemy_session()
            record = queue.get()
            start_date = record.update_daily_basic_date
            # 不存在最新的日期的话，则记录从2006-01-01开始的数据
            if stringUtils.is_blank(start_date):
                start_date = '2006-01-01'
            rs = bs.query_history_k_data_plus(code=str(record.code), fields=
                                              "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,"
                                              "tradestatus,pctChg,peTTM,pbMRQ,psTTM,pcfNcfTTM,isST",
                                              start_date=start_date, end_date=today)
            k_data_list = []
            while (rs.error_code == '0') & rs.next():
                # 获取一条记录，将记录合并在一起
                k_data_list.append(rs.get_row_data())
            df = pd.DataFrame(k_data_list, columns=rs.fields)
            logger.debug("股票代码为{}正在插入数据".format(record.code))
            if df is not None:
                d_len = df.shape[0]
                for index in range(d_len):
                    resu1 = df.iloc[index]
                    stock_k_data = StockKData.transfer(resu1)
                    session.merge(stock_k_data)
                logger.info("股票代码为{}插入数据完成".format(record.code))
                # 更新当前代码的最新更新日期
                update_record = StockDataUpdateRecord()
                update_record.code = record.code
                # 获取当前证券编号对应的最新日期
                update_daily_basic_date = session.query(func.max(StockKData.trade_date)).filter(
                    StockBasic.code == record.code).first()
                update_record.update_daily_basic_date = update_daily_basic_date[0]
                session.merge(update_record)
                session.commit()
                count = count + 1
                session.close()
        except Exception as e:
            # 或者得到堆栈字符串信息
            info = traceback.format_exc()
            logger.error("代码为{}的股票插入数据失败，失败信息为{}".format(record.code, info))
    logger.info("当前进程完成插入的数目是{}".format(count))
    return count


def update_k_data():
    now = time.time()
    # 创建会话
    my_session = sqlUtils.get_sqlalchemy_session()
    # 此处代码等价于
    # select from stock_basic b left join stock_data_update_record r on r.code = b.code
    # where b.type == 1 and b.status == 1
    record_list = my_session.query(StockBasic.code, StockDataUpdateRecord.update_daily_basic_date).outerjoin(
        StockDataUpdateRecord, StockDataUpdateRecord.code == StockBasic.code).filter(StockBasic.type == 1,
                                                                                     StockBasic.status == 1).all()
    my_session.close()
    m = Manager()
    q = m.Queue()
    before_count = 0
    for row in record_list:
        q.put(row)
        before_count = before_count + 1

    pool_count = config.pool_count
    p = Pool(processes=pool_count)
    result = []
    for i in range(pool_count):
        result.append(p.apply_async(update_day_stock_by_code, args=(q,)))
    logger.info("等待子进程完成数据插入")
    p.close()
    p.join()
    end = time.time()  # 结束计时
    total_time = end - now
    total_count = 0
    bs.logout()
    for sub_result in result:
        total_count = total_count + int(sub_result.get())
    logger.info("更新每日行情完成耗时：{:.2f}秒，本次更新{}条记录，成功更新{}条记录".format(total_time, before_count, total_count))
