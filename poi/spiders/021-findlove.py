# -*- coding: utf-8 -*-

from scrapy import Spider, Request
from poi.items import PoiItem
import datetime
import re
import json

class RdaoSpider(Spider):
    name = 'findlove'
    allow_domains = ['www.51findlove.com/']
    start_urls = [
        'http://www.51findlove.com/'
    ]

    def parse(self, response):
        for i in xrange(100864, 126975):
            yield  Request('http://www.51findlove.cn/personal.php?uid='+str(i) ,
                callback=self.parse_item,
                meta={'user_id': i})

    def parse_item(self, response):
        item = PoiItem()

        name = response.xpath("//div[@class='pp_s']/p[1]/strong[1]/text()").extract()[0][0:-5-len(str(response.meta['user_id']))]
        info = response.xpath("//div[@class='pp_x']/ul[1]/li/text()").extract()




        try:
            item['name'] = name
            item['avatar'] ='http://www.51findlove.cn/'+ response.xpath("//div[@class='happ_img']/img/@src").extract()[0]
            # item['gender'] = 'M' if info[0]==u'男' else 'F'
            # If name is available, then this item is valid.
            item['site_id'] = 21 # Site id of 7rdao.
            item['user_id'] = str(response.meta['user_id'])
            # except:
            #     return

            # item['occupation']=info[6]

            marital_status = {
                u'未婚':u'S',
                u'离异':u'D',
                u'丧偶':u'W',
            }
            if info[4][5:] in marital_status:
                item['marital_status'] = marital_status[info[4][5:]]

            education_level = {
                u'高中':u'1',
                u'本科':u'4',
                u'硕士':u'5',
                u'中专':u'2',
                u'大专':u'3',
                u'博士':u'6',
                u'其他':u'7',
            }
            if info[2][3:] in education_level:
                item['education_level'] = education_level[info[2][3:]]
            item['height'] = info[1][3:]
            item['salary'] = info[5][3:]
            item['location'] = info[6][3:]
            item['birthday'] = str(datetime.date.today().year - int(info[0][3:-1])) + '-00-00'
            # if not u"Ta有点害羞,需要你的鼓励" in description:
            #     item['description'] ="".join(description.split())
        except:
            return
        return item
