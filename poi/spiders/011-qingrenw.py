# -*- coding: utf-8 -*-
import re
import datetime
from scrapy import Spider, Request
from poi.items import PoiItem

class _95195Spider(Spider):
    name = 'qingrenw'
    allow_domains = ['www.qingrenw.com']

    def start_requests(self):
        for i in xrange(5000000, 54000000):
            yield  Request('http://www.qingrenw.com/user1/' + str(i) + '.html',
                callback=self.parse_item,
                meta={'user_id': i})

    def parse_item(self, response):
        item = PoiItem()
        root = response.xpath('//html')
        try:
            item['name'] = response.css('dd.nickname a::text').extract()[0]

            # If name is available, then this item is valid.
            item['site_id'] = 11 # Site id of tianya.
            item['user_id'] = str(response.meta['user_id'])
        except:
            return

        item['avatar'] = response.css('a.img img::attr(src)').extract()[0]
        item['gender'] = 'M' if u'男' in response.css('dd.f::text').extract()[0] else 'F'
        birthday = root.re(ur'出生年月.*?(\d+)')[0]
        item['birthday'] = birthday[:4] + '-' + birthday[4:] + '-00'
        item['height'] = root.re(ur'(\d+)</dd><dt>年龄：')[0]

        marital_status = {
            u'未婚':u'S',
            u'非单身':u'L',
            u'离异':u'D',
            u'丧偶':u'W'
        }
        r = root.re(ur'婚姻状况：</dt><dd class="f">(.*?)</dd><dt>')
        if r: item['marital_status'] = marital_status[r[0].strip()]

        education_level = {
            u'初中':u'1',
            u'高中':u'1',
            u'本科':u'4',
            u'硕士':u'5',
            u'中专':u'2',
            u'专科':u'3',
            u'博士':u'6',
        }
        r = root.re(ur'最高学历：</dt><dd>(.*?)</dd><dt>')
        if r: item['education_level'] = education_level[r[0].strip()]

        r = root.re(ur'从事职业：</dt><dd class="f">(.*?)</dd><dt>')
        if r: item['occupation'] = r[0].strip()

        r = root.re(ur'年收入：</dt><dd>(.*?)</dd><dt>')
        if r: item['salary'] = r[0].strip()

        r = root.re(ur'现居住地：</dt><dd class="f">(.*?)</dd><dt>')
        if r: item['location'] = re.sub(r'<(.*?)>','',r[0]).strip()

        r = root.re(ur'最后在线时间：(\d+-\d+-\d+ \d+:\d+:\d+)')
        if r: item['last_login_time'] = r[0].strip()

        r = root.re(ur'自我介绍：</b>(.*?)</li>')
        if r: item['description'] = r[0].strip()

        r = root.re(ur'<li><b>我的个性：</b>(.*?)</li>')
        if r: item['personality'] = r[0].strip()

        r = root.re(ur'<li><b>兴趣爱好：</b>(.*?)</li>')
        if r: item['favorites'] = r[0].strip()

        r = root.re(ur'<li><b>我的外貌：</b>(.*?)</li>')
        if r: item['looks'] = r[0].strip()

        r = root.re(ur'诚信值:(\d+)')
        if r: item['score'] = int(r[0].strip())

        r = root.re(ur'(\d+)</span></dd><dt>性别：')
        if r: item['level'] = r[0].strip()

        return item
