# -*- coding: utf-8 -*-
import scrapy
import re

from stockSpider.items import StockSpiderItem, StockSpiderItemLoader, StockConceptDetailsItem
from service import stockConceptService
from stockSpider.request.SeleniumRequest import SeleniumRequest
from stockSpider.spiders.SeleniumSpider import SeleniumSpider


class StockSpider(SeleniumSpider):
    name = 'stock'
    allowed_domains = ['q.10jqka.com.cn']
    start_urls = ['http://q.10jqka.com.cn/gn/']

    def start_requests(self):
        url = 'http://q.10jqka.com.cn/gn/'
        yield scrapy.Request(url)

    def parse(self, response):
        item_nodes = response.xpath("//div[@class='cate_items']/a")
        gn_items = []
        for item_node in item_nodes:
            # 根据item文件中所定义的字段内容，进行字段内容的抓取
            item_loader = StockSpiderItemLoader(item=StockSpiderItem(), selector=item_node)
            item_loader.add_xpath("gn_name", "text()")
            item_loader.add_xpath("gn_url", "@href")

            stock_item = item_loader.load_item()
            # 示例链接：http://q.10jqka.com.cn/gn/detail/code/301558/，只需要提取code后面的值
            # 使用正则表达式获取code/和/之前的值
            codes = re.findall(r"code/(.+?)/", stock_item['gn_url'])
            # 正则表达式匹配成功，并且值不为空时替换
            if codes:
                stock_item['gn_code'] = codes[0]
            gn_items.append(stock_item)
        stockConceptService.update_stock_concept_by_spider(gn_items)
        for index in range(len(gn_items)):
            # 循环执行每个概念的关联关系爬虫
            stockConceptService.update_stock_concept_details_by_spider(self.browser, gn_items[index]['gn_url'], gn_items[index]['gn_code'])

    # 暂时弃用，改成stockService.update_stock_concept_details_by_spider方法进行爬取，待优化
    def gn_page_parse(self, response):
        table_tr = response.xpath('/html/body/table/tbody/tr')
        item = response.meta["item"]
        page_num = int(response.meta["page_num"])
        page_size = int(response.meta["page_size"])
        if page_size == -1:
            page_total = response.xpath('//*[@id="m-page"]/span/text()').extract_first()
            if page_num:
                page_size = int(page_total.split('/')[1])
        son_items = response.meta["son_items"]
        for tr in table_tr:
            item_loader = StockSpiderItemLoader(item=StockConceptDetailsItem(), selector=tr)
            item_loader.add_xpath("code", "td[2]/a/text()")
            stock_item = item_loader.load_item()
            stock_item['concept_code'] = item['gn_code']
            son_items.append(stock_item)
            print(stock_item)
        if page_num < page_size:
            url = 'http://q.10jqka.com.cn/gn/detail/field/264648/order/desc/page/{}/ajax/1/code/{}'.format(page_num + 1,item['gn_code'])
            yield SeleniumRequest(url=url, callback=self.gn_page_parse, method="GET",
                                  meta={"item": item, "son_items": son_items, "page_num": page_num + 1, "page_size": page_size})

    def selenium_func(self, request):
        # 这个方法会在我们的下载器中间件返回Response之前被调用
        # 等待页面的ajax加载的带分页的html内容成功后，再继续
        # 这样的话，我们就能在gn_page_parse方法里用选择器筛出正常的table了
        self.waitForXpath(self.browser, '//*[@id="m-page"]')
