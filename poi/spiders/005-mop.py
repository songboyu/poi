# -*- coding: utf-8 -*-
import time
import json

from scrapy import Spider
from scrapy.http import Request,FormRequest
from poi.items import PoiItem

class MopSpider(Spider):
    name = 'mop'
    allow_domains = ['hi.mop.com']

    start_urls = [
        'http://hi.mop.com/space/410000000/profile'
    ]

    def parse(self, response):
        for i in xrange(423900000, 520000000):
            yield Request('http://hi.mop.com/space/'+str(i)+'/profile', 
                    callback=self.parse_item, 
                    meta={'user_id': i},
                    priority=10)

    def parse_item(self, response):
        item = PoiItem()
        try:
            item['name'] = response.css('ul.hpUserInfoUl li')[0].css('div.oh::text').extract()[0]
            item['avatar'] = response.css('img.br4::attr(src)').extract()[0]

            # If name is available, then this item is valid.
            item['site_id'] = 5 # Site id of tianya.
            item['user_id'] = str(response.meta['user_id'])
        except:
            return 

        r = response.css('ul.hpUserInfoUl li')[1].css('div.oh::text').extract()
        if r: item['location'] = r[0]

        r = response.css('ul.hpUserInfoUl li')[2].css('div.oh::text').extract()
        if r: item['gender'] = 'M' if u'男' in r[0] else 'F'

        r = response.css('ul.hpUserInfoUl li')[3].css('div.oh::text').extract()
        if r and r[0]!=u'无': item['birthday'] = r[0].replace(u' 年 ','-').replace(u' 月 ','-').replace(u' 日','')

        item['login_num'] = response.css('ul.hpUserInfoUl li')[4].css('div.oh::text').extract()[0]

        r = response.css('ul.hpUserInfoUl li')[5].css('div.oh::text').extract()
        if r and r[0]!=u'无': item['last_login_time'] = r[0]

        r = response.css('ul.hpUserInfoUl li')[6].css('div.oh::text').extract()
        if r: item['description'] = r[0]

        item['score'] = int(response.css('div.user-sns-count li')[3].css('a.num::attr(title)').extract()[0])
        item['level'] = response.css('div.user-sns-count li')[2].css('a.num::text').extract()[0] + u'级 - ' + response.css('div.levelBox div::text').extract()[-1]

        item['reg_time'] = response.css('div.hpUserInfo2 span.c999::text').extract()[0]

        return FormRequest(
            'http://hi.mop.com/ajax/get',
            headers = {
                'X-Requested-With':'XMLHttpRequest'
            },
            formdata = {'data':json.dumps({'header':{},'req':{'User/SubCount':{'uid':item['user_id']},'User/SnsCount':{'uid':item['user_id']}}}),
                        'date': str(int(time.time()*1000))
            },
            callback = self.parse_item_get_ajax,
            meta={'item': item},
            priority=20,
        )

    def parse_item_get_ajax(self, response):
        item = response.meta['item']
        data = json.loads(response.body)

        item['followers'] = data['resp']['User/SnsCount']['retObj']['fans']
        item['following'] = data['resp']['User/SnsCount']['retObj']['follow']

        item['post_num'] = data['resp']['User/SubCount']['retObj']['subject']
        item['reply_num'] = data['resp']['User/SubCount']['retObj']['reply']

        return item
