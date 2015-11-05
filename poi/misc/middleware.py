
import re
import random

import requests
from scrapy import log

from agents import AGENTS


PROXY_POOL = []
PROXY_COUNT = 1000


def get_proxy():
    global PROXY_POOL, PROXY_COUNT
    PROXY_COUNT += 1
    if PROXY_COUNT >= 1000:
        PROXY_COUNT = 0
        # Refresh proxy pool.
        # http://cn-proxy.com/
        resp = requests.get('http://cn-proxy.com/')
        PROXY_POOL.extend([match[0] + ':' + match[1] for match in re.findall(r'(\d+\.\d+\.\d+\.\d+)</td>[\s\S]*?<td>(\d+)', resp.content)])
        # http://www.xici.net.co/
        resp = requests.get('http://www.xici.net.co/')
        PROXY_POOL.extend([match[0] + ':' + match[1] for match in re.findall(r'(\d+\.\d+\.\d+\.\d+)</td>[\s\S]*?<td>(\d+)', resp.content)[:40]])

    return random.choice(PROXY_POOL)


class CustomUserAgentMiddleware(object):
    def process_request(self, request, spider):
        agent = random.choice(AGENTS)
        request.headers['User-Agent'] = agent


class CustomHttpProxyMiddleware(object):
    def process_request(self, request, spider):
        """Use proxy with probability 0.3.
        """
        if random.random() < 0.3:
            request.meta['proxy'] = get_proxy()
