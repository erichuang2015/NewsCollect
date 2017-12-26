# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, Date, Text, PickleType, create_engine, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os


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


def get_session(db_name):
    db_path = os.path.abspath('..') + '\%s' % db_name
    engine = create_engine('sqlite:///' + db_path)
    Base.metadata.create_all(engine)
    db_session = sessionmaker(bind=engine)
    return db_session()


if __name__ == '__main__':
   pass

