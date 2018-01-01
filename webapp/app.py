# -*- coding: utf-8 -*-
from flask import Flask, jsonify, current_app, request, \
                    render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
import os, sys
from bs4 import BeautifulSoup as bs
from erros import not_found
from info import info
from utils import jsonp, get_tag_list
from sqlalchemy.sql import func
import datetime

app = Flask(__name__, template_folder='templates')
app.debug = True
bootstrap = Bootstrap(app)
# db_path = os.path.abspath('.') + '\data.db'
db_path = 'mysql+pymysql://root:ssh0912@localhost/NewCollect'
app.config['SQLALCHEMY_DATABASE_URI'] = db_path # 'sqlite:///' + db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
db.create_all()

#    __  __                       _          _
#   |  \/  |   ___    _   _    __| |   ___  | |  ___
#   | |\/| |  / _ \  | | | |  / _` |  / _ \ | | / __|
#   | |  | | | (_) | | |_| | | (_| | |  __/ | | \__ \
#   |_|  |_|  \___/   \__,_|  \__,_|  \___| |_| |___/

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

#          _      ____    ___
#         / \    |  _ \  |_ _|
#        / _ \   | |_) |  | |
#       / ___ \  |  __/   | |
#      /_/   \_\ |_|     |___|

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
            latest: 更新时间戳
        }
    ]
    """
    unit_info = []
    for unit in info:
        try:
            timestamp = News.query.filter_by(unit=info[unit]['unit'])\
                            .order_by('timestamp').first().timestamp
            timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S")
        except AttributeError as e:
            print(e)
            timestamp = '状态获取失败'
        item = {
            'code': unit,
            'tag_codes': info[unit]['tag_codes'],
            'name': info[unit]['unit'],
            'latest': timestamp,
        }
        unit_info.append(item)
    return jsonify(unit_info)


@app.route('/api/news/<unit_code>')
@jsonp
def get_news_list(unit_code):
    """
    获取单位新闻列表 
    params:
        tag: 新闻tag
        num: 获取条数
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
    q = News.query.filter_by(unit=info[unit_code]['unit']).order_by('time')
    if tag is not None:
        q = q.filter_by(type=tag)
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
    q = News.query.filter_by(id=id).first()
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

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/detail/<unit>')
def detail_redirect(unit):
    tag_list = get_tag_list(info[unit]['tag_codes'])
    return redirect(url_for('detail', unit=unit, tag=tag_list[0]))     

@app.route('/detail/<unit>/<tag>')
def detail(unit, tag):
    """
    详情页
    params:
        page: 页数
    """
    tag_list = get_tag_list(info[unit]['tag_codes'])
    # 分页数据获取需要优化
    q = News.query.filter_by(unit=info[unit]['unit'], type=tag).order_by('time').all()
    max_page = len(q)
    page = int(request.args.get('page', 1))
    if page < 1:
        page = 1
    news_list = []
    for i in range(20 * (page - 1), 20 * page)[::-1]:
        try:
            item = {
                'title': q[i].title,
                'id': q[i].id,
                'time': q[i].time.strftime('%y-%m-%d'),
                'url': q[i].url,
            }
            news_list.append(item)
        except IndexError:
            break
    data = {
        'unit_code': unit,
        'unit': info[unit]['unit'],
        'tag_list': tag_list,
        'current_tag': tag,
        'page': page,
        'max_page': max_page,
        'news_list': news_list,
    }
    print(data['page'], data['max_page'])
    # current_app.logger.debug(url_for('detail', unit=unit, tag=tag_list[2], param=111))
    return render_template('detail.html', data=data)  

if __name__ == '__main__':
    app.run()
 
