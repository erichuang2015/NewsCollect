# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()  # 标题
    unit = scrapy.Field()  # 文章所属单位
    type = scrapy.Field()  # 文章类型
    time = scrapy.Field()  # 发布时间
    url = scrapy.Field()  # 文章位置
    imgs = scrapy.Field()  # 图片链接列表
    content = scrapy.Field()  # html正文
    timestamp = scrapy.Field()  # 抓取时间戳
    # imgs_replace = scrapy.Field() # 备份图片链接


