# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from ..items import NewsItem
from .info import info
from .utils import *
from bs4 import BeautifulSoup as bs
import datetime
import time


class hfutSpider(scrapy.Spider):
    name = 'hfut'
    base_url = 'http://news.hfut.edu.cn/'
    url_template = info['hfut']['url_template']
    tag_codes = info['hfut']['tag_codes']
    count = 0

    def start_requests(self):
        for code in self.tag_codes:
            url = render_url(self.url_template, tag_code=code, page=1)
            yield Request(url, self.parse_index, meta={'tag_code': code})

    def parse_index(self, response):
        # print (response.url)
        max_page = int(response.xpath('//*[@id="pages"]/a/text()').extract()[-2])
        # print(max_page)
        code = response.meta['tag_code']
        for p in range(1, 5):
            url = render_url(self.url_template, tag_code=code, page=p)
            # print(url)
            yield Request(url, self.get_news, meta={'tag_code': code}, dont_filter=True)

    def get_news(self, response):
        code = response.meta['tag_code']
        soup = bs(response.text, 'html.parser')
        # ul = soup.find(id='pages').previous
        ul = soup.find(class_=['content', 'list'])
        li = ul.find_all('li')
        for l in li:
            if l.a:
                url = self.base_url + l.a.attrs['href']  # 该属性使用相对路径
                # print(url)
                title = l.a.text
                time_ = l.span.text
                # print(url, time)
                yield Request(url, self.get_content, dont_filter=True,
                              meta={'tag_code': code,
                                    'title': title,
                                    'time': time_})

    def get_content(self, response):
        self.count += 1
        # print('crawl No.%s: %s' % (self.count, response.meta['title']))
        soup = bs(response.text, 'html.parser')
        content = soup.find(id='artibody')

        meta = response.meta
        item = NewsItem()
        item['imgs'] = get_img_urls(content, self.base_url)
        item['content'] = content_process(content, self.base_url).encode('utf-8')
        item['title'] = meta['title']
        item['time'] = datetime.datetime.strptime(meta['time'], '%Y-%m-%d').date()
        item['url'] = response.url
        item['unit'] = info['hfut']['unit']
        item['type'] = self.tag_codes[meta['tag_code']]
        item['timestamp'] = datetime.datetime.utcfromtimestamp(int(time.time()))
        return item

    def get_content_test(self, response):
        self.count += 1
        print('crawl No.%s: %s' % (self.count, response.meta['time']))










