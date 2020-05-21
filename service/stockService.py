#! /usr/local/env python
# -*- encoding: utf-8 -*-

"""
@File  :  stockService.py
@Time  :  2020-05-14 15:33
@Author  :  jeremesang
@Version :  V1.0
@Desc    :  股票数据服务类
"""
import time

from mapper.stock import StockConcept, StockConceptDetails
import logging

from scrapy.http import HtmlResponse
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

from database import sqlUtils
from stockSpider.items import StockSpiderItemLoader, StockConceptDetailsItem
from utils.stockLogger import StockLogger

logger = StockLogger('stockService').get_logger()


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


def update_stock_concept_details_by_spider(browser, url, gn_code):
    """
        根据爬虫得来的数据，拼装插入数据库表中(概念对应的股票)
        @param browser: selenium浏览器实例
        @param url: 链接
        @param gn_code: 概念编号
        @return:
    """
    logger.debug('开始爬取概念编号%s对应的股票信息', gn_code)
    have_next = True
    session = sqlUtils.get_sqlalchemy_session()
    logger.debug('正在删除概念编号%s对应的股票信息', gn_code)
    session.query(StockConceptDetails).filter(StockConceptDetails.gn_code == gn_code).delete()
    session.commit()
    logger.debug('删除完成')
    browser.get(url)
    concept_items = []
    # 循环下一页，直至尾页
    while have_next:
        # 获取浏览器渲染后的html
        html = browser.page_source
        # 构造Response
        # 这个Response将会被进一步处理
        response = HtmlResponse(url=url, body=html.encode(), encoding="utf-8")
        table_tr = response.xpath('//*[@id="maincont"]/table/tbody/tr')
        for tr in table_tr:
            item_loader = StockSpiderItemLoader(item=StockConceptDetailsItem(), selector=tr)
            item_loader.add_xpath("code", "td[2]/a/text()")
            stock_item = item_loader.load_item()
            stock_item['concept_code'] = gn_code
            concept_items.append(StockConceptDetails.transfer(stock_item))
        try:
            # 在页面中查找是否还有下一页
            next_page = browser.find_element_by_link_text("下一页")
            if next_page:
                have_next = True
                # 有下一页则点击，等待2秒后获取渲染后的结果
                next_page.click()
                logger.debug('发现概念%s有下一页的按钮，点击并等待5s', gn_code)
                time.sleep(5)
                # browser.implicitly_wait(5)
            else:
                have_next = False
        # 如果找不到对应的下一页的元素，会抛出NoSuchElementException，捕获并跳出循环
        except NoSuchElementException:
            have_next = False
        # except StaleElementReferenceException:
        #     have_next = False
    logger.debug('开始插入爬取的概念编号%s对应的股票信息', gn_code)
    session.add_all(concept_items)
    session.commit()
    logger.debug('插入成功')
    session.close()
