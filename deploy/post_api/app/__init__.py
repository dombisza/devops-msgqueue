import time
import logging
from flask import Flask, jsonify, request
from flask_caching import Cache
import requests
import json
import redis
from jsonschema import validate
APP = Flask(__name__)
APP.config.from_pyfile('config.py')

def validate_body(body):
    j_schema = {"type":"object","properties":{"id":{"type":"string"},"metadata":{"type":"object","properties":{"param1":{"type":"string"},"param2":{"type":"string"},"param3":{"type":"integer"}},"required":["param1","param2","param3"]},"owner":{"type":"string"},"req_time":{"type":"integer"}},"required":["id","metadata","owner","req_time"]}
    try:
        validate(instance=body, schema=j_schema)
    except jsonschema.exceptions.ValidationError as err:
        print(err)
        err = "JSON invalid"
        return Fasle, err
    return True

@APP.route('/', methods=['POST'])
def add_job_to_q():
    REDIS_HOST = 'mqueue'
    PAYLOAD_DB = 0
    SORT_DB = 1
    if request.method == 'POST':
        logging.info('post')
        body = request.get_json()
        validate_body(body)
        uuid = body['id']
        r = redis.StrictRedis(REDIS_HOST, db=PAYLOAD_DB)
        r_time = redis.StrictRedis(REDIS_HOST, db=SORT_DB)
        if r.execute_command('JSON.GET', uuid):
            return("key already in use")
        else:
            r.execute_command('JSON.SET', uuid, '.', json.dumps(body))
            r_time.set(body['req_time'], uuid)
            return uuid
