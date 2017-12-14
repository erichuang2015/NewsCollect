# -*- coding: utf-8 -*-
from flask import Flask, jsonify, current_app, request, render_template
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
import os, sys
from bs4 import BeautifulSoup as bs
from erros import not_found
from info import info
from utils import jsonp

# reload(sys)
# sys.setdefaultencoding('utf8')

app = Flask(__name__, template_folder='templates')
app.debug = True
bootstrap = Bootstrap(app)
db_path = os.path.abspath('..') + '\data.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
db = SQLAlchemy(app)
manager = Manager(app)

#          _      ____    ___
#         / \    |  _ \  |_ _|
#        / _ \   | |_) |  | |
#       / ___ \  |  __/   | |
#      /_/   \_\ |_|     |___|


# from models import News
import models
@app.route('/api/unit_list')
@jsonp
def unit_list():
    """
    获取已有单位
    :return:
    [
        {
            code: 单位代码
            name: 单位名称,
            tag_codes: tag代码及名称,
        }
    ]
    """
    unit_info = []
    for unit in info:
        item = {
            'code': unit,
            'tag_codes': info[unit]['tag_codes'],
            'name': info[unit]['unit'],
        }
        unit_info.append(item)
    return jsonify(unit_info)


@app.route('/api/<unit_code>')
@jsonp
def get_news_list(unit_code):
    """
    获取单位新闻列表
    :return:
    [ ...
    {
        title: 标题,
        id: 新闻id
        time: 发布时间,
        url: 链接,
    }
    ...]
    """
    news_list = []
    tag = request.args.get('tag', None)
    num = int(request.args.get('num', 10))
    q = models.News.query.filter_by(unit=unicode(
        info[unit_code]['unit'])).order_by('time')
    if tag is not None:
        q = q.filter_by(type=unicode(tag))
    q = q.all()
    if q is None:
        return not_found("items not found")
    for i in range(num)[::-1]:
        try:
            item = {
                'title': '【' + q[i].type + '】' + q[i].title,
                'id': q[i].id,
                'time': q[i].time.strftime('%y-%m-%d'),
                'url': q[i].url,
            }
            news_list.append(item)
        except IndexError:
            break
    return jsonify(news_list)


@app.route('/api/news/<int:id>')
@jsonp
def get_news(id):
    """

    :param id:
    :return:
    """
    q = models.News.query.filter_by(id=id).first()
    if q is None:
        return not_found('news not found')
    soup = bs(q.content, 'html.parser')
    content = soup.body.find('div')
    res = {
        'id': q.id,
        'title': q.title,
        'type': q.type,
        'unit': q.unit,
        'time': q.time.strftime('%y-%m-%d'),
        'url': q.url,
        'content': content.prettify(),
        'timestamp': q.timestamp,
    }
    return jsonify(res)


#       __     __  _
#       \ \   / / (_)   ___  __      __  ___
#        \ \ / /  | |  / _ \ \ \ /\ / / / __|
#         \ V /   | | |  __/  \ V  V /  \__ \
#          \_/    |_|  \___|   \_/\_/   |___/

@app.route('/detail/<unit>')
def show_detail(unit):
    current_app.logger.debug(current_app.template_folder)
    return render_template('test.html')


@app.route('/')
def index():
    return 'test'

if __name__ == '__main__':
    app.run()
