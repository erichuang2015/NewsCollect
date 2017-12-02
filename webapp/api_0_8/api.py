# -*- coding: utf-8 -*-
import sys
from flask import jsonify, current_app, request
from bs4 import BeautifulSoup as bs
from ..models import News
from . import api_0_8
from ..erros import not_found
from ..info import info
from ..utils import jsonp

reload(sys)
sys.setdefaultencoding('utf8')


@api_0_8.route('/unit_list')
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


@api_0_8.route('/news/<unit_code>')
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
    q = News.query.filter_by(unit=unicode(info[unit_code]['unit'])).order_by('time')
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


@api_0_8.route('/news/<int:id>')
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



