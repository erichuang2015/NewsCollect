# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, Date, Text, PickleType, create_engine, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from .utils import get_conf_from_json


conf = get_conf_from_json('conf.json')
if conf is None:
    raise Exception("Can't import conf")
db_conf = conf['db']
using_db = db_conf['using_db']
if using_db is None:
    using_db = 'mysql'
pw = 'ssh0912' # os.environ.get('MYSQL_PASSWORD', None)
if pw is None:
    raise Exception("Can't get password of MySQL")
mysql_info = db_conf['db_info'].get('mysql', None)
if mysql_info is None and db_conf['using_db'] is 'mysql':
    raise Exception("Can't gey MySQL info")

# 对象基类
Base = declarative_base()

class News(Base):
    __tablename__ = 'news'

    id = Column(Integer, primary_key=True)
    title = Column(String(255))  # 标题
    unit = Column(String(255))  # 文章所属单位
    type = Column(String(255))  # 文章类型
    time = Column(Date)  # 发布时间
    url = Column(String(255))  # 文章位置
    imgs = Column(PickleType)  # 图片链接列表
    content = Column(Text)  # html正文
    timestamp = Column(TIMESTAMP)  # 抓取时间戳


def get_session(db_name='dev.db'):
    # if using_db is 'mysql':
    db_path = 'mysql+pymysql://{}:{}@{}/{}?charset=utf8'.format(
        mysql_info['usr'], pw, mysql_info['host'], mysql_info['database'])
    # if using_db is 'sqlite':
    #    db_path = 'sqlite:///' + os.path.abspath('..') + '\%s' % db_name
    engine = create_engine(db_path)
    Base.metadata.create_all(engine)
    db_session = sessionmaker(bind=engine)
    return db_session()


if __name__ == '__main__':
   get_session()

