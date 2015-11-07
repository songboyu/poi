# -*- coding: utf-8 -*-
import datetime

from scrapy import Spider, Request
from poi.items import PoiItem

class GanjiSpider(Spider):
    name = 'ganji'
    allow_domains = ['love.ganji.com']

    def start_requests(self):
        for i in xrange(130000000, 131000000):
            yield  Request('http://love.ganji.com/' + str(i) + '.htm',
                callback=self.parse_item,
                meta={'user_id': i})

    def parse_item(self, response):
        item = PoiItem()

        try:
            item['name'] = response.css('div.z-xql span.mr-5::text').extract()[0]
            item['avatar'] = response.css('div.z-img img::attr(src)').extract()[0]

            item['site_id'] = 30
            item['user_id'] = str(response.meta['user_id'])
        except:
            return

        info = response.css('p.z-detail span')

        item['gender'] = 'M' if info[0].css('::text').extract()[0]==u'男' else 'F'

        item['birthday'] = str(datetime.date.today().year - int(info[1].css('::text').extract()[0])) + '-00-00'
        
        item['location'] = info[-1].css('::text').extract()[0][2:]

        info = response.css('div.z-subcon2 td.w2')

        # item['height'] = info[0].css('span::text').extract()[0]

        education_level = {
            u'初中':u'1',
            u'中专/职高/技校':u'2',
            u'高中及以下':u'1',
            u'大专以下':u'2',
            u'大专':u'3',
            u'本科':u'4',
            u'硕士':u'5',
            u'博士':u'6',
            u'博士后':u'6',
            }
        # print info[1].css('span::text').extract()[0]
        r = info[1].css('span::text').extract()
        if r: item['education_level'] = education_level[r[0].strip()]

        marital_status = {
            u'已婚':u'M',
            u'未婚':u'S',
            u'离异':u'D',
            u'离异单身':u'D',
            u'离异带孩':u'D',
            u'丧偶':u'W',
            u'丧偶单身':u'W',
            u'丧偶带孩':u'W'
            }
        # print info[2].css('span::text').extract()[0]
        r = info[2].css('span::text').extract()
        if r and r[0]!=u'未填写': item['education_level'] = marital_status[r[0].strip()]

        item['description'] = response.css('div.z-db')[0].css('::text').extract()[0]
        return item
