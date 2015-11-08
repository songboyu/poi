# -*- coding: utf-8 -*-

from scrapy import Spider, Request
from poi.items import PoiItem
import datetime
import re
import json

class RdaoSpider(Spider):
    name = '7rdao'
    allow_domains = ['www.7rdao.com/']
    start_urls = [
        'http://www.7rdao.com/'
    ]

    def parse(self, response):
        for i in xrange(3081255, 3082256):
            yield  Request('http://www.7rdao.com/user2/'+str(i)+'.html' ,
                callback=self.parse_item,
                meta={'user_id': i})

    def parse_item(self, response):
        item = PoiItem()
        name = response.xpath("//div[@id='baseInfo']/dl/dd[2]/a/text()").extract()[0]
        info = response.xpath("//div[@id='baseInfo']/dl/dd/text()").extract()




        # try:
        item['name'] = name
        item['avatar'] = response.xpath("//a[@class='img']/img/@src").extract()[0]
        item['gender'] = 'M' if info[0]==u'男' else 'F'
        # If name is available, then this item is valid.
        item['site_id'] = 19 # Site id of 7rdao.
        item['user_id'] = str(response.meta['user_id'])
        # except:
        #     return

        item['occupation']=info[6]

        marital_status = {
            u'未婚':u'S',
            u'离异':u'D',
            u'丧偶':u'W',
        }
        if info[4] in marital_status:
            item['marital_status'] = marital_status[info[4]]

        education_level = {
            u'高中':u'1',
            u'大学本科':u'4',
            u'硕士':u'5',
            u'中专':u'2',
            u'大专':u'3',
            u'博士':u'6',
            u'其他':u'7',
        }
        if info[5] in education_level:
            item['education_level'] = education_level[info[5]]
        item['height'] = info[1]
        item['salary'] = info[7]
        item['location'] = info[8][0:-2]
        item['birthday'] = str(datetime.date.today().year - int(info[2])) + '-00-00'
        # if not u"Ta有点害羞,需要你的鼓励" in description:
        #     item['description'] ="".join(description.split())
        return item
