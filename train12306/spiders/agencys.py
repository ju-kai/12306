# -*- coding: utf-8 -*-
import json
import urllib
import time
import scrapy
from scrapy.http.request import Request
from train12306.items import AgencyItem
from train12306.items import CommitItem


class AgencysSpider(scrapy.Spider):
    name = 'AgentcysSpider'
#    start_urls = ['https://kyfw.12306.cn/otn/userCommon/allProvince']

    custom_settings = {
            'ITEM_PIPELINES': {
                'train12306.pipelines.AgencySQLPipeline': 300,
            },
#            'DUPEFILTER_DEBUG': True,
            'DOWNLOADER_MIDDLEWARES': {
                'train12306.middle.DownloaderMiddleware': 500,
            },
            #去除重复的url
            'DUPEFILTER_CLASS': "train12306.filter.URLTurnFilter",
            #断点续传，实现在网络掉线或人为停止scrapy后，下次启动后可以接着上次的下载进度继续下载
            'JOBDIR': "s/agencys",
    }

    def __init__(self, *a, **kw):
        super(AgencysSpider, self).__init__(self.name, **kw)
        # self.turn = a[0]
        #引入turn参数，意为轮次，用来判断下载的信息是在哪一次下载的
        turn = int(time.time() / 86400)
        self.turn = turn
        self.logger.info("%s. this turn %d" % (self.name, self.turn))

    def start_requests(self):
        #该url地址为代售点所有的省份信息
        yield Request("https://kyfw.12306.cn/otn/userCommon/allProvince", callback = self.parse, meta = {"turn":self.turn})

    def parse(self, response):
        url = "https://kyfw.12306.cn/otn/queryAgencySellTicket/query?"

        j = json.loads(response.body)
        #prov 例子为{"chineseName":"安徽","allPin":"","simplePin":"ah","stationTelecode":"34"}
        for prov in j["data"]:

            params = {"province":prov["chineseName"].encode("utf-8"), "city":"", "county":""}
            #s_url为组合后的新的url地址，改地址可以访问到各个省的所有代售点信息的json页面
    #s_url ：https://kyfw.12306.cn/otn/queryAgencySellTicket/query?province=%E5%90%89%E6%9E%97&city=&county=
            s_url = url + urllib.urlencode(params)
            yield Request(s_url, callback = self.parse_agency, meta = {"turn":response.meta["turn"]})

    def parse_agency(self, response):
        datas = json.loads(response.body)
        for data in datas["data"]["datas"]:
            item = AgencyItem()
            #省
            item["province"] = data["province"]
            #城市
            item["city"] = data["city"]
            #区县
            item["county"] = data["county"]
            #地址
            item["address"] = data["address"]
            #代售点名称
            item["name"] = data["agency_name"]
            #窗口数量
            item["windows"] = data["windows_quantity"]
            #营业开始时间
            item["start"] = data["start_time_am"]
            #营业结束时间
            item["end"] = data["stop_time_pm"]
            #轮次
            item["turn"] = response.meta["turn"]
            yield item
        yield CommitItem()


