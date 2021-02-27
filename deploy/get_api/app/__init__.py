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
#CACHE = Cache(APP)

def validate_body(body):
    schema = {"type":"object","properties":{"id":{"type":"string"},"metadata":{"type":"object","properties":{"param1":{"type":"string"},"param2":{"type":"string"},"param3":{"type":"string"}},"required":["param1","param2","param3"]},"owner":{"type":"string"},"req_time":{"type":"integer"}},"required":["id","metadata","owner","req_time"]}
    if not validate(instance=body, schema=schema):
        return "body not valid"


@APP.route('/<uuid>', methods=['GET'])
def check_job(uuid):
    # get request should return the satus of the job from the queue or from the state db
    # get localhost:5001/${job id}
    if request.method == 'GET':
        logging.info('api1')
        return jsonify({'api': 'one'})
    # generate uuid for the job
    # post should check the id against the redis and etcd
    # if it is not in the db it should add it to the redis queue
@APP.route('/', methods=['POST'])
def add_job_to_q():
    if request.method == 'POST':
        logging.info('post')
        body = request.get_json()
        #validate_body(json)
        uuid = body['id']
        #r = redis.Redis(host='mqueue', port=6379)
        #r.set(uuid, str(json))

        r = redis.StrictRedis('mqueue', db=0)
        r_time = redis.StrictRedis('mqueue', db=1)
        if r.execute_command('JSON.GET', uuid):
            return("key already in use")
        else:
            r.execute_command('JSON.SET', uuid, '.', json.dumps(body))
            r_time.set(body['req_time'], uuid)
            return uuid
