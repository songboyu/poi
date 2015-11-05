# -*- coding: utf-8 -*-
import datetime

from scrapy import Spider, Request
from poi.items import PoiItem

class JiayuanSpider(Spider):
    name = 'jiayuan'
    allow_domains = ['www.jiayuan.com/']
    start_urls = [
        'http://www.jiayuan.com/110000000'
    ]

    def parse(self, response):
        for i in xrange(120000000, 217000000):
            yield  Request('http://www.jiayuan.com/' + str(i),
                callback=self.parse_item,
                meta={'user_id': i})

    def parse_item(self, response):
        item = PoiItem()

        try:
            item['name'] = response.css('h4::text').extract()[0]
            item['avatar'] = response.css('img.img_absolute::attr(_src)').extract()[0]
            # item['gender'] = 'M' if 'male' in response.css('div.portrait i::attr(class)').extract()[0] else 'F'

            # If name is available, then this item is valid.
            item['site_id'] = 6 # Site id of tianya.
            item['user_id'] = str(response.meta['user_id'])
        except:
            return
        item['score'] = int(response.css('h6::text').extract()[0])

        try:
            item['level'] = response.css('span.member_dj::text').extract()[0]
        except:
            item['level'] = ' '.join(response.css('span.member_dj a::attr(title)').extract())
        
        item['description'] = response.css('div.js_text::text').extract()[0]

        age, marital, location = response.css('h6.member_name::text').extract()[0].split(u'，')

        item['birthday'] = str(datetime.date.today().year - int(age[0:2])) + '-00-00'
        marital_status = {
            u'未婚':u'S',
            u'已婚':u'M',
            u'恋爱':u'L',
            u'分居':u'P',
            u'离异':u'D',
            u'离异,无小孩':u'D',
            u'离异,有小孩归对方':u'D',
            u'离异,有小孩归自己':u'D',
            u'丧偶':u'W',
            u'丧偶,无小孩':u'W',
            u'丧偶,有小孩归对方':u'W',
            u'丧偶,有小孩归自己':u'W',
        }
        item['marital_status'] = marital_status[marital]
        item['location'] = location[2:]

        education_level = {
            u'初中':u'1',
            u'高中':u'1',
            u'本科':u'4',
            u'双学士':u'5',
            u'硕士':u'5',
            u'小学':u'7',
            u'高中中专及以下':u'1',
            u'中专或相当学历':u'2',
            u'大专':u'3',
            u'博士':u'6',
            u'其他':u'7',
        }
        r = response.css('ul.member_info_list li')[0].css('em::text').extract()

        if r and r[0]!=u'--' and r[0]!=u'保密': item['education_level'] = education_level[r[0].strip()]

        r = response.css('ul.member_info_list li')[1].css('em::text').extract()
        if r and r[0]!=u'--' and r[0]!=u'保密': item['height'] = r[0]

        r = response.css('ul.member_info_list li')[3].css('em::text').extract()
        if r and r[0]!=u'--' and r[0]!=u'保密': item['salary'] = r[0]

        r = response.css('ul.member_info_list li')[5].css('em::text').extract()
        if r and r[0]!=u'--' and r[0]!=u'保密': item['weight'] = r[0]

        bloodType = {
            u'O型':u'1',
            u'A型':u'2',
            u'B型':u'3',
            u'AB型':u'4',
            u'其它':u'5'
        }
        r = response.css('ul.member_info_list li')[9].css('em::text').extract()

        if r and r[0]!=u'--' and r[0]!=u'保密': item['blood_type'] = bloodType[r[0].strip()]

        experience = ''
        r = response.css('div.js_box')[4]
        if r:
            for li in r.css('li.fn-clear'):
                if li.css('em::text').extract()[0] != '--':
                    experience += li.css('span::text').extract()[0]+li.css('em::text').extract()[0]+' '
            item['experience'] = experience
            # print experience

        return item
