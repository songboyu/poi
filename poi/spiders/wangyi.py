# -*- coding: utf-8 -*-

import re
import urllib

import scrapy
from scrapy import Spider, Request
from poi.items import PoiItem

from poi.utils import *

class WangyiSpider(Spider):
    name = 'wangyi'
    allowed_domains = ['blog.163.com']
    start_urls = [
        'http://blog.163.com/',
    ]

    def dwr_headers(self):
        return {
            'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
            'Content-Type': 'text/plain',
            'Origin': 'http://api.blog.163.com',
            'Referer': 'http://api.blog.163.com/crossdomain.html?t=20100205',
        }

    def profile_request(self, user):
        return Request(
            'http://' + user + '.blog.163.com/profile',
            callback=self.parse_profile,
            priority=10,
        )

    def friends_request(self, user):
        return Request(
            'http://api.blog.163.com/' + user + '/dwr/call/plaincall/UserBeanNew.getFriends.dwr',
            callback=self.parse_friends,
            method='POST',
            headers=self.dwr_headers(),
            body=('callCount=1\n'
                  'scriptSessionId=${scriptSessionId}187\n'
                  'c0-scriptName=UserBeanNew\n'
                  'c0-methodName=getFriends\n'
                  'c0-id=0\n'
                  'c0-param0=boolean:false\n'
                  'c0-param1=number:0\n'
                  'c0-param2=number:0\n'
                  'c0-param3=number:1000\n'
                  'batchId=516151\n'),
            priority=0,
        )

    def level_request(self, userid, item):
        return Request(
            'http://api.blog.163.com/bgs/dwr/call/plaincall/BgsBean.getBgsUserByUserId.dwr',
            callback=self.parse_level,
            meta={'item': item},
            method='POST',
            headers=self.dwr_headers(),
            body=('callCount=1\n'
                  'scriptSessionId=${scriptSessionId}187\n'
                  'c0-scriptName=BgsBean\n'
                  'c0-methodName=getBgsUserByUserId\n'
                  'c0-id=0\n'
                  'c0-param0=number:' + userid + '\n'
                  'c0-param1=boolean:false\n'
                  'batchId=516151\n'),
            priority=20,
        )

    def blog_request(self, item):
        return Request(
            'http://' + item['user_id'] + '.blog.163.com/blog',
            callback=self.parse_blog,
            meta={'item': item},
            priority=30,
        )

    def parse(self, response):
        """Parse the homepage of wangyi blog.

        @url http://blog.163.com
        """

        users = set(response.xpath('//html').re('(\w+)\.blog\.163\.com/blog/static/\d+'))
        for user in users:
            yield self.profile_request(user)
            yield self.friends_request(user)

    def parse_profile(self, response):
        """Parse a user's profile page.

        @url http://lvxiaobin99.blog.163.com/profile
        """

        item = PoiItem()
        root = response.xpath('//html')
        username = response.url.split('/')[2].split('.')[0]
        self.log('Profile=> ' + username, level=scrapy.log.DEBUG)

        # ID attributes.
        item['site_id'] = 2

        item['user_id'] = username

        # Personal attributes.
        r = root.re(r"nickName:'(.*?)'")
        if r: item['name'] = r[0]

        item['avatar'] = 'http://os.blog.163.com/common/ava.s?host=' + username + '&b=1'

        r = root.re(ur'介绍：</td>[\s\S]*?>([\s\S]*?)<')
        if r: item['description'] = r[0].strip()

        r = root.re(r'marital=(\w)')
        if r: item['marital_status'] = r[0]

        r = root.re(r'education=(\d)')
        if r: item['education_level'] = r[0]

        r1 = root.re(r'industry=.*?>(.*?)<')
        r2 = root.re(r'occupation=.*?>(.*?)<')
        if r1 or r2: item['occupation'] = r1[0] + ' ' + r2[0]

        r = root.re(r'salary=.*?>(.*?)<')
        if r: item['salary'] = r[0]

        r = root.re(r'skills=([%\w]+)')
        if r: item['speciality'] = urllib.unquote(r[0].encode('utf8'))

        r = root.re(r'characteristics=[^"]+')
        if r: item['personality'] = urllib.unquote(' '.join(re.findall('%[%\w]+', ' '.join(r))).encode('utf8'))

        r = root.re(r'favorite\w+=[^"]+')
        if r: item['favorites'] = urllib.unquote(' '.join(re.findall('%[%\w]+', ' '.join(r))).encode('utf8'))

        r = ' '.join(root.xpath('//div[@class="biograph"]//text()').extract())
        if r: item['experience'] = re.sub(r'\s\s+', ' ', r).strip()

        # Body attributes.
        r = root.re(r'gender=(\w)')
        if r: item['gender'] = r[0]

        r = root.re(r'weight=.*?>(.*?)<')
        if r: item['weight'] = r[0]

        r = root.re(r'height=.*?>(.*?)<')
        if r: item['height'] = r[0]

        r = root.re(r'bodyShape=.*?>(.*?)<')
        if r: item['body_size'] = r[0]

        r = root.re(r'appearance=.*?>(.*?)<')
        if r: item['looks'] = r[0]

        r = root.re(r'bloodType=(\d)')
        if r: item['blood_type'] = r[0]

        # Contact attributes.
        r = root.re(ur'E-Mail　:</td>[\s\S]*?>([\s\S]*?)<')
        if r: item['email'] = r[0].strip()

        r = root.re(ur'QQ:</td>[\s\S]*?>([\s\S]*?)<')
        if r: item['qq'] = r[0].strip()

        r = root.re(ur'移动电话:</td>[\s\S]*?>([\s\S]*?)<')
        if r: item['cellphone'] = r[0].strip()

        r = root.re(ur'固定电话:</td>[\s\S]*?>([\s\S]*?)<')
        if r: item['telephone'] = r[0].strip()

        # Time attributes.
        item['reg_time'] = timestamp2datetime(root.re(r'creatTime:(\d+)')[0])

        item['last_update_time'] = timestamp2datetime(root.re(r'updateTime:(\d+)')[0])

        item['last_login_time'] = timestamp2datetime(root.re(r'lastLoginTime:(\d+)')[0])

        r = root.re(r'birthDate=([^"]+)')
        if r: item['birthday'] = r[0]

        # Location attributes.
        r = root.re(r'type=1[^"]+')
        if r: item['location'] = urllib.unquote(' '.join(re.findall('%[%\w]+', r[-1])).encode('utf8'))

        r = root.re(r'type=4[^"]+')
        if r: item['hometown'] = urllib.unquote(' '.join(re.findall('%[%\w]+', r[-1])).encode('utf8'))

        userid = root.re(r'userId:(\d+)')[0]
        yield self.level_request(userid, item)

    def parse_friends(self, response):
        """Parse a user's friends list.
        """
        r = re.findall('userName="(.*?)"', response.body)
        if not r: return

        self.log('friends=> %d' % len(r), level=scrapy.log.DEBUG)
        for user in r:
            yield self.profile_request(user)
            yield self.friends_request(user)

    def parse_level(self, response):
        """Parse score and level.
        """
        item = response.meta['item']
        self.log('level=> ' + item['user_id'], level=scrapy.log.DEBUG)

        r = re.findall('totalScore:"(\d+)"', response.body)
        if r: item['score'] = int(r[0])

        r = re.findall('grade:"(\d+)"', response.body)
        if r: item['level'] = r[0]

        yield self.blog_request(item)

    def parse_blog(self, response):
        """Parse a user's blog page.
        """
        item = response.meta['item']
        self.log('Blog=> ' + item['user_id'], level=scrapy.log.DEBUG)

        item['post_num'] = max([int(x) for x in re.findall(r'count:(\d+)', response.body)])
        return item
