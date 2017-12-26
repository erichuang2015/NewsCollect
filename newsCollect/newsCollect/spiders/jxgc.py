# -*- coding: utf-8 -*-
# 机械工程学院爬虫

import scrapy
from scrapy.http import Request
from ..items import NewsItem
from .info import info
from .utils import *
from bs4 import BeautifulSoup as bs
import datetime
import time
import re
import sys

if sys.version_info.major == 2:
    reload(sys)
    sys.setdefaultencoding('utf8')


class JXGC(scrapy.Spider):
    name = 'jxgc'
    base_url = 'http://jxxy.hfut.edu.cn'
    url_template = info['jxgc']['url_template']
    tag_codes = info['jxgc']['tag_codes']
    count = 0

    def start_requests(self):
        for tag in self.tag_codes:
            if type(self.tag_codes[tag]) is not dict:
                url = render_url(self.url_template, primary_title=tag)
                yield Request(url, self.parse_index, meta={'tag_code': self.tag_codes[tag]})
            else:
                for sub_tag in self.tag_codes[tag]:
                    url = render_url(self.url_template, primary_title=tag) + '/' + sub_tag
                    yield Request(url, self.parse_index, meta={'tag_code': self.tag_codes[tag][sub_tag]})

    def parse_index(self, response):
        soup = bs(response.text, 'html.parser')
        h_tags = soup.find_all('h3', class_='catItemTitle')
        for h in h_tags:
            # print h.a.string
            url = self.base_url + h.a.attrs['href']
            title = h.a.string.split(']')[-1].replace('\t', '').replace(' ', '')
            time = h.a.string.split(']')[0].split('[')[-1]
            # print (title, time, url)
            yield Request(url, self.get_content, meta={'tag_code': response.meta['tag_code'],
                                                       'title': title,
                                                       'time': time})

    def get_content(self, response):
        self.count += 1
        # print('crawl No.%s: %s' % (self.count, response.meta['title']))
        soup = bs(response.text, 'html.parser')
        content = soup.find('div', id='k2Container')

        meta = response.meta
        item = NewsItem()
        item['imgs'] = get_img_urls(content, self.base_url)
        item['content'] = content_process(content, self.base_url).encode('utf-8')
        item['title'] = meta['title']
        item['time'] = datetime.datetime.strptime(meta['time'], '%Y-%m-%d').date()
        item['url'] = response.url
        item['unit'] = info['jxgc']['unit']
        item['timestamp'] = datetime.datetime.utcfromtimestamp(int(time.time()))
        item['type'] = meta['tag_code']
        return item
