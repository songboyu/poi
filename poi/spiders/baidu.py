# -*- coding: utf-8 -*-
import json
import re
import hashlib

from scrapy.spiders import Spider
from scrapy.http import Request
from poi.items import PoiItem

class BaiduTiebaSpider(Spider):
    name = 'baidu'
    allow_domains = ['c.tieba.baidu.com']

    start_urls = [
        'http://tieba.baidu.com'
    ]

    def parse(self, response):
        for uid in xrange(2000000,100000000):
            a = 'has_plist=0&need_post_count=1&pn=1&rn=1&uid=' + str(uid)
            b = a.replace('&','') + 'tiebaclient!!!'
            sign = hashlib.md5(b).hexdigest()

            yield  Request('http://c.tieba.baidu.com/c/u/user/profile?' + a + '&sign='+sign, 
                callback=self.parse_item_json,
                priority=0)

    def parse_item_json(self,response):
        data = json.loads(response.body)
        item = PoiItem()
        
        item['site_id']     =   3
        item['user_id']     =   data['user']['id']                  #id
        item['name']        =   data['user']['name']                #姓名
        item['gender']      =   'M' if data['user']['sex']==1 else 'F'    #性别
        item['level']       =   data['user']['tb_age']              #吧龄
        item['followers']   =   int(data['user']['fans_num'])       #粉丝数
        item['following']   =   int(data['user']['concern_num'])    #关注数
        # item['my_like_num'] =   data['user']['my_like_num']       #喜欢的吧
        item['post_num']    =   int(data['user']['post_num'] if data['user']['post_num'] else '0')       #总发帖数
        item['reply_num']   =   int(data['user']['repost_num'] if data['user']['repost_num'] else '0')   #回复数
        # item['thread_num']  =   data['user']['thread_num']        #主题数
        item['description'] =   data['user']['intro']               #简介
        item['avatar']      =   'http://tb.himg.baidu.com/sys/portrait/item/'+data['user']['portrait']  #头像

        if item['name']:
            yield  Request('http://www.baidu.com/p/'+item['name']+'/detail', 
                callback=self.parse_item_detail,
                meta={'item': item},
                priority=10)

    def parse_item_detail(self,response):
        item = response.meta['item']
        root = response.xpath('//html')
        
        r = root.re(ur'生日<.*?"profile-cnt">(.*?)<')
        if r: 
            birthday = ''
            b = r[0].strip().replace(u' ','').replace(u'年','-').replace(u'月','-').replace(u'日','')
            if len(b) < 8:
                if re.search(r'\d{4}', b):
                    birthday = b + '01'
                else:
                    birthday = '0000-' + b
            else:
                birthday = b
            item['birthday'] = birthday

        bloodType = {
            u'O':u'1',
            u'A':u'2',
            u'B':u'3',
            u'AB':u'4',
            u'其他':u'5'
        }
        r = root.re(ur'血型<.*?"profile-cnt">(.*?)<')
        if r: item['blood_type'] = bloodType[r[0].strip()]

        r = root.re(ur'出生地<.*?"profile-cnt">(.*?)<')
        if r: item['hometown'] = r[0].strip()

        r = root.re(ur'居住地<.*?"profile-cnt">(.*?)<')
        if r: item['location'] = r[0].strip()

        r = root.re(ur'体型.*?<span>(.*?)<')
        if r: item['body_size'] = r[0].strip()

        marital_status = {
            u'单身':u'S',
            u'已婚':u'M',
            u'恋爱':u'L',
            u'离异':u'D'
        }
        r = root.re(ur'婚姻状态.*?<span>(.*?)<')
        if r: item['marital_status'] = marital_status[r[0].strip()]

        r = root.re(ur'性格.*?<span>(.*?)<')
        if r: item['personality'] = r[0].strip()

        item['favorites'] = ''
        r = root.re(ur'个人习惯.*?<span>(.*?)<')
        if r: item['favorites'] += r[0].strip()

        education_level = {
            u'初中':u'1',
            u'高中':u'1',
            u'大学':u'4',
            u'硕士':u'5',
            u'小学':u'7',
            u'中专/技校':u'2',
            u'大专':u'3',
            u'博士':u'6',
            u'其他':u'7',
        }
        r = root.re(ur'教育程度.*?<span>(.*?)<')
        if r: item['education_level'] = education_level[r[0].strip()]

        r = root.re(ur'当前职业.*?<span>(.*?)<')
        if r: item['occupation'] = r[0].strip()

        r = ' '.join(root.xpath('//dl[@class="userdetail-profile-habits"]//text()').extract())
        if r: item['favorites'] += re.sub(r'\s\s+', ' ', r).strip()

        r = ' '.join(root.xpath('//div[@class="biograph"]//text()').extract())
        if r: item['experience'] = re.sub(r'\s\s+', ' ', r).strip()

        r = root.re(ur'联系方式.*?<span>(.*?)<')
        if r: 
            if u'@' in r[0].strip():
                item['email'] = r[0].strip()
            else:
                item['cellphone'] = r[0].strip()

        item['experience'] = ''
        r = root.xpath('//dt[contains(./text(),"'+u'教育背景'+'")]')
        if r: item['experience'] += ' '.join(r.xpath('..//text()').extract())

        r = root.xpath('//dt[contains(./text(),"'+u'工作信息'+'")]')
        if r: item['experience'] += ' '.join(r.xpath('..//text()').extract())

        return item