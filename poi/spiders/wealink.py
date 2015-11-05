# -*- coding: utf-8 -*-
import re
import datetime
from scrapy import Spider, Request
from poi.items import PoiItem

class wealinkSpider(Spider):
    name = 'wealink'
    allow_domains = ['www.wealink.com/']

    def start_requests(self):
        for i in xrange(10000000, 59500000):
            yield  Request('http://www.wealink.com/dangan/'+str(i),
                callback=self.parse_item,
                meta={'user_id': i})

    def parse_item(self, response):
        item = PoiItem()
        root = response.xpath('//html')
        try:
            name = response.css('div.card-photo a::attr(title)').extract()[0]
            if name.strip() == '':
                return
            item['name'] = name

            # If name is available, then this item is valid.
            item['site_id'] = 14 # Site id of tianya.
            item['user_id'] = str(response.meta['user_id']) 
        except:
            return

        r = response.css('div.card-photo img::attr(src)').extract()
        if r: item['avatar'] = r[0]

        experience = ''
        r = response.css('ul.card-info a.clr-333::attr(title)').extract()
        if r:  experience += ' '.join(r)

        r = root.re(ur'<li><span class="clr-999">工作经验：</span>(.*?)</li>')
        if r:  experience += r[0]

        item['experience'] = experience


        r = response.css('ul.card-info li')[-2].css('a::text').extract()
        if r:
            item['followers'] = int(r[0].strip())
            item['following'] = int(r[1].strip())

        r = root.re(ur'<li><span class="clr-999">性　　别：</span>(.*?)</li>')
        if r and r[0].strip() != '': item['gender'] = 'M' if u'男' in r[0].strip() else 'F'

        r = root.re(ur'<li><span class="clr-999">年　　龄：</span>([\s\S]*?)</li>')
        if r and r[0].strip() != '': 
            r = re.findall(r'\((.*?)\)', r[0].strip())
            if r:
                birthday = r[0]
                if len(birthday) < 10:
                    item['birthday'] = u'0000-'+birthday
                else:
                    item['birthday'] = birthday

        r = root.re(ur'<li><span class="clr-999">身　　高：</span>[\s]*(.+)')
        if r and r[0].strip() != '': item['height'] = r[0].strip()

        r = root.re(ur'<li><span class="clr-999">居 住 地 ：</span>(.*?)</li>')
        if r and r[0].strip() != '': item['location'] = r[0].strip()

        r = root.re(ur'<li><span class="clr-999">户　　籍：</span>(.*?)</li>')
        if r and r[0].strip() != '': item['hometown'] = r[0].strip()

        r = root.re(ur'<li><span>体育爱好：</span>(.*?)</li>')
        if r and r[0].strip() != '': item['favorites'] = r[0].strip()

        marital_status = {
            u'已婚':u'M',
            u'未婚':u'S'
        }
        r = root.re(ur'<li><span class="clr-999">婚姻状况：</span>(.*?)</li>')
        if r and r[0].strip()!=u'保密': item['marital_status'] = marital_status[r[0].strip()]

        education_level = {
            u'初中':u'1',
            u'高中':u'1',
            u'中技':u'2',
            u'中专':u'2',
            u'大专':u'3',
            u'本科':u'4',
            u'硕士':u'5',
            u'MBA':u'5',
            u'博士':u'6',
        }
        r = root.re(ur'<li><span class="clr-999">最高学历：</span>(.*?)</li>')
        if r: item['education_level'] = education_level[r[0].strip()]

        r = response.css('p.clr-333::text').extract()
        if r: item['description'] = r[0]
        return item
