# -*- coding: utf-8 -*-
import time
import datetime
import json
import urllib

import scrapy
from scrapy.http.request import Request
from train12306.items import BriefItem
from train12306.items import InfoItem
from train12306.items import TurnItem
from train12306.items import CommitItem

class ScheduleSpider(scrapy.Spider):
    name = 'ScheduleSpider'
    #start_urls = ['https://kyfw.12306.cn/otn/queryTrainInfo/getTrainName']

    custom_settings = {
            'ITEM_PIPELINES': {
                'train12306.pipelines.TrainSQLPipeline': 300,
            },
            'DOWNLOADER_MIDDLEWARES': {
                'train12306.middle.DownloaderMiddleware': 500,
            },
            #通过对url判断来实现过滤掉已经下载过的url地址
            'DUPEFILTER_CLASS': "train12306.filter.URLTurnFilter",
            #断点续传，实现在网络掉线或人为停止scrapy后，下次启动后可以接着上次的下载进度继续下载
            'JOBDIR': "s/schedule",
    }

    def __init__(self, *a, **kw):
        super(ScheduleSpider, self).__init__(self.name, **kw)
        # self.turn = a[0]
        #引入turn参数，意为轮次，用来判断下载的信息是在哪一次下载的
        turn = int(time.time() / 86400)
        self.turn = turn
        self.logger.info("%s. this turn %d" % (self.name, self.turn))

    def start_requests(self):

        url = "https://kyfw.12306.cn/otn/queryTrainInfo/getTrainName?"
        #获得当前系统时间
        n = datetime.datetime.now()
        #获得当前时间后的第三天，并将其转换为年月日的格式 例如：2016-08-03
        t = (n + datetime.timedelta(days = 3)).strftime("%Y-%m-%d")
        params = {"date":t}
        #s_url : https://kyfw.12306.cn/otn/queryTrainInfo/getTrainName?date=2016-08-02,某一天所有的车次
        s_url = url + urllib.urlencode(params)

        yield Request(s_url, callback = self.parse, meta = {"t":t, "turn":self.turn})

    def parse(self, response):
        datas = json.loads(response.body)
        url = "https://kyfw.12306.cn/otn/czxx/queryByTrainNo?"
        #data 形式例如 {"station_train_code":"G2(上海虹桥-北京南)","train_no":"5l000000G230"}
        for data in datas["data"]:
            item = BriefItem()
            briefs = data["station_train_code"].split("(")
            #车次编号 比如5l000000G230
            item["train_no"] = data["train_no"]
            #车次 例如G2
            item["code"] = briefs[0]
            briefs = briefs[1].split("-")
            #起始站
            item["start"] = briefs[0]
            #终点站
            item["end"] = briefs[1][:-1]
            #轮次
            item["turn"] = response.meta["turn"]
            yield item

            params = u"train_no=" + data["train_no"] + u"&from_station_telecode=BBB&to_station_telecode=BBB&depart_date=" + response.meta["t"]
    #该url+params例为：https://kyfw.12306.cn/otn/czxx/queryByTrainNo?train_no=5l000000G230&from_station_telecode=BBB&to_station_telecode=BBB&depart_date=2016-08-02
            yield Request(url + params, callback = self.parse_train_schedule, meta = {"train_no":data["train_no"], "turn":response.meta["turn"]})

    def parse_train_schedule(self, response):
        stations = json.loads(response.body)

        datas = stations["data"]["data"]
        size = len(datas)
        for i in range(0, size):
            data = datas[i]

            info = InfoItem()
            #车次编号
            info["train_no"] = response.meta["train_no"]
            #站点编号
            info["no"] = int(data["station_no"])
            #站点名称
            info["station"] = data["station_name"]
            #轮次
            info["turn"] = response.meta["turn"]
            #发车时间
            if data["start_time"] != u"----":
                info["start_time"] = data["start_time"] + u":00";
            else:
                info["start_time"] = None
            #到达时间
            if data["arrive_time"] != u"----":
                info["arrive_time"] = data["arrive_time"] + u":00";
            else:
                info["arrive_time"] = None

            stop = data["stopover_time"]
            if stop != u"----":
                if stop.endswith(u"分钟"):
                    info["stopover_time"] = u"00:" + stop[:stop.find(u"分钟")] + u":00";
                else:
                    info["stopover_time"] = stop + u":00";
            else:
                info["stopover_time"] = None

            yield info
        yield CommitItem()




