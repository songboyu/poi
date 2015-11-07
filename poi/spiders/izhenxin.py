# -*- coding: utf-8 -*-
import datetime
import json

from scrapy import Spider, Request
from poi.items import PoiItem

class IzhenxinSpider(Spider):
    name = 'izhenxin'
    allow_domains = ['www.izhenxin.com']

    def start_requests(self):
        for i in xrange(531700000, 531800000, 10):
            yield  Request('http://www.izhenxin.com/user/getUserInfo/?oid=' + str(i),
                callback=self.parse_item,
                meta={'user_id': i})

    def parse_item(self, response):
        item = PoiItem()
        j = json.loads(response.body)['data']
        if not j['uid']: return
        try:
            item['name'] = j['nick']
            item['avatar'] = j['avatar_150']

            # If name is available, then this item is valid.
            item['site_id'] = 25 # Site id of tianya.
            item['user_id'] = str(response.meta['user_id'])
        except:
            return
        age = j['age'][0:-1]
        try:
            item['birthday'] = str(datetime.date.today().year - int(age)) + '-00-00'
        except:
            pass

        item['height'] = j['height']
        item['description'] = j['intro']
        item['location'] = j['location']
        item['salary'] = j['salary']
        item['gender'] = 'M' if j['sex']=='1' else 'F'
        education_level = {
            u'初中':u'1',
            u'中专/职高/技校':u'2',
            u'高中/中专':u'2',
            u'大专以下':u'2',
            u'大专':u'3',
            u'本科':u'4',
            u'硕士':u'5',
            u'博士':u'6',
            u'博士后':u'6',
        }
        print j['education']
        item['education_level'] = education_level[j['education'].strip()]
        return item
