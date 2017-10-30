# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup as bs
from bs4 import NavigableString, Tag
import requests

'''
TODO: 2017/10/22
    - 优化content_process对class处理
'''


def render_url(template, **kwargs):
    for item in kwargs:
        try:
            template = template.replace('[' + item + ']', str(kwargs[item]))
        except Exception as e:
            print(e.message)
            continue
    return template


def unicode2str(text):
    return text.encode('unicode-escape').decode('string_escape')


def content_process(content, base_url):
    content = clone_bs4_elem(content)
    if content is None:
        return None
    del content['class']  # 删除属性
    soup = bs('<html><head><meta charset="utf-8"></head><body></body></html>', 'html.parser')
    soup.body.append(content)  # 插入内容
    # print (soup.prettify())
    no_script_list = soup.find_all("noscript")
    for no_script in no_script_list:
        no_script.extract()  # 删除noscript
    img_list = soup.find_all('img')
    for img in img_list:
        img_url_complement(img, base_url)
    return soup.prettify()


def clone_bs4_elem(el):
    """Clone a bs4 tag before modifying it.

    Code from `http://stackoverflow.com/questions/23057631/clone-element-with
    -beautifulsoup`
    """
    if isinstance(el, NavigableString):
        return type(el)(el)
    try:
        copy = Tag(None, el.builder, el.name, el.namespace, el.nsprefix)
    except:
        return None
    # work around bug where there is no builder set
    # https://bugs.launchpad.net/beautifulsoup/+bug/1307471
    copy.attrs = dict(el.attrs)
    for attr in ('can_be_empty_element', 'hidden'):
        setattr(copy, attr, getattr(el, attr))
    for child in el.contents:
        copy.append(clone_bs4_elem(child))
    return copy


def get_img_urls(content, base_url):
    if content is None:
        return None
    img_list = content.find_all('img')
    if img_list is None:
        return None
    img_url = []
    for img in img_list:
        img_url.append(img_url_complement(img, base_url).attrs['src'])
    return img_url


def img_url_complement(img, base_url):
    try:
        requests.get(img.attrs['src'])  # 测试链接可用性
    except requests.exceptions.MissingSchema:
        img.attrs['src'] = base_url + img.attrs['src']
    return img

if __name__ == '__main__':
    r = requests.get('http://news.hfut.edu.cn/show-1-72510-1.html')
    s = bs(r.content)
    div = s.find(id='artibody')
    # print(content_process(div, 'http://news.hfut.edu.cn/'))
    print (get_img_urls(div, 'http://news.hfut.edu.cn/'))