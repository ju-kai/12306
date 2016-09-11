# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html


import scrapy


class CommitItem(scrapy.Item):
    pass

#轮次  对应数据库turns
class TurnItem(scrapy.Item):
    id = scrapy.Field()
    mark = scrapy.Field()


#客运代售点信息 对应数据库agencys数据库
class AgencyItem(scrapy.Item):
    #省
    province = scrapy.Field()
    #城市
    city = scrapy.Field()
    #区县
    county = scrapy.Field()
    #代售点地址
    address = scrapy.Field()
    #代售点名称
    name = scrapy.Field()
    #代售点数量
    windows = scrapy.Field()
    #营业开始时间
    start = scrapy.Field()
    #营业结束时间
    end = scrapy.Field()
    #轮次
    turn = scrapy.Field()


#客运营业站点信息 对应数据库stations
class StationItem(scrapy.Item):
    #铁路局名称
    bureau = scrapy.Field()
    #客运站车站
    station = scrapy.Field()
    #站名
    name = scrapy.Field()
    #车站地址
    address = scrapy.Field()
    #旅客乘降
    passenger = scrapy.Field()
    #行李
    luggage = scrapy.Field()
    #包裹
    package = scrapy.Field()
    #轮次
    turn = scrapy.Field()


#列车线路信息  对应数据库 train_briefs
class BriefItem(scrapy.Item):
    #车次
    code = scrapy.Field()
    #车次编号
    train_no = scrapy.Field()
    #起始站点
    start = scrapy.Field()
    #终点站
    end = scrapy.Field()
    #轮次
    turn = scrapy.Field()

#列车时刻表信息 对应数据库train_infos
class InfoItem(scrapy.Item):
    #车次编号
    train_no = scrapy.Field()
    #站点数量编号（某天线路上的第几站）
    no = scrapy.Field()
    #站点名称
    station = scrapy.Field()
    #发车时间
    start_time = scrapy.Field()
    #到达时间
    arrive_time = scrapy.Field()

    stopover_time = scrapy.Field()
    #座位类型
    seat_type = scrapy.Field()
    #轮次
    turn = scrapy.Field()


class BriefDeltaItem(scrapy.Item):
    code = scrapy.Field()
    seat_type = scrapy.Field()
    turn = scrapy.Field()

#列车站点信息 对应数据库train_stations
class CodeItem(scrapy.Item):
    #站点
    name = scrapy.Field()
    #站点英文编号（例如 上海SHH）
    code = scrapy.Field()
    #轮次
    turn = scrapy.Field()

#余票信息
class TicketItem(scrapy.Item):
    #车次编号
    train_no = scrapy.Field()
    #起始站
    start = scrapy.Field()
    #到达站
    end = scrapy.Field()
    #商务座
    swz = scrapy.Field()
    #特等座
    tz = scrapy.Field()
    #一等座
    zy = scrapy.Field()
    #二等座
    ze = scrapy.Field()
    #高级软卧
    gr = scrapy.Field()
    #软卧
    rw = scrapy.Field()
    #硬卧
    yw = scrapy.Field()
    #软座
    rz = scrapy.Field()
    #硬座
    yz = scrapy.Field()
    #无座
    wz = scrapy.Field()
    #其他
    qt = scrapy.Field()
    #轮次
    turn = scrapy.Field()
