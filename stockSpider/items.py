# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst


class StockSpiderItemLoader (ItemLoader):
    # 自定义itemloader,用于存储爬虫所抓取的字段内容
    default_output_processor = TakeFirst()


class StockSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    gn_name = scrapy.Field()
    gn_url = scrapy.Field()
    gn_code = scrapy.Field()
    pass


class StockConceptDetailsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    concept_code = scrapy.Field()
    code = scrapy.Field()
    pass


class StockCommonDetailsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    code = scrapy.Field()
    name = scrapy.Field()
    close = scrapy.Field()
    pct_change = scrapy.Field()
    price_change = scrapy.Field()
    turn = scrapy.Field()
    amplitude = scrapy.Field()
    amount = scrapy.Field()
    circulating_shares = scrapy.Field()
    circulating_marking_value = scrapy.Field()
    pe = scrapy.Field()
    pass
