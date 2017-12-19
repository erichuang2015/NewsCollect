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


if __name__ == '__main__':
    conf = get_conf_from_json('conf.json')
    redis_conf = conf['redis']
    redis_db = redis.Redis(
        host=redis_conf['host'], port=redis_conf['port'], db=4)
    print(redis_db.hlen('test'))