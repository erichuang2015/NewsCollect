# coding: utf-8
from newsCollect.utils import get_conf_from_json
import time
from scrapy.cmdline import execute
from apscheduler.schedulers.blocking import BlockingScheduler

spider_conf = get_conf_from_json('newsCollect/conf.json')['spider']


def crawl(): 
    spiders = spider_conf.get('load_spider', [])
    for spider in spiders:
        execute(['scrapy', 'crawl', '%s' % spider])


if __name__ == '__main__':
    crawl()