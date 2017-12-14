# coding: utf-8
from functools import wraps
from flask import request, current_app
from info import info

def jsonp(func):
    """Wraps JSONified output for JSONP requests."""
    @wraps(func)
    def decorated_function(*args, **kwargs):
        callback = request.args.get('callback', False)
        if callback:
            data = str(func(*args, **kwargs).data)
            content = str(callback) + '(' + data + ')'
            mimetype = 'application/javascript'
            return current_app.response_class(content, mimetype=mimetype)
        else:
            return func(*args, **kwargs)
    return decorated_function


def get_tag_list(tag_codes):
    """递归获取tag_codes中的tag"""
    tag_list = []
    travel(tag_codes, tag_list)
    return tag_list

def travel(tree, node_list):
    """递归获取树的所有叶子节点list"""
    for node in tree:
        if type(tree[node]) is not dict:
            node_list.append(tree[node])
        else:
            travel(tree[node], node_list)


if __name__ == '__main__':
    print(get_tag_list(info['jxgc']['tag_codes']))