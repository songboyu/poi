# -*- coding: utf-8 -*-

from scrapy import Spider, Request
from poi.items import PoiItem
import datetime
import re
import json

class LoverSpider(Spider):
    name = '51lover'
    allow_domains = ['www.51lover.org']
    start_urls = [
        'http://www.51lover.org'
    ]

    def parse(self, response):
        for i in xrange(1068478, 7068478):

            yield  Request('http://www.51lover.org/perinfo-id-'+str(i)+'.htm',
                callback=self.parse_item,
                meta={'user_id': i})

    def parse_item(self, response):
        item = PoiItem()




        try:
            name = response.xpath("//div[@class='tit']/h1/text()").extract()[0]
            # info = response.xpath("//div[@id='pertagContent0']/table/tr/td/span/text()").extract()
            info = response.xpath("//table[@width='633']/tr/td/span/text()").extract()
            item['name'] = name
            # item['avatar'] = response.xpath("//div[@class='box02']/img/@src").extract()[0]
            item['gender'] = 'M' if info[1]==u'男' else 'F'
            # If name is available, then this item is valid.
            item['site_id'] = 29 # Site id of 7rdao.
            item['user_id'] = str(response.meta['user_id'])
            # except:
            #     return

            item['occupation']=info[5]

            marital_status = {
                u'未婚':u'S',
                u'离异':u'D',
                u'丧偶':u'W',
            }
            if info[3] in marital_status:
                item['marital_status'] = marital_status[info[3]]

            education_level = {
                u'高中':u'1',
                u'大学本科':u'4',
                u'硕士':u'5',
                u'中专':u'2',
                u'大专':u'3',
                u'博士':u'6',
                u'其他':u'7',
            }
            if info[6] in education_level:
                item['education_level'] = education_level[info[6]]
            item['height'] = info[len(info)-7]
            item['weight'] = info[len(info)-6]
            item['blood_type'] = info[len(info)-3]
            item['salary'] = info[len(info)-9]
            item['location'] = info[4]
            item['birthday'] = str(datetime.date.today().year - int(info[2][0:-1])) + '-00-00'
            # if not u"Ta有点害羞,需要你的鼓励" in description:
            #     item['description'] ="".join(description.split())
        except:
            return
        return item
