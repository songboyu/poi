# -*- coding: utf-8 -*-

from scrapy import Spider, Request
from poi.items import PoiItem
import datetime
import re
import json

class RdaoSpider(Spider):
    name = 'showse'
    allow_domains = ['www.showse.com/']
    start_urls = [
        'http://www.showse.com/'
    ]

    def parse(self, response):
        for i in xrange(1204712, 1586595):
            yield  Request('http://www.showse.com/MyHome.asp?userid='+str(i) ,
                callback=self.parse_item,
                meta={'user_id': i})

    def parse_item(self, response):
        item = PoiItem()
        info = response.xpath("//div[@id='jibenxinxi']/p/text()").extract()

        info2 = response.xpath("//table[1]/tr[1]/td[1]/table[1]/tr/td[2]/text()").extract()



        try:
            item['name'] = info[0][3:]
            item['avatar'] = response.xpath("//div[@id='bigface']/div/img/@src").extract()[0]
            item['gender'] = 'M' if info[3][3:]==u'男' else 'F'
            # If name is available, then this item is valid.
            item['site_id'] = 23 # Site id of 7rdao.
            item['user_id'] = str(response.meta['user_id'])
            # except:
            #     return

            item['occupation']=info[6][3:]

            marital_status = {
                u'未婚':u'S',
                u'离异':u'D',
                u'丧偶':u'W',
            }
            if info2[0] in marital_status:
                item['marital_status'] = marital_status[info2[0]]

            education_level = {
                u'高中':u'1',
                u'大学本科':u'4',
                u'硕士':u'5',
                u'中专':u'2',
                u'大专':u'3',
                u'博士':u'6',
                u'其他':u'7',
            }
            if info2[3] in education_level:
                item['education_level'] = education_level[info2[3]]
            item['height'] = info2[1]
            item['salary'] = info2[6]
            item['location'] = info[5][3:]
            item['birthday'] = str(datetime.date.today().year - int(info[4][3:-1])) + '-00-00'
            # if not u"Ta有点害羞,需要你的鼓励" in description:
            #     item['description'] ="".join(description.split())
        except:
            return
        return item
