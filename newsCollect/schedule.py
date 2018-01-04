# coding: utf-8
from newsCollect.utils import get_conf_from_json
import time
from scrapy.cmdline import execute
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import threading


spider_conf = get_conf_from_json('newsCollect/conf.json')['spider']


def crawl():
    settings = get_project_settings()
    spiders = spider_conf.get('load_spider', [])
    process = CrawlerProcess(settings=settings)
    for spider in spiders:
        process.crawl(spider)
    process.start()


if __name__ == '__main__':
    crawl()
 
