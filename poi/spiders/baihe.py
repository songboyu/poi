# -*- coding: utf-8 -*-
import re
import datetime
from scrapy import Spider, Request
from poi.items import PoiItem

class BaiheSpider(Spider):
    name = 'baihe'
    allow_domains = ['profile.baihe.com']

    def start_requests(self):
        for i in xrange(90000000, 185000000):
            yield  Request('http://profile.baihe.com/new/BasicInfo.action?oppId='+str(i),
                headers={
                    'Cookie':'61ACA814921737385EA2CAFACD96262F=120623081; tmib_res_layout=1024%20x%20768; tempID=1154204010; sjbhCookie=sjbh; noticeEvent_120780133=10; accessToken=BH1431249650477328708; accessID=20150510172121980849; AuthCookie=4BFFD62B611D896EC1B9A52516C3ABAD20213A39FCC0F405B7E9DA9237C4A7C92CFF25929C2F172A904AF051C2A81FF4D7A6E2425F8EA85867F26BDD2B80CF714225AA2638EF6BAB6BFB0F813A653583; GCUserID=120780133; OnceLoginWEB=120780133; LoginEmail=18646492184%40mobile.baihe.com; userID=120780133; spmUserID=120780133; 120780133_log=1; hvaeHn_120780133=0; ck_msgInfo_bzt_firstloopTime_120780133=1431249697504; Hm_lvt_5caa30e0c191a1c525d4a6487bf45a9d=null,1431249650; Hm_lpvt_5caa30e0c191a1c525d4a6487bf45a9d=1431249712; __asc=null; __auc=null; nTalk_CACHE_DATA={uid:kf_9847_ISME9754_120780133,tid:1431249650508134}; NTKF_T2D_CLIENTID=guestAA1A49C7-96D2-4199-8263-3D01F4750A72; JSESSIONID=B52790E88E7EC6697E77CE06B84BC55E; _fmdata=1B6B911EAB1E48D50913EA061FEBA24BFA51BA78519F7F5CAA35D01CA6BFE20A49D4B1D4C0565B7434051B4FF13E590FCB23022D65631CCD; ck_msgInfo_bzt_lastloopTime_120780133=1431249884182; ck_msgInfo_bzt_loopTime_120780133=10000; ck_msgInfo_bzt_120780133=noReadSys%3A%231%257CcityChn%3A%23%25E5%258C%2597%25E4%25BA%25AC%25E5%25B4%2587%25E6%2596%2587%257CgroupID%3A%230%257CtodayNoRead%3A%23undefined%257CmainPhoto%3A%23http%3A//images.baihe.com/images/baihe_new/images/default_pictures/120_150/nopic_male.gif%257CnoReadAllMsg%3A%230%257CcityCode%3A%23861103%257CuserName%3A%23kulala1982%257Cgender%3A%231%257CnoReadCommMsg%3A%230%257CnoReadAllMsg_u%3A%230%257Cage%3A%2324; gid_m4h=1; ck_webim_info_120780133=1431249889767; ck_webim_num_120780133=0',
                    'Pragma':'no-cache',
                    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.94 Safari/537.36'
                },
                callback=self.parse_item,
                meta={'user_id': i})

    def parse_item(self, response):
        item = PoiItem()
        root = response.xpath('//html')
        try:
            item['name'] = response.css('strong#userNameStrong::text').extract()[0]

            # If name is available, then this item is valid.
            item['site_id'] = 12 # Site id of tianya.
            item['user_id'] = str(response.meta['user_id'])
        except:
            return

        r = root.re(ur'"defaultUrl":"(.*?)"')
        if r: 
            item['avatar'] = r[0]
        else:
            item['avatar'] = 'http://profile.baihe.com/new/' + response.css('div#simplePhotoDiv img::attr(src)').extract()[0]

        gender = root.re(ur'var gender_topSendMsg_name_TA = \'(.*?)\';')[0]
        item['gender'] = 'M' if u'他' in gender else 'F'

        birthday = root.re(ur'var oppAge = (\d+);')[0]
        item['birthday'] = str(datetime.date.today().year - int(birthday)) + '-00-00'
        item['height'] = root.re(ur'<strong>身高：</strong><p>(.*?)</p>')[0]

        marital_status = {
            u'已婚':u'M',
            u'未婚':u'S',
            u'离异':u'D',
            u'丧偶':u'W'
        }
        r = root.re(ur'<strong>婚姻状况：</strong><p>(.*?)</p>')
        if r: item['marital_status'] = marital_status[r[0].strip()]

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
        r = root.re(ur'<strong>学历：</strong><p>(.*?)</p>')
        if r and r[0].strip()!=u'以后告诉你': item['education_level'] = education_level[r[0].strip()]

        r = root.re(ur'<strong>职业：</strong><p>(.*?)</p>')
        if r and r[0].strip()!=u'以后告诉你': item['occupation'] = r[0].strip()

        r = root.re(ur'<strong>月薪：</strong><p>(.*?)</p>')
        if r and r[0].strip()!=u'以后告诉你': item['salary'] = r[0].strip()

        r = root.re(ur'<strong>来自：</strong><p>(.*?)</p>')
        if r and r[0].strip()!=u'以后告诉你': item['location'] = r[0].strip()

        r = response.css('td#_item_want_know_1::text').extract()
        if r and r[0].strip()!=u'以后告诉你': item['hometown'] = r[0].strip()

        item['experience'] = ''
        r = response.css('td#_item_want_know_2::text').extract()
        if r and r[0].strip()!=u'以后告诉你': item['experience'] += u'毕业学校：'+r[0].strip()

        r = response.css('td#_item_want_know_10::text').extract()
        if r and r[0].strip()!=u'以后告诉你': item['experience'] += u'  公司行业：'+r[0].strip()

        r = response.css('td#_item_want_know_3::text').extract()
        if r and r[0].strip()!=u'以后告诉你': item['body_size'] = r[0].strip()

        r = response.css('td#_item_want_know_5::text').extract()
        if r and r[0].strip()!=u'以后告诉你': item['weight'] = r[0].strip()

        r = response.css('td#_item_want_know_9::text').extract()
        if r and r[0].strip()!=u'以后告诉你': item['looks'] = r[0].strip()

        bloodType = {
            u'O型':u'1',
            u'A型':u'2',
            u'B型':u'3',
            u'AB型':u'4',
            u'其他型':u'5'
        }
        r = response.css('td#_item_want_know_7::text').extract()
        if r and r[0].strip()!=u'以后告诉你': item['blood_type'] = bloodType[r[0].strip()]

        item['description'] = response.css('div.pro_details pre::text').extract()[0]

        return item
