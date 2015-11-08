# -*- coding: utf-8 -*-
import datetime
import time

import requests
from bs4 import BeautifulSoup
from scrapy import Spider, Request, FormRequest
from poi.items import PoiItem

import utils

class RenrenSpider(Spider):
    name = 'renren'
    allow_domains = ['http://www.renren.com/']

    uid = 275000000

    cookies = 'anonymid=i8pg5nhd-shfdcd; _r01_=1; JSESSIONID=abc6gyMzwvHPk4Az8nN0u; wp=0; jebe_key=35c0ba4a-c1fa-454c-bf08-3cd0517227a4%7Ce65290594db334b483ac1f24d6999fef%7C1430884448428%7C1%7C1430885122107; _urm_378384894=9999; depovince=BJ; jebecookies=e1c7f34b-675d-48d9-873c-a6327590c04e|||||; ick_login=f242e96a-c484-4f68-b46e-eeeca52a314c; _de=E6CA621BCBC30E9A85E798EF221DF2AF; p=920950803139a28ca9a4c028f1c2846e4; first_login_flag=1; ln_uact=18345174475; ln_hurl=http://hdn.xnimg.cn/photos/hdn421/20140206/2325/h_main_TZb3_97690001dbe1111a.jpg; t=2582a0a96c3887f092040edd842ea33b4; societyguester=2582a0a96c3887f092040edd842ea33b4; id=378384894; xnsid=d7c2bea1; __utma=10481322.1851133621.1430901819.1430901819.1430901819.1; __utmc=10481322; __utmz=10481322.1430901819.1.1.utmcsr=share.renren.com|utmccn=(referral)|utmcmd=referral|utmcct=/share/v7/161125632; alxn=a5d9878e44be799cc3e99efcab2d3dcd; mt=Jvfhn7u-wG7PdteezqsqEK; cp_config=2; l4pager=0; jebe_key=35c0ba4a-c1fa-454c-bf08-3cd0517227a4%7Ce65290594db334b483ac1f24d6999fef%7C1430908978129%7C1; ver=7.0; loginfrom=null; wp_fold=0',
    
    def start_requests(self):
        yield  Request('http://www.renren.com/'+str(self.uid)+'/profile?v=info_timeline',
            headers={
                'Cookie':self.cookies,
                'Pragma':'no-cache',
                'Referer':'http://www.renren.com/343633795/profile',
                'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.94 Safari/537.36'
            },
            callback =self.parse_item,
            meta={'user_id': self.uid})
    
    def validateuser(self, uid):
        s = requests.session()
        cookies = {
            'anonymid':'i8pg5nhd-shfdcd',
            '_r01_':'1',
            'JSESSIONID':'abc6gyMzwvHPk4Az8nN0u',
            'wp':'0',
            'jebe_key':'35c0ba4a-c1fa-454c-bf08-3cd0517227a4%7Ce65290594db334b483ac1f24d6999fef%7C1430884448428%7C1%7C1430885122107',
            '_urm_378384894':'9999',
            'depovince':'BJ',
            'jebecookies':'e1c7f34b-675d-48d9-873c-a6327590c04e|||||',
            'ick_login':'f242e96a-c484-4f68-b46e-eeeca52a314c',
            '_de':'E6CA621BCBC30E9A85E798EF221DF2AF',
            'p':'920950803139a28ca9a4c028f1c2846e4',
            'first_login_flag':'1',
            'ln_uact':'18345174475',
            'ln_hurl':'http://hdn.xnimg.cn/photos/hdn421/20140206/2325/h_main_TZb3_97690001dbe1111a.jpg',
            't':'2582a0a96c3887f092040edd842ea33b4',
            'societyguester':'2582a0a96c3887f092040edd842ea33b4',
            'id':'378384894',
            'xnsid':'d7c2bea1',
            '__utma':'10481322.1851133621.1430901819.1430901819.1430901819.1',
            '__utmc':'10481322',
            '__utmz':'10481322.1430901819.1.1.utmcsr=share.renren.com|utmccn=(referral)|utmcmd=referral|utmcct=/share/v7/161125632',
            'alxn':'a5d9878e44be799cc3e99efcab2d3dcd',
            'mt':'Jvfhn7u-wG7PdteezqsqEK',
            'cp_config':'2',
            'ver':'7.0',
            'loginfrom':'null',
            'jebe_key':'35c0ba4a-c1fa-454c-bf08-3cd0517227a4%7Ce65290594db334b483ac1f24d6999fef%7C1430910523708%7C1',
            'wp_fold':'0',
            'l4pager':'0'
        }
        r = s.get('http://www.renren.com/validateuser.do?id='+str(uid),
            cookies = cookies,
            headers={
                    'Pragma':'no-cache',
                    'Referer':'http://www.renren.com/343633795/profile',
                    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.94 Safari/537.36'
                })

        soup = BeautifulSoup(r.content)
        form = soup.find('form', attrs={'name': 'valiateUserForm'})
        payload = utils.get_datadic(form)

        r = s.get('http://icode.renren.com/getcode.do?t=ninki&rnd='+str(int(time.time()*1000)),
                cookies = cookies,
                headers={
                    'Accept':'image/webp,*/*;q=0.8',
                    'Referer':'http://www.renren.com/validateuser.do'
                })
        seccode = utils.crack_captcha(r.content)
        payload['icode'] = seccode
        payload['requestToken'] = '-295732589'
        payload['_rtk'] = 'ba2078ed'
        print payload
        r = s.post('http://www.renren.com/validateuser.do', data=payload,
            cookies = cookies,
            headers={
                    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Host':'www.renren.com',
                    'Origin':'http://www.renren.com',
                    'Pragma':'no-cache',
                    'Referer':'http://www.renren.com/validateuser.do?id='+str(uid),
                    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.94 Safari/537.36'
                })
        print r.url

    def parse_item(self, response):
        self.uid += 1
        if '继续浏览' in response.body:
            self.validateuser(self.uid)

        item = PoiItem()

        try:
            item['name'] = response.css('h1.avatar_title::text').extract()[0]
            item['avatar'] = response.css('img#userpic::attr(src)').extract()[0]

            item['site_id'] = 7 # Site id 
            item['user_id'] = str(response.meta['user_id'])
        except:
            yield  Request('http://www.renren.com/'+str(self.uid)+'/profile?v=info_timeline',
                    headers={
                        'Cookie':self.cookies,
                        'Pragma':'no-cache',
                        'Referer':'http://www.renren.com/343633795/profile',
                        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.94 Safari/537.36'
                    },
                    callback =self.parse_item,
                    meta={'user_id': self.uid})
            return

        item['experience'] = ''

        r = response.css('li.work span::text').extract()
        if r: item['experience'] += r[0]

        r = response.css('li.school span::text').extract()
        if r: item['experience'] += r[0]

        r = response.css('li.birthday span::text').extract()
        if r: 
            item['gender'] = 'M' if u'男' in r[0] else 'F'

        r = response.css('li.hometown::text').extract()
        if r: item['hometown'] = r[0]

        r = response.css('li.address::text').extract()
        if r: item['location'] = r[0]

        yield item
        yield  Request('http://www.renren.com/'+str(self.uid)+'/profile?v=info_timeline',
                    headers={
                        'Cookie':self.cookies,
                        'Pragma':'no-cache',
                        'Referer':'http://www.renren.com/343633795/profile',
                        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.94 Safari/537.36'
                    },
                    callback =self.parse_item,
                    meta={'user_id': self.uid})