# -*- coding: utf-8 -*-

from scrapy import Spider, Request
from poi.items import PoiItem

SESSION = '3721045b2924d22ce951534122ef8cd2edd7ff9b'

class DoubanSpider(Spider):
    name = 'douban'
    allow_domains = ['m.douban.com']
    start_urls = [
        'http://m.douban.com/'
    ]

    def parse(self, response):
        for i in xrange(4350000, 102500000):
            yield  Request('http://m.douban.com/people/' + str(i) + '/about?session=' + SESSION,
                callback=self.parse_item,
                meta={'user_id': i})

    def parse_item(self, response):
        item = PoiItem()

        try:
            item['name'] = response.css('a.founder::text').extract()[0]
            item['avatar'] = response.css('div.photo img::attr(src)').extract()[0]

            item['site_id'] = 8
            item['user_id'] = str(response.meta['user_id'])
        except:
            return

        r = response.css('div.info').re(ur'常居地：</span>(.*?)<')
        if r: item['location'] = r[0].strip()

        r = response.css('div.intro::text').extract()
        if r: item['description'] = r[0].strip()

        return item
