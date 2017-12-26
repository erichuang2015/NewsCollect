# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from ..items import NewsItem
from .info import info
from .utils import *
from bs4 import BeautifulSoup as bs
import datetime
import time
from newsCollect.utils import get_conf_from_json
import sys

if sys.version_info.major == 2:
    reload(sys)
    sys.setdefaultencoding('utf8')

conf = get_conf_from_json('../conf.json')
if conf is None:
    conf = {
        "spider": {
            "load_spider": [],
            "crawl_page": 1
        }
    }


class EA(scrapy.Spider):
    name = 'EA'
    base_url = 'http://ea.hfut.edu.cn'
    url_template = info['EA']['url_template']
    tag_codes = info['EA']['tag_codes']
    count = 0

    def start_requests(self):
        for code in self.tag_codes:
            url = render_url(self.url_template, tag_code=code)
            yield Request(url, self.parse_index, meta={'type': self.tag_codes[code]})

    def parse_index(self, response):
        soup = bs(response.text, 'html.parser')
        table = soup.find('table', class_='category').tbody
        for tr in table.find_all('tr'):
            tds = tr.find_all('td')
            title = clean_string(tds[0].a.string)
            url = self.base_url + tds[0].a.attrs['href'] # 测试性爬取一页
            time_ = clean_string(tds[-1].string)
            yield Request(url, self.get_content, meta={'type': response.meta['type'],
                                                       'title': title,
                                                       'time': time_})

    def get_content(self, response):
        soup = bs(response.text, 'html.parser')
        content = soup.find('div', class_='content_all_art')

        meta = response.meta
        item = NewsItem()
        item['imgs'] = get_img_urls(content, self.base_url)
        item['content'] = content_process(content, self.base_url).encode('utf-8')
        item['title'] = meta['title']
        item['time'] = datetime.datetime.strptime(meta['time'], '%Y/%m/%d').date()
        item['url'] = response.url
        item['unit'] = info['EA']['unit']
        item['type'] = meta['type']
        item['timestamp'] = datetime.datetime.utcfromtimestamp(int(time.time()))
        return item
