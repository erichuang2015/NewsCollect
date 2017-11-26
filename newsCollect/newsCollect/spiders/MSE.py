# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from ..items import NewsItem
from .info import info
from .utils import *
from bs4 import BeautifulSoup as bs
import datetime
import time


class EA(scrapy.Spider):
    name = 'MSE'
    base_url = 'http://mse.hfut.edu.cn'
    url_template = info['MSE']['url_template']
    tag_codes = info['MSE']['tag_codes']
    count = 0

    def start_requests(self):
        for code in self.tag_codes:
            url = render_url(self.url_template, tag_code=code)
            yield Request(url, self.parse_index, meta={'type': self.tag_codes[code]})

    def parse_index(self, response):
        soup = bs(response.text, 'html.parser')
        li_list = soup.find('div', class_='ab_txt').find_all('li')
        for li in li_list:
            a = li.find('div', class_='news_menu1').a
            title = a.string
            url = self.base_url + '/' + a.attrs['href']
            time_ = li.find('div', class_='news_date').string
            yield Request(url, self.get_content, meta={'type': response.meta['type'],
                                                       'title': title,
                                                       'time': time_})

    def get_content(self, response):
        soup = bs(response.text, 'html.parser')
        content = soup.find('div', class_='new_xx')

        meta = response.meta
        item = NewsItem()
        item['imgs'] = get_img_urls(content, self.base_url)
        item['content'] = content_process(content, self.base_url).encode('utf-8')
        item['title'] = meta['title']
        item['time'] = datetime.datetime.strptime(meta['time'], '%Y/%m/%d').date()
        item['url'] = response.url
        item['unit'] = info['MSE']['unit']
        item['type'] = meta['type']
        item['timestamp'] = datetime.datetime.utcfromtimestamp(int(time.time()))
        return item
        # print item
