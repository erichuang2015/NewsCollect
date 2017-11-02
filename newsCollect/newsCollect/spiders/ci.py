# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from ..items import NewsItem
from .info import info
from .utils import *
from bs4 import BeautifulSoup as bs
import datetime
import time


class jsj(scrapy.Spider):
    name = 'jsj'
    base_url = 'http://ci.hfut.edu.cn/'
    url_template = info['jsj']['url_template']
    tag_codes = info['jsj']['tag_codes']
    count = 0

    def start_requests(self):
        for code in self.tag_codes:
            url = render_url(self.url_template, tag_code=code)
            yield Request(url, self.parse_index, meta={'type': self.tag_codes[code]})

    def parse_index(self, response):
        soup = bs(response.text, 'html.parser')
        li_list = soup.find('div', class_='column').find_all('li')
        for li in li_list:
            title = li.a.string
            url = li.a.attrs['href']
            yield Request(url, self.get_content, meta={'type': response.meta['type'],
                                                       'title': title})

    def get_content(self, response):
        time_ = response.xpath('//*[@id="main"]/div[3]/div[1]/text()').extract()[0]
        soup = bs(response.text, 'html.parser')
        content = soup.find('div', class_='article')

        meta = response.meta
        item = NewsItem()
        item['imgs'] = get_img_urls(content, self.base_url)
        item['content'] = content_process(content, self.base_url).encode('utf-8')
        item['title'] = meta['title']
        item['time'] = datetime.datetime.strptime(time_, '%Y-%m-%d').date()
        item['url'] = response.url
        item['unit'] = info['jsj']['unit']
        item['type'] = meta['type']
        item['timestamp'] = datetime.datetime.utcfromtimestamp(int(time.time()))
        return item
