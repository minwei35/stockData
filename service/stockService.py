#! /usr/local/env python
# -*- encoding: utf-8 -*-

"""
@File  :  stockService.py
@Time  :  2020-05-14 15:33
@Author  :  jeremesang
@Version :  V1.0
@Desc    :  股票列表数据服务类
"""

import baostock as bs
import pandas as pd
from domain.stock import StockBasic
from database import sqlUtils

from utils.stockLogger import StockLogger

logger = StockLogger('stockService')


def update_stock_all():
    bs.login()
    rs = bs.query_stock_basic()
    data_list = []
    while (rs.error_code == '0') & rs.next():
        # 获取一条记录，将记录合并在一起
        data_list.append(rs.get_row_data())
    data = pd.DataFrame(data_list, columns=rs.fields)
    # 创建会话
    session = sqlUtils.get_sqlalchemy_session()
    # 默认状态都先设为退市
    session.query(StockBasic).update({"status": 0})
    session.commit()
    d_len = data.shape[0]
    for i in range(d_len):
        row = data.iloc[i]
        stock_basic = StockBasic.tranfer(row)
        session.merge(stock_basic)
        session.commit()
    session.close()
    bs.logout()
    logger.info("股票列表已更新")

