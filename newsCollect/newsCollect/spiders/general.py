import scrapy
from scrapy.http import Request
from ..items import NewsItem
from .info import info as info_
from .utils import *
from bs4 import BeautifulSoup as bs
import datetime
import time

conf = get_conf_from_json('../conf.json').get('spider', None)
if conf is None:
    raise Exception('Load config failed')

class general(scrapy.Spider):
    name = 'general'
    loads = conf.get('general_load', [])

    def start_requests(self, test=False, crawl_list=[], *args, **kwargs):
        if test:
            self.loads = []
        self.loads.extend(crawl_list)
        for unit in self.loads:
            info = info_[unit]
            rules = info.get('rules', None)
            base = rules.get('base_url', None)
            url_template = rules.get('url_template', None)
            for code in info['tag_codes']:
                url = render_url(url_template, tag_code=code, page=1)
                yield Request(url, self.parse_index, dont_filter=True,
                            meta={
                                'unit_code': unit,
                                'tag_code': code,
                                'rules': rules
                            })
    
    def parse_index(self, response):
        rules = response.meta['rules']
        tag_code = response.meta['tag_code']
        unit = response.meta['unit_code']
        max_page = response.xpath(rules['max_page_xpath']).extract()[0]
        for page in range(1, int(conf['crawl_page'] + 1)):
            if page > int(max_page):
                break
            url = render_url(rules['url_template'], tag_code=tag_code, page=page)
            yield Request(url, self.parse_list, 
                        meta={
                            'unit_code': unit,
                            'tag_code': tag_code,
                            'rules': rules
                        })
        
    def parse_list(self, response):
        tag_code = response.meta['tag_code']
        unit = response.meta['unit_code']
        rules = response.meta['rules']
        news_len = len(response.xpath(rules['container_xpath'] + '/li'))
        print(news_len)
        for i in range(1, news_len + 1): # xpath从1计数
            time = response.xpath(rules['container_xpath'] + 
                        '/li[{}]'.format(i) + rules['time_xpath']).extract()[0] # 需要修饰时间格式
            url = rules['base_url'] + response.xpath(rules['container_xpath'] +
                                            '/li[{}]'.format(i) + rules['url_xpath']).extract()[0]
            print(url)
            yield Request(url, self.get_content,
                          meta={
                              'unit_code': unit,
                              'tag_code': tag_code,
                              'time': time,
                              'rules': rules,
                          })
    
    def get_content(self, response):
        meta = response.meta
        rules = meta['rules']
        title = response.xpath(rules['title_xpath']).extract()[0]
        soup = bs(response.text, 'html.parser')
        if rules['content_id']: # 如果使用id
            content = soup.find('div', id=rules['content_id'])
        elif rules['content_class']:
            content = soup.find('div', class_=rules['content_class'])
        else:
            content = None

        if content is None:
            raise Exception('Can not get content')
        
        item = NewsItem()
        item['imgs'] = get_img_urls(content, rules['base_url'])
        item['content'] = content_process(content, rules['base_url']).encode('utf-8')
        item['title'] = title
        # datetime.datetime.strptime(meta['time'], '%Y-%m-%d').date()
        item['time'] = meta['time']
        item['url'] = response.url
        item['unit'] = info[meta['unit_code']]['unit']
        item['type'] = info[meta['unit_code']]['tag_codes'][meta['tag_code']]
        item['timestamp'] = datetime.datetime.utcfromtimestamp(int(time.time()))

        print(item['title'], item['time'])



