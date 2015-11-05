# -*- coding: utf-8 -*-

from scrapy import Spider, Request
from poi.items import PoiItem

class TianyaSpider(Spider):
    name = 'tianya'
    allow_domains = ['www.tianya.cn']
    start_urls = [
        'http://www.tianya.cn/0'
    ]

    def parse(self, response):
        for i in xrange(10450000, 10**8):
            yield  Request('http://www.tianya.cn/' + str(i),
                callback=self.parse_item,
                meta={'user_id': i})

    def parse_item(self, response):
        item = PoiItem()

        try:
            item['name'] = response.css('div.portrait img::attr(alt)').extract()[0]
            item['avatar'] = response.css('div.portrait img::attr(src)').extract()[0]
            item['gender'] = 'M' if 'male' in response.css('div.portrait i::attr(class)').extract()[0] else 'F'

            # If name is available, then this item is valid.
            item['site_id'] = 1 # Site id of tianya.
            item['user_id'] = str(response.meta['user_id'])
        except:
            return

        item['description'] = ''.join(response.css('div.profile p::text').extract())
        item['followers'] = int(response.css('div.link-box a::text').extract()[1])
        item['following'] = int(response.css('div.link-box a::text').extract()[0])
        item['score'] = int(response.css('div.userinfo').re(ur'分</span>(.*?)</p>')[0])
        item['login_num'] = int(response.css('div.userinfo').re(ur'登录次数</span>(.*?)</p>')[0])
        item['last_login_time'] = response.css('div.userinfo').re(ur'最新登录</span>(.*?)</p>')[0]
        item['reg_time'] = response.css('div.userinfo').re(ur'注册日期</span>(.*?)</p>')[0]

        # May not have location or level.
        r = response.css('div.userinfo').re(ur'区</span>(.*?)</p>')
        if r: item['location'] = r[0]
        r = response.css('div.userinfo').re(ur'_blank">(.*?)</a>')
        if r: item['level'] = r[0]

        # Inexistence indicats zero.
        r = response.css('div.mod-hd').re(ur'主贴(\d+)')
        item['post_num'] = int(r[0]) if r else 0
        r = response.css('div.mod-hd').re(ur'回帖(\d+)')
        item['reply_num'] = int(r[0]) if r else 0

        return item
