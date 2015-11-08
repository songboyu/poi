# -*- coding: utf-8 -*-

from scrapy import Spider, Request
from poi.items import PoiItem



class Lol99Spider(Spider):
    name = 'lol99'
    allow_domains = ['lol99.com']
    start_urls = [
        'http://www.lol99.com/'
    ]

    def parse(self, response):
        for i in xrange(2050000, 15899999):


            yield  Request('http://www.lol99.com/member/view.php?uid='+str(i),
                callback=self.parse_item,
                meta={'user_id': i})

    def parse_item(self, response):
        item = PoiItem()

        try:
            user_name = u''
            user_name = response.css('div.right_content h2::text').extract()[0]
            user_name = user_name.split('[')[0].rstrip()
            # print user_name
            item['name'] = user_name
            item['avatar'] = response.css('div.pic img::attr(src)').extract()[0]

            item['site_id'] = 18
            item['user_id'] = str(response.meta['user_id'])
            item['description'] = response.css('div.box_content p::text').extract()[0]
            r = response.xpath("//div[@class='right_content']/p/span/text()").extract()
            temp = u''
            for i in range(len(r)):
                temp = r[i]

                if u'男' in temp:
                    item['gender'] = 'M'
                elif u'女' in temp:
                    item['gender'] = 'F'
                elif u'学历' in temp:
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
                    education_list =[
                    u'初中',
                    u'中专/职高/技校',
                    u'高中',
                    u'大专',
                    u'本科',
                    u'硕士',
                    u'博士',
                    u'博士后',]
                    education = u''
                    education = temp[3:]

                    if education in education_list and education!=u'保密': item['education_level'] = education_level[education]
                elif u'所在地' in temp:
                    item['location'] = temp[4:]
                elif u'籍贯' in temp:
                    item['hometown'] = temp[3:]
                elif u'婚姻状况' in temp:
                    marital_status = {
                    u'已婚':u'M',
                    u'单身':u'S',
                    u'未婚':u'S',
                    u'离异':u'D',
                    u'丧偶':u'W'
                    }
                    item['marital_status'] = marital_status[temp[5:]]
                elif u'月薪' in temp:
                    item['salary'] = temp[3:]
                elif u'身高' in temp:
                    item['height'] = temp[3:]
                else:
                    pass
        except:
            return

        return item
