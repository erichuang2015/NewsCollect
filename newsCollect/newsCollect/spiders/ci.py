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


conf = get_conf_from_json('../conf.json').get('spider', None)
if conf is None:
    raise Exception('Load config failed')

class CI(scrapy.Spider):
    name = 'CI'
    base_url = 'http://ci.hfut.edu.cn'
    url_template = info['CI']['url_template']
    tag_codes = info['CI']['tag_codes']
    count = 0

    def start_requests(self):
        print(conf)
        for code in self.tag_codes:
            url = render_url(self.url_template, tag_code=code, page=1)
            yield Request(url, self.parse_index, dont_filter=True, meta={'tag_code': code})

    def parse_index(self, response):
        max_page = int(response.xpath('//*[@id="wp_paging_w6"]/ul/li[3]/span[1]/em[2]/text()').extract()[0])
        tag_code = response.meta['tag_code']
        for page in range(1, int(conf['crawl_page'] + 1)):
            if page > max_page:
                break
            url = render_url(self.url_template, tag_code=tag_code, page=page)
            yield Request(url, self.parse_list, meta={'tag_code': tag_code})

    def parse_list(self, response):
        tag_code = response.meta['tag_code']
        soup = bs(response.text, 'html.parser')
        news_list = soup.find('ul', class_='wp_article_list').find_all('li')
        for li in news_list:
            time = li.find('span', class_='Article_PublishDate').string
            url = self.base_url + li.find('span', class_='Article_Title').a.attrs['href']
            yield Request(url, 
                self.get_content, 
                meta={
                    'tag_code': tag_code,
                    'time': time,
                })
        
    def get_content(self, response):
        title = response.xpath(
            '//*[@id="container"]/div/div/div/h1/text()').extract()[0]
        soup = bs(response.text, 'html.parser')
        content = soup.find('div', class_='entry')

        meta = response.meta
        item = NewsItem()
        item['imgs'] = get_img_urls(content, self.base_url)
        item['content'] = content_process(content, self.base_url).encode('utf-8')
        item['title'] = title
        item['time'] = datetime.datetime.strptime(meta['time'], '%Y-%m-%d').date()
        item['url'] = response.url
        item['unit'] = info['CI']['unit']
        item['type'] = self.tag_codes[meta['tag_code']]
        item['timestamp'] = datetime.datetime.utcfromtimestamp(int(time.time()))
        return item
