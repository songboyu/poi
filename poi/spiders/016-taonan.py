# -*- coding: utf-8 -*-

from scrapy import Spider, Request
from poi.items import PoiItem



class TaonanSpider(Spider):
    name = 'taonan'
    allow_domains = ['51taonan.com']
    start_urls = [
        'http://www.51taonan.com/'
    ]

    def parse(self, response):
        for i in xrange(1880991, 15899999):

            yield  Request('http://www.51taonan.com/u_'+str(i) ,
                callback=self.parse_item,
                meta={'user_id': i})

    def parse_item(self, response):
        item = PoiItem()

        try:
            item['name'] = response.css('a.profile-netname h1::text').extract()[0]
            item['avatar'] = response.css('div.profile-user-img-box img::attr(src)').extract()[0]

            item['site_id'] = 16
            item['user_id'] = str(response.meta['user_id'])
            item['gender'] = 'M' if u'先生' in response.css('span#profile_sex::text').extract()[0] else 'F'
            item['occupation'] = response.css('span#profile_occupation::text').extract()[0]
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
            r = response.css('span#profile_education::text').extract()
            if r and r[0].strip()!=u'保密': item['education_level'] = education_level[r[0].strip()]
            item['height'] = response.css('span#profile_height::text').extract()[0]
            item['weight'] = response.css('span#profile_weight::text').extract()[0]
            bloodType = {
            u'O型':u'1',
            u'A型':u'2',
            u'B型':u'3',
            u'AB型':u'4',
            u'其他型':u'5'
            }
            r = response.css('span#profile_blood_type::text').extract()
            if r and r[0].strip()!=u'保密': item['blood_type'] = bloodType[r[0].strip()]
            marital_status = {
            u'已婚':u'M',
            u'未婚':u'S',
            u'离异':u'D',
            u'丧偶':u'W'
            }
            r = response.css('span#profile_marital::text').extract()
            if r and r[0].strip()!=u'保密': item['marital_status'] = marital_status[r[0].strip()]
            r = response.css('span#profile_income::text').extract()
            if r and r[0].strip()!=u'保密':item['salary'] =r[0].strip()
            r = response.css('span#profile_r_state_id a[target=_blank]::text').extract()
            if r and r[0].strip()!=u'保密':item['location'] = r[0].strip()
            item['hometown'] = response.css('span#profile_n_state_id::text').extract()[0]

        except:
            return

        return item
