# -*- coding: utf-8 -*-

from scrapy import Spider, Request
from poi.items import PoiItem




class CunyouSpider(Spider):
    name = 'cunyou'
    allow_domains = ['cunyouwang.com']
    start_urls = [
        'http://www.cunyouwang.com/'
    ]

    def parse(self, response):
        for i in xrange(5000, 1000000):


            yield  Request('http://www.cunyouwang.com/jiaoyou-'+str(i),
                callback=self.parse_item,
                meta={'user_id': i})

    def parse_item(self, response):
        item = PoiItem()

        try:
            item['name'] = response.xpath("//p[@class='name']/strong/text()").extract()[0]
            item['avatar'] = response.xpath("//div[@class='photo']/img/@src").extract()[0]

            item['site_id'] = 24
            item['user_id'] = str(response.meta['user_id'])
            r = response.xpath("//div[@style='background:none;']/dl/dd/text()").extract()
            for i in range(len(r)):
                if u'男' in r[i]:
                    item['gender'] = 'M'
                elif u'女' in r[i]:
                    item['gender'] = 'F'
                elif u'身高' in r[i]:
                    item['height'] =r[i][4:]
                elif u'体重' in r[i]:
                    item['weight'] = r[i][4:]
                elif u'情感状态' in r[i]:
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
                    if r[i][6:] in marital_statusA:item['marital_status'] = marital_status[r[i]]
            r = response.xpath("//div[@class='pro_details']/dl/dd/text()").extract()
            for i in range(len(r)):
                if u'兴趣爱好' in r[i]:
                    item['favorites'] = r[i][6:]
                elif u'血型' in r[i]:
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
                    if r[i][4:] in bloodTypeA :item['blood_type'] = bloodType[r[i][4:]]
                elif u'工作地区' in r[i]:

                    item['location'] = r[i][5:]
                elif u'学历' in r[i]:
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
                    if r[i][3:] in education_levelA:item['education_level'] = education_level[r[i][3:]]
                elif u'职业' in r[i]:
                    item['occupation'] = r[i][3:]
                elif u'年收入' in r[i]:
                    item['salary'] = r[i][4:]
                else:
                    pass
            r = response.xpath("//div[@class='pro_details']/p/text()").extract()
            temp = u''
            for i in xrange(1,len(r)):
                temp+=r[i]

            item['description'] = temp



        except:
            return

        return item
