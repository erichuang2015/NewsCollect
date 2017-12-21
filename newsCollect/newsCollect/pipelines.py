# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sys
import sqlalchemy
from .db import News, get_session
from .utils import get_conf_from_json
import redis
from .spiders.info import info

# reload(sys)
# sys.setdefaultencoding('utf8')

'''
TODO: 2017/10/30
    - 使用redis增量去重
'''

conf = get_conf_from_json('conf.json')
if conf is None:
    conf = {
        "redis": {
            "host": "127.0.0.1",
            "port": 6379,
            "pw": "",
        }
    }



class DuplicatePipeline(object):
    def open_spider(self, spider):
        redis_conf = conf['redis']
        self.redis_db = redis.Redis(host=redis_conf['host'], port=redis_conf['port'], db=4)
        self.db_session = get_session('dev.db')
    def process_item(self, item, spider):
        # 字段存在校验
        if self.redis_db.hlen(item['unit']) == 0:
            self.redis_db.hset(item['unit'], item['url'], '')
            return item
        ex = self.redis_db.hget(item['unit'], item['url'])
        if ex is None:
            self.redis_db.hset(item['unit'], item['url'], '')
            return item
        print('item Duplicate: url[%s]' % item['url'])
        

class NewsItemPipeline(object):
    def open_spider(self, spider):
        self.session = get_session('dev.db')

    def process_item(self, item, spider):
        new_news = News(
            title=unicode(item['title']),
            unit=unicode(item['unit']),
            type=unicode(item['type']),
            time=item['time'],
            url=unicode(item['url']),
            imgs=unicode(item['imgs']),
            content=unicode(item['content']),
            timestamp=item['timestamp']
        )
        self.session.add(new_news)
        try:
            self.session.commit()
        except sqlalchemy.exc.InvalidRequestError:
            self.session.rollback()
        return item

    def close_spider(self, spider):
        self.session.close()
