# -*- coding: utf-8 -*-
import re
import datetime
from scrapy import Spider, Request
from poi.items import PoiItem

class EasyDongSpider(Spider):
    name = 'easydong'
    allow_domains = ['www.easydong.com/']

    def start_requests(self):
        for i in xrange(2000000, 100000000):
            yield  Request('http://www.easydong.com/index.php/space/'+str(i),
                callback=self.parse_item,
                meta={'user_id': i})

    def parse_item(self, response):
        item = PoiItem()
        root = response.xpath('//html')
        try:
            name = response.css('div#member_messages h3 a::text').extract()[0]
            if name == u'编辑' or name == '':
                return
            item['name'] = name

            # If name is available, then this item is valid.
            item['site_id'] = 13 # Site id of tianya.
            item['user_id'] = str(response.meta['user_id'])
        except:
            return
        desc = response.css('div#member_messages h3 span::text').extract()[0].strip()
        if desc != '':
            item['description'] = desc

        avatar = response.css('div.face a img::attr(src)').extract()[0]
        if avatar[0:4] == 'http': 
            item['avatar'] = avatar
        else:
            item['avatar'] = 'http://www.easydong.com' + avatar

        r = root.re(ur'<li><span>性别：</span>(.*?)</li>')
        if r and r[0].strip() != '': item['gender'] = 'M' if u'男' in r[0] else 'F'

        r = root.re(ur'<li><span>生日：</span>(.*?)</li>')
        if r and r[0].strip() != '': 
            birthday = r[0].strip()
            if len(birthday) < 10:
                item['birthday'] = u'0000-'+birthday
            else:
                item['birthday'] = birthday

        r = root.re(ur'<li><span>易动积分：</span>(\d+)</li>')
        if r and r[0].strip() != '': item['score'] = int(r[0].strip())

        r = root.re(ur'<li><span>运动主场：</span>(.*?)</li>')
        if r and r[0].strip() != '': item['location'] = r[0].strip()

        r = root.re(ur'<li><span>体育爱好：</span>(.*?)</li>')
        if r and r[0].strip() != '': item['favorites'] = r[0].strip()

        return item
