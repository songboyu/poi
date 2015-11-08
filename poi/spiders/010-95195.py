# -*- coding: utf-8 -*-
import re
import datetime
from scrapy import Spider, Request
from poi.items import PoiItem

class _95195Spider(Spider):
    name = '95195'
    allow_domains = ['www.95195.com/']

    def start_requests(self):
        for i in xrange(14000000, 100000000):
            yield  Request('http://www.95195.com/zone/index/' + str(i),
                callback=self.parse_item,
                meta={'user_id': i})

    def parse_item(self, response):
        item = PoiItem()

        try:
            item['name'] = response.css('p.nametit b::text').extract()[0]

            # If name is available, then this item is valid.
            item['site_id'] = 10 # Site id of tianya.
            item['user_id'] = str(response.meta['user_id'])
        except:
            return

        item['avatar'] = response.css('img#changesize::attr(src)').extract()[0]
        item['gender'] = 'M' if u'男' in response.css('p.nametit span::text').extract()[0] else 'F'
        item['birthday'] = str(datetime.date.today().year - int(re.findall(r'(\d+)', response.css('p.nametit span::text').extract()[0])[0])) + '-00-00'

        text = response.css('div.font12::text').extract()[0].replace('&nbsp;','').split('/')
        item['location'] = text[0].strip()
        item['height'] = text[1].strip()
        education_level = {
            u'专科以下':u'1',
            u'专科':u'3',
            u'本科':u'4',
            u'硕士':u'5',
            u'博士':u'6',
            u'博士后':u'6',
        }
        item['education_level'] = education_level[text[2].strip()]
        item['occupation'] = text[3].strip().replace(u'职业：','')
        desc = response.css('p#updateDesc span::text').extract()[0]
        if desc != u'评论一下嘛…' and desc!= u'在照片上写点什么':
            item['description'] = desc

        r = response.css('p.nametit b img').extract()
        if r: 
            item['level'] = '认证'
        else:
            item['level'] = '未认证'

        return item
