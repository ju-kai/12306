# -*- coding: utf-8 -*-
import json
import urllib
import time
import scrapy
from scrapy.http.request import Request
from train12306.items import StationItem
from train12306.items import CommitItem

class StationsSpider(scrapy.Spider):
    name = 'StationsSpider'
#    start_urls = ['http://www.12306.cn/mormhweb/kyyyz/']

    custom_settings = {
            'ITEM_PIPELINES': {
                'train12306.pipelines.StationSQLPipeline': 300,
            },
            'DOWNLOADER_MIDDLEWARES': {
                'train12306.middle.DownloaderMiddleware': 500,
            },
            'DUPEFILTER_CLASS': "train12306.filter.URLTurnFilter",
            'JOBDIR': "s/stations",
    }

    def __init__(self, *a, **kw):
        super(StationsSpider, self).__init__(self.name, **kw)
        # self.turn = a[0]
        turn = int(time.time()/86400)
        self.turn = turn
        self.logger.info("%s. this turn %d" % (self.name, self.turn))

    def start_requests(self):
        #该url 进入到12306客运营业站站点页面
        yield Request("http://www.12306.cn/mormhweb/kyyyz/", callback = self.parse, meta = {"turn":self.turn})

    def parse(self, response):
        #通过css选择器获得各个铁路局的名称
        names = response.css("#secTable > tbody > tr > td::text").extract()
        #获得客运站车站和客运站乘降所的相对url地址
        sub_urls = response.css("#mainTable td.submenu_bg > a::attr(href)").extract()
        # print sub_urls
        for i in range(0, len(names)):
            #获得客运站乘降所的相对url地址
            sub_url1 = response.url + sub_urls[i * 2][2:]
            yield Request(sub_url1, callback = self.parse_station, meta = {'bureau':names[i], 'station':True, "turn":response.meta["turn"]})
            # 获得客运站车站的相对url地址
            sub_url2 = response.url + sub_urls[i * 2 + 1][2:]
            yield Request(sub_url2, callback = self.parse_station, meta = {'bureau':names[i], 'station':False, "turn":response.meta["turn"]})

    def parse_station(self, response):
        #datas为某铁路局的客运站车站表格内数据
        datas = response.css("table table tr")
        #表头占两行，所有判断datas是否小于2，如果小于2，则该表内容为空
        if len(datas) <= 2:
            return
        for i in range(0, len(datas)):
            if i < 2:
                continue
            infos = datas[i].css("td::text").extract()

            item = StationItem()
            #铁路局名称
            item["bureau"] = response.meta["bureau"]
            item["station"] = response.meta["station"]
            #站点名称
            item["name"] = infos[0]
            #车站地址
            item["address"] = infos[1]
            #旅客乘降
            item["passenger"] = infos[2].strip() != u""
            #行李
            item["luggage"] = infos[3].strip() != u""
            #包裹
            item["package"] = infos[4].strip() != u""
            #轮次
            item["turn"] = response.meta["turn"]
            yield item
        yield CommitItem()




