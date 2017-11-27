# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sys

import sqlalchemy

from db import News, get_session

reload(sys)
sys.setdefaultencoding('utf8')

'''
TODO: 2017/10/30
    - 使用redis增量去重
'''


class NewsItemPipeline(object):
    def open_spider(self, spider):
        self.session = get_session()

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
