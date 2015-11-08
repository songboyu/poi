# -*- coding: utf-8 -*-

from scrapy import Spider, Request
from poi.items import PoiItem
import datetime
import re
import json

class LoverSpider(Spider):
    name = 'jiandan'
    allow_domains = ['www.jjdd.me']
    start_urls = [
        'http://www.jjdd.me/'
    ]

    def parse(self, response):
        for i in xrange(23147, 63147):

            yield  Request('http://www.jjdd.me/'+str(i),
                callback=self.parse_item,
                meta={'user_id': i})

    def parse_item(self, response):
        item = PoiItem()


        if u'提示消息' == response.xpath("//title/text()").extract()[0]:
            print 'nnooooooooooooooooooo'
            return
        else:
            name = response.xpath("//title/text()").extract()[0][0:-5]

        info0 = response.xpath("//div[@class='person_basics']/div[1]/div[1]/dl").extract()

        # info = response.xpath("//div[@class='clear']/dl/dd/text()").extract()
        item['name'] = name
        item['avatar'] = response.xpath("//p[@class='per_img']/a/img/@src").extract()[0]
        # item['gender'] = 'M' if info[1]==u'男' else 'F'
        # If name is available, then this item is valid.
        item['site_id'] = 20 # Site id of
        item['user_id'] = str(response.meta['user_id'])
        # except:
        #     return
        if u'span'not in info0[6]:
            item['occupation']= info0[6][35:-10]

        marital_status = {
            u'未婚':u'S',
            u'离异':u'D',
            u'丧偶':u'W',
        }
        # if info[3] in marital_status:
        #     item['marital_status'] = marital_status[info[3]]

        education_level = {
            u'高中':u'1',
            u'大学本科':u'4',
            u'硕士':u'5',
            u'中专':u'2',
            u'大专':u'3',
            u'博士':u'6',
            u'其他':u'7',
        }
        if u'span'not in info0[7]:
            if info0[7][35:-10] in education_level:
                item['education_level'] = education_level[info0[7][35:-10]]
        if u'span'not in info0[1]:
            item['height'] = info0[1][35:-10]
        if u'span'not in info0[8]:
            item['salary'] = info0[8][35:-10]
        # item['weight'] = info[len(info)-6]
        # item['blood_type'] = info[len(info)-3]
        if u'span'not in info0[2]:
            item['location'] = info0[2][34:-10]
        if u'span'not in info0[0]:
            item['birthday'] = str(datetime.date.today().year - int(info0[0][35:-23])) + '-00-00'
        # if not u"Ta有点害羞,需要你的鼓励" in description:
        #     item['description'] ="".join(description.split())


        return item
