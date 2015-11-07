# -*- coding: utf-8 -*-

BOT_NAME = 'poi'

SPIDER_MODULES = ['poi.spiders']
NEWSPIDER_MODULE = 'poi.spiders'

# SCHEDULER = 'scrapy_redis.scheduler.Scheduler'

# SCHEDULER_PERSIST = True

# SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.SpiderPriorityQueue'

# SCHEDULER_IDLE_BEFORE_CLOSE = 10

ITEM_PIPELINES = {
    'poi.pipelines.MySQLPipeline': 500,
    # 'poi.pipelines.JSONPipeline': 500,
}

EXTENSIONS = {
   'scrapy.contrib.feedexport.FeedExporter': None
}

# REDIS_HOST = '192.168.8.55'
# REDIS_PORT = 6379

LOG_LEVEL = 'INFO'

# REDIRECT_ENABLED = False

COOKIES_ENABLED = False

USER_AGENT = 'Baiduspider+(+http://www.baidu.com/search/spider.htm)'

CONCURRENT_REQUESTS = 100

# LOG_FILE = 'log'

# DUPEFILTER_CLASS = 'scrapy.dupefilter.BaseDupeFilter'

DEPTH_PRIORITY = 1 
# SCHEDULER_DISK_QUEUE = 'scrapy.squeue.PickleFifoDiskQueue'
# SCHEDULER_MEMORY_QUEUE = 'scrapy.squeue.FifoMemoryQueue'