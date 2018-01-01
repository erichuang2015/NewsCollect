# -*- coding: utf-8 -*-
import json
import redis
import os
import sys

defult_conf_path = os.path.split(os.path.abspath(__file__))[0] + '/conf.json'

def get_conf_from_json(path=defult_conf_path):
    f = sys._getframe()
    filename = f.f_back.f_code.co_filename
    file_dir = os.path.split(os.path.abspath(filename))[0] # 实现相对目录导入
    if path[0] is not '/': # 处理同目录文件的情况
        path = '/' + path
    path = file_dir + path
    # print(path)
    try:
        with open(path, 'r') as f:
            config = json.load(f)
    except IOError as e:
        print(e)
        return None
    # print(config)
    return config

def clear_redis(conf_path='conf.json'):
    conf = get_conf_from_json(conf_path)
    redis_conf = conf['redis']
    redis_db = redis.Redis(host=redis_conf['host'], port=redis_conf['port'])
    redis_db.flushdb()

        
if __name__ == '__main__':
    print(get_conf_from_json(os.path.split(os.path.abspath(__file__))[0] + '/conf.json'))
