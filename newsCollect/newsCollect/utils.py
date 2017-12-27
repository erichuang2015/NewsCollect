# -*- coding: utf-8 -*-
import json
import redis
import os

defult_conf_path = os.path.split(os.path.abspath(__file__))[0] + '/conf.json'

def get_conf_from_json(path=defult_conf_path):
    try:
        with open(path, 'r') as f:
            config = json.load(f)
    except IOError as e:
        print(e)
        return None
    return config

def clear_redis(conf_path='conf.json'):
    conf = get_conf_from_json(conf_path)
    redis_conf = conf['redis']
    redis_db = redis.Redis(host=redis_conf['host'], port=redis_conf['port'])
    redis_db.flushdb()

        
if __name__ == '__main__':
    print(get_conf_from_json(os.path.split(os.path.abspath(__file__))[0] + '/conf.json'))
