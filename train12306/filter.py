# -*- coding: utf-8 -*-


import logging
from scrapy.dupefilters import RFPDupeFilter

logger = logging.getLogger()

#继承scrapy自带的类RFPDupeFilter，实现对url的过滤功能
class URLTurnFilter(RFPDupeFilter):
    def request_fingerprint(self, request):
        #当turn已经存在于meta中，则返回请求的url加本次抓取的轮次数，避免在同一轮次中对相同url的重复请求
        if "turn" in request.meta:
            return request.url + ("-- %d" % request.meta["turn"])

        else:
            return request.url
