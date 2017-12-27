# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, Date, Text, PickleType, create_engine, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from utils import get_conf_from_json

conf = get_conf_from_json('conf.json')
if conf is None:
    db_conf = {
        "using_db": "mysql",
        "db_info": {
            "mysql": {
                "usr": "root",
                "host": "localhost"
            }
        }
    }
else:
    db_conf = conf['db']
using_db = db_conf['using_db']
if using_db is None:
    using_db = 'mysql'
pw = 'ssh0912' # os.environ.get('MYSQL_PASSWORD', None)


# 对象基类
Base = declarative_base()

class News(Base):
    __tablename__ = 'news'

    id = Column(Integer, primary_key=True)
    title = Column(String)  # 标题
    unit = Column(String)  # 文章所属单位
    type = Column(String)  # 文章类型
    time = Column(Date)  # 发布时间
    url = Column(String)  # 文章位置
    imgs = Column(PickleType)  # 图片链接列表
    content = Column(Text)  # html正文
    timestamp = Column(TIMESTAMP)  # 抓取时间戳


def get_session(db_name='dev.db'):
    if using_db is 'mysql':
        db_path = 'mysql://{}:{}@{}'.format(
            db_conf['db_info']['mysql']['usr'], pw, db_conf['db_info']['mysql']['host'])
    if using_db is 'sqlite':
        db_path = 'sqlite:///' + os.path.abspath('..') + '\%s' % db_name
    print(db_path)
    engine = create_engine(db_path)
    Base.metadata.create_all(engine)
    db_session = sessionmaker(bind=engine)
    return db_session()


if __name__ == '__main__':
   get_session()

