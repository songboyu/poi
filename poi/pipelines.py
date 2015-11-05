# -*- coding: utf-8 -*-

import json
import codecs

import yaml
import MySQLdb
from scrapy import log


class MySQLPipeline(object):
    def __init__(self):
        CONFIG = yaml.load(open('config.yaml'))
        self.con = MySQLdb.connect(CONFIG['db']['host'],
                                   CONFIG['db']['user'],
                                   CONFIG['db']['password'],
                                   CONFIG['db']['database'],
                                   charset='utf8')
        self.cur = self.con.cursor()

    def process_item(self, item, spider):
        if 'user_id' not in item: return
        info = '%s on site %d' % (item['user_id'], item['site_id'])
        sql = 'INSERT INTO poi (%s) VALUES (%s)' % (', '.join(item.keys()), 
                                                    ', '.join(['%(' + key + ')s' for key in item.keys()]))
        try:
            self.cur.execute(sql, dict(item))
            self.con.commit()
            log.msg('Save ' + info, level=log.INFO)
        except Exception as e:
            msg = ' '.join(['Error', info, str(e)])
            log.msg(msg, level=log.ERROR)


class JSONPipeline(object):
    def __init__(self):
        self.file = codecs.open('items.json', 'wb', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line.decode('unicode_escape'))

        info = '%s on site %d' % (item['user_id'], item['site_id'])
        log.msg('Save ' + info, level=log.INFO)
        return item
