import json
import requests
import redis
import time
from random import randrange
import etcd3
import os

REDIS_HOST = os.environ['REDIS_HOST'] 
REDIS_PORT = os.environ['REDIS_PORT']
PAYLOAD_DB = os.environ['PAYLOAD_DB']
SORT_DB = os.environ['SORT_DB']
ETCD_HOST = os.environ['ETCD_HOST']

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
    r = redis.Redis(REDIS_HOST, port=REDIS_PORT, db=SORT_DB)
    timestamps = r.keys()
    print(timestamps)
    if timestamps == []:
        print('No task in queue...')
        return False
    else:
        sorted_list = sorted(timestamps, key=int)
        first_obj = r.get(sorted_list[0])
        print(first_obj)
        if first_obj == None:
            print(first_obj)
            return False
        else:
            r.delete(sorted_list[0])
            return first_obj.decode("utf-8")

def update_queue(uuid):
    r = redis.Redis(REDIS_HOST, port=REDIS_PORT, db=PAYLOAD_DB)
    if r.execute_command('JSON.DEL', uuid) == 0:
        print("{} deleted from redis".format(uuid))
        return True
    else:
        return False



def main():
    r = redis.Redis(REDIS_HOST, REDIS_PORT, PAYLOAD_DB)
    while True:
        uuid = None 
        if uuid := select_task():
            print(uuid)
            json_object = json.loads(r.execute_command('JSON.GET', uuid))
            etcd_client = etcd3.client(host=ETCD_HOST)
            print(json_object)
            if build_task(json_object):
                update_queue(uuid)
                etcd_client.put(uuid, 'Success')
                print("task {} success".format(uuid))
            else:
                update_queue(uuid)
                etcd_client.put(uuid, 'Failed')
                print("task {} failed".format(uuid))
        time.sleep(5)
if __name__ == '__main__':
    main()
