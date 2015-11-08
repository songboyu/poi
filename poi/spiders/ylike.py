# -*- coding: utf-8 -*-

from scrapy import Spider, Request
from poi.items import PoiItem




class YlikeSpider(Spider):
    name = 'ylike'
    allow_domains = ['ylike.com']
    start_urls = [
        'http://www.ylike.com/'
    ]

    def parse(self, response):
        for i in xrange(15357385, 15899999):


            yield  Request('http://www.ylike.com/User/'+str(i)+'/',
                callback=self.parse_item,
                meta={'user_id': i})

    def parse_item(self, response):
        item = PoiItem()

        try:

            user_name = response.css('dl.dl02 dt::text').extract()[0]

            item['name'] = user_name
            item['avatar'] = response.css('img#myImagePhoto_mid::attr(src)').extract()[0]
            item['site_id'] = 17
            item['user_id'] = str(response.meta['user_id'])
            item['gender'] = 'M' if u'男' in response.css('dl.dl02 dd.d01::text').extract()[0] else 'F'
            item['occupation'] = response.css('dl.dl02 dd.d02::text').extract()[0]
            education_level = {
            u'初中':u'1',
            u'中专/职高/技校':u'3',
            u'高中':u'1',
            u'大专':u'2',
            u'本科':u'4',
            u'硕士':u'5',
            u'博士':u'6',
            u'博士后':u'6',
            }
            r = response.css('dl.dl02 dd.d01::text').extract()
            if r and r[8].strip()!=u'保密': item['education_level'] = education_level[r[8].strip()]
            item['height'] = response.css('dl.dl02 dd.d01::text').extract()[4]

            marital_status = {
            u'已婚':u'M',
            u'单身':u'S',
            u'未婚':u'S',
            u'离异':u'D',
            u'丧偶':u'W'
            }
            r = response.css('dl.dl02 dd.d01::text').extract()
            if r and r[3].strip()!=u'保密': item['marital_status'] = marital_status[r[3].strip()]
            r = response.css('dl.dl02 dd.d02::text').extract()
            if r and r[0].strip()!=u'保密':item['salary'] =r[2].strip()
            r = response.css('dl.dl02 dd.d01::text').extract()
            if r and r[0].strip()!=u'保密':item['location'] = r[2].strip()
            item['body_size'] = response.css('dl.dl02 dd.d01::text').extract()[5]
            item['looks'] = response.css('dl.dl02 dd.d01::text').extract()[6]


        except:
            return

        return item
