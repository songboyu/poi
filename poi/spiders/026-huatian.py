# -*- coding: utf-8 -*-
import datetime

from scrapy import Spider, Request
from poi.items import PoiItem

class HuatianSpider(Spider):
    name = 'huatian'
    allow_domains = ['love.163.com']

    def start_requests(self):
        for i in xrange(5000000, 6000000):
            yield  Request('http://love.163.com/' + str(i),
                callback=self.parse_item,
                meta={'user_id': i})

    def parse_item(self, response):
        item = PoiItem()

        try:
            item['name'] = response.css('span#profileVerifyName::text').extract()[0]
            item['avatar'] = response.css('a.photo-trigger img::attr(src)').extract()[0]

            item['site_id'] = 26
            item['user_id'] = str(response.meta['user_id'])
        except:
            return

        info = response.css('div.profile-basic-info-left span')
        item['gender'] = 'M' if info[0].css('::text').extract()[0]==u'男' else 'F'

        item['birthday'] = str(datetime.date.today().year - int(info[1].css('em::text').extract()[0])) + '-00-00'

        item['height'] = info[2].css('em::text').extract()[0] + 'cm'

        item['location'] = info[3].css('::text').extract()[0]

        item['score'] = int(response.css('span.js-totalPercent::text').extract()[0])
        return item
