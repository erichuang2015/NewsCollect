# -*- coding: utf-8 -*-
import json
import redis

def get_conf_from_json(path):
    try:
        with open(path) as f:
            config = json.load(f)
    except IOError:
        return None
    return config

def clear_redis(conf_path='conf.json'):
    conf = get_conf_from_json(conf_path)
    redis_conf = conf['redis']
    redis_db = redis.Redis(host=redis_conf['host'], port=redis_conf['port'])
    redis_db.flushdb()
        
if __name__ == '__main__':
    clear_redis()