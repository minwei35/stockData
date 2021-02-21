#! /usr/local/env python
# -*- encoding: utf-8 -*-

"""
@File  :  stockConceptService.py
@Time  :  2020-05-25 16:18
@Author  :  jeremesang
@Version :  V1.0
@Desc    :  股票概念板块及对应股票服务类
"""
import time
import traceback
from multiprocessing import Pool, Manager

from domain.stock import StockConcept, StockConceptDetails, StockCommonDetails

from scrapy.http import HtmlResponse
from selenium.common.exceptions import NoSuchElementException

from database import sqlUtils
from stockSpider.items import StockSpiderItemLoader, StockConceptDetailsItem, StockCommonDetailsItem
from utils import seleniumUtils
from utils.configUtils import config
from utils.stockLogger import StockLogger

logger = StockLogger('stockConceptService')


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
        根据爬虫得来的数据，运行selenium拼装插入数据库表中(概念对应的股票)
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
            # 判断当前页是否有数据, 如果第一个td是序号数字的话，才会执行
            if tr.xpath("td/text()").extract_first().strip().isdigit():
                item_loader = StockSpiderItemLoader(item=StockConceptDetailsItem(), selector=tr)
                item_loader.add_xpath("code", "td[2]/a/text()")
                stock_item = item_loader.load_item()
                stock_item['concept_code'] = gn_code
                concept_items.append(StockConceptDetails.transfer(stock_item))
                # 新增记录当前最新的涨跌幅和流通值
                data_item_loader = StockSpiderItemLoader(item=StockCommonDetailsItem(), selector=tr)
                data_item_loader.add_xpath("code", "td[2]/a/text()")
                data_item_loader.add_xpath("name", "td[3]/a/text()")
                data_item_loader.add_xpath("close", "td[4]/text()")
                data_item_loader.add_xpath("pct_change", "td[5]/text()")
                data_item_loader.add_xpath("price_change", "td[6]/text()")
                data_item_loader.add_xpath("turn", "td[8]/text()")
                data_item_loader.add_xpath("amplitude", "td[10]/text()")
                data_item_loader.add_xpath("amount", "td[11]/text()")
                data_item_loader.add_xpath("circulating_shares", "td[12]/text()")
                data_item_loader.add_xpath("circulating_marking_value", "td[13]/text()")
                data_item_loader.add_xpath("pe", "td[14]/text()")
                data_item = item_loader.load_item()
                stock_common = StockCommonDetails.transfer(data_item)
                session.merge(stock_common)
                session.commit()
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


def update_concept_data_multiprocess(queue):
    record = None
    count = 0
    browser = seleniumUtils.get_browser()
    url = config.concept_url
    while not queue.empty():
        try:
            record = queue.get()
            code = record.code
            update_stock_concept_details_by_spider(browser, url + code, code)
        except Exception as e:
            # 或者得到堆栈字符串信息
            info = traceback.format_exc()
            logger.error("代码为{}的股票插入数据失败，失败信息为{}".format(record.code, info))
    logger.info("当前进程完成插入的数目是{}".format(count))
    return count


def update_concept_data():
    start = time.time()
    # 创建会话
    session = sqlUtils.get_sqlalchemy_session()
    # 此处代码等价于
    # select from stock_basic b left join stock_data_update_record r on r.code = b.code
    # where b.type == 1 and b.status == 1
    record_list = session.query(StockConcept.code).all()
    session.close()
    manager = Manager()
    q = manager.Queue()
    before_count = 0
    for row in record_list:
        q.put(row)
        before_count = before_count + 1

    pool_count = config.pool_count
    pool = Pool(processes=pool_count)
    result = []
    for i in range(pool_count):
        result.append(pool.apply_async(update_concept_data_multiprocess, args=(q,)))
    logger.info("等待子进程完成数据插入")
    pool.close()
    pool.join()
    end = time.time()  # 结束计时
    total_time = end - start
    total_count = 0
    for sub_result in result:
        total_count = total_count + int(sub_result.get())
    logger.info("更新每日行情完成耗时：{:.2f}秒，本次更新{}条记录，成功更新{}条记录".format(total_time, before_count, total_count))