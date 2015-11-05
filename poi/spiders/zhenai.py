# -*- coding: utf-8 -*-

from scrapy import Spider, Request
from poi.items import PoiItem
import datetime
import re
import json

class ZhenaiSpider(Spider):
    name = 'zhenai'
    allow_domains = ['www.zhenai.com/']
    start_urls = [
        'http://album.zhenai.com/'
    ]

    def parse(self, response):
        for i in xrange(72610000, 72620000):
            yield  Request('http://album.zhenai.com/profile/getmemberdata.jsps?memberid=' + str(i),
                callback=self.parse_item,
                meta={'user_id': i})

    def parse_item(self, response):
        item = PoiItem()
        pattern = re.compile('memberInfo : \$.parseJSON\(\'(.*?)\'\),',re.S)
        result = re.search(pattern,response.body.decode('gbk'))
        ans=json.loads(result.group(1))
        pattern_description = re.compile('<p class="fs14 lh20 c5e slider-area-js">(.*?)<span class="info-mark"></span></p>',re.S)
        description=re.search(pattern_description,response.body.decode('gbk')).group(1)
        try:
            item['name'] = ans["fullName"]
            item['avatar'] = ans["photo"]
            item['gender'] = 'M' if ans["sex"]==0 else 'F'
            # If name is available, then this item is valid.
            item['site_id'] = 9 # Site id of zhenai.
            item['user_id'] = str(response.meta['user_id'])
        except:
            return

        item['occupation']=ans["occupation"]

        marital_status = {
            u'未婚':u'S',
            u'离异':u'D',
            u'丧偶':u'W',
        }
        if ans["marriage"] in marital_status:
            item['marital_status'] = marital_status[ans["marriage"]]

        education_level = {
            u'高中及以下':u'1',
            u'大学本科':u'4',
            u'硕士':u'5',
            u'中专':u'2',
            u'大专':u'3',
            u'博士':u'6',
            u'其他':u'7',
        }
        if ans["education"] in education_level:
            item['education_level'] = education_level[ans["education"]]
        item['height'] = ans["height"]
        item['occupation'] = ans["occupation"]
        item['salary'] = ans["salary"]
        item['location'] = ans["workCity"]
        item['birthday'] = str(datetime.date.today().year - int(ans["age"])) + '-00-00'
        if not u"Ta有点害羞,需要你的鼓励" in description:
            item['description'] ="".join(description.split())
        return item
