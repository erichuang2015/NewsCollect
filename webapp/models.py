# -*- coding: utf-8 -*-
from app import db


class News(db.Model):
    __tablename__ = 'news'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)  # 标题
    unit = db.Column(db.String)  # 文章所属单位
    type = db.Column(db.String)  # 文章类型
    time = db.Column(db.Date)  # 发布时间
    url = db.Column(db.String)  # 文章位置
    imgs = db.Column(db.PickleType)  # 图片链接列表
    content = db.Column(db.Text)  # html正文
    timestamp = db.Column(db.TIMESTAMP)  # 抓取时间戳