#! /usr/local/env python
# -*- encoding: utf-8 -*-

"""
@File  :  stockService.py
@Time  :  2020-05-14 15:33
@Author  :  jeremesang
@Version :  V1.0
@Desc    :  股票数据服务类
"""
from database import sqlUtils
from mapper.stock import StockConcept


def update_stock_concept_by_spider(concept_list):
    """
    根据爬虫得来的数据，拼装插入数据库表中
    @param concept_list:
    @return:
    """
    session = sqlUtils.get_sqlalchemy_session()
    d_len = len(concept_list)
    for index in range(d_len):
        row = concept_list[index]
        stock_concept = StockConcept.transfer(row)
        session.merge(stock_concept)
    session.commit()
    session.close()
