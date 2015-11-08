# -*- coding: utf-8 -*-

from scrapy import Spider, Request
from poi.items import PoiItem



class HzxqSpider(Spider):
    name = 'hzxq'
    allow_domains = ['hzxq.net']
    start_urls = [
        'http://www.hzxq.net/'
    ]

    def parse(self, response):
        for i in xrange(2, 50000):


            yield  Request('http://www.hzxq.net/user/'+str(i),
                callback=self.parse_item,
                meta={'user_id': i})

    def parse_item(self, response):
        item = PoiItem()

        try:
            item['name'] = response.xpath("//a[@class='sexico1']/text()").extract()[0]
            item['avatar'] = response.xpath("//div[@class='U110MP']/img/@src").extract()[0]
            item['site_id'] = 28
            item['user_id'] = str(response.meta['user_id'])
            info_A = response.xpath("//div[@class='UmainL3content1']/dt/text()").extract()
            info_B = response.xpath("//div[@class='UmainL3content1']/dd/text()").extract()
            bloodType = {
            u'O型':u'1',
            u'A型':u'2',
            u'B型':u'3',
            u'AB型':u'4',
            u'其他型':u'5'
            }
            bloodTypeA = [
            u'O型',
            u'A型',
            u'B型',
            u'AB型',
            u'其他型',
            ]
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
            education_levelA = [
                    u'初中',
                    u'中专/职高/技校',
                    u'高中',
                    u'大专',
                    u'本科',
                    u'硕士',
                    u'博士',
                    u'博士后',
                    ]
            marital_status = {
            u'已婚':u'M',
            u'恋爱中':u'S',
            u'未婚':u'S',
            u'离异':u'D',
            u'丧偶':u'W'
            }
            marital_statusA = [
            u'已婚',
            u'恋爱中',
            u'未婚',
            u'离异',
            u'丧偶',
            ]
            for i in range(len(info_A)):
                if u'血' in info_A[i]:
                    if info_B[i]!=u'保密'and info_B[i]!=u'未填'and info_B[i] in bloodTypeA: item['blood_type'] = bloodType[info_B[i]]
                elif u'学' in info_A[i]:
                    if info_B[i]!=u'保密'and info_B[i]!=u'未填'and info_B[i] in education_levelA: item['education_level'] = education_level[info_B[i]]
                elif u'月' in info_A[i]:
                    if info_B[i]!=u'保密'and info_B[i]!=u'未填': item['salary'] = info_B[i]
                elif u'身' in info_A[i]:
                    if info_B[i]!=u'保密'and info_B[i]!=u'未填': item['height'] = info_B[i]
                else:
                    pass
            info_A = response.xpath("//div[@class='UmainL3content2']/dt/text()").extract()
            info_B = response.xpath("//div[@class='UmainL3content2']/dd/text()").extract()
            for i in range(len(info_A)):

                if u'婚姻状况' in info_A[i]:
                    if info_B[i]!=u'保密'and info_B[i]!=u'未填'and info_B[i] in marital_statusA: item['marital_status'] = marital_status[info_B[i]]
                elif u'体' in info_A[i]:
                    if info_B[i]!=u'保密'and info_B[i]!=u'未填': item['weight'] = info_B[i]
                elif u'职' in info_A[i]:
                    if info_B[i]!=u'保密'and info_B[i]!=u'未填': item['occupation'] = info_B[i]
                elif u'年' in info_A[i]:
                    if info_B[i]!=u'保密'and info_B[i]!=u'未填': item['birthday'] = info_B[i][-11:-1]
                else:
                    pass
        except:
            return

        return item
