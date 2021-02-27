import json
import requests
import redis
import time
from random import randrange
import etcd3

def build_task(build_object):
    s_time = build_object['metadata']['param3']
    print("{} {}".format(build_object['metadata']['param1'], build_object['metadata']['param2']))
    x = 0
    #for simulation purpose lets make every 5th build failed
    rng = randrange(5)
    print(rng)
    while x < s_time:
        print('building...')
        time.sleep(1)
        x = x + 1
    if rng == 2:
        print("build {} failed.".format(build_object['id']))
        return False
    else:
        print("build {} success.".format(build_object['id']))
        return True


def select_task():
    r = redis.Redis('127.0.0.1', port=6379, db=1)
    timestamps = r.keys()
    sorted_list = sorted(timestamps, key=int)
    first_obj = r.get(sorted_list[0])
    print(first_obj)
    if first_obj == None:
        print(first_obj)
        return False
    else:
        return first_obj.decode("utf-8")

def update_queue(uuid):
    r = redis.Redis('127.0.0.1', port=6379, db=0)
    if r.execute_command('JSON.DEL', uuid) == 0:
        print("{} deleted from redis".format(uuid))
        return True
    else:
        return False



def main():
    redis_host = '127.0.0.1'
    redis_port = 6379
    while True:
        r = redis.Redis(redis_host, redis_port, db=0)
        uuid = select_task()
        print(uuid)
        json_object = json.loads(r.execute_command('JSON.GET', uuid))
        etcd_client = etcd3.client()
        print(json_object)
        if build_task(json_object):
            update_queue(uuid)
            etcd_client.put(uuid, 'Success')
            print("task {} success".format(uuid))
            #add to state
        else:
            #add to state that the build failed
            update_queue(uuid)
            etcd_client.put(uuid, 'Failed')
            print("task {} failed".format(uuid))
if __name__ == '__main__':
    main()
