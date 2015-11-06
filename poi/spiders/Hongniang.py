# -*- coding: utf-8 -*-
import re
import datetime
from scrapy import Spider, Request
from poi.items import PoiItem

class HongniangSpider(Spider):
    name = 'hongniang'
    allow_domains = ['profile.baihe.com']

    def start_requests(self):
        for i in xrange(300000, 400000):
            yield  Request('http://www.hongniang.com/?mod=member&mid='+str(i),
                callback=self.parse_item,
                meta={'user_id': i})

    def parse_item(self, response):
        item = PoiItem()
        
        html = response.body.decode('gbk')
        try:
            item['name'] = re.findall(ur'我是<em>(.*?)<\/em>', html)[0]
            item['avatar'] = 'http://www.hongniang.com' + response.css('a.da-pic img::attr(src)').extract()[0]
            # If name is available, then this item is valid.
            item['site_id'] = 22 # Site id of tianya.
            item['user_id'] = str(response.meta['user_id'])
        except:
            return
        try: 
            item['hometown'] = re.findall(ur'>(.*?)</a></strong>人', html)[0] 
        except: 
            pass

        try: 
            age = re.findall(ur'今年<em>(\d+)岁</em>', html)[0]
            item['birthday'] = str(datetime.date.today().year - int(age)) + '-00-00' 
        except: 
            pass

        try: 
            item['height'] = re.findall(ur'身高<strong style=" color: #FB8B38">(.*?)</strong>', html)[0] 
        except: 
            pass

        try: 
            item['location'] = re.findall(ur'工作在<strong ><a target="_blank" style=" color:#5E83EF; font-weight:bold;">(.*?)<', html)[0] 
        except: 
            pass

        try: 
            item['salary'] = re.findall(ur'年入<em>(.*?)</em>', html)[0] 
        except: 
            pass

        try:
            marital_status = {
            u'已婚':u'M',
            u'未婚':u'S',
            u'离异':u'D',
            u'离异单身':u'D',
            u'离异带孩':u'D',
            u'丧偶':u'W',
            u'丧偶单身':u'W',
            u'丧偶带孩':u'W'
            }
            r = re.findall(ur'color:#7AAE1F">(.*?)</strong>', html)
            if r: item['marital_status'] = marital_status[r[0].strip()]
        except:
            pass

        try: 
            education_level = {
            u'初中':u'1',
            u'中专/职高/技校':u'3',
            u'高中':u'1',
            u'大专以下':u'1',
            u'大专':u'2',
            u'本科':u'4',
            u'硕士':u'5',
            u'博士':u'6',
            u'博士后':u'6',
            }
            r = re.findall(ur'</strong>，<em>(.*?)学历</em>', html)
            if r: item['education_level'] = education_level[r[0].strip()]
        except: 
            pass

        return item
