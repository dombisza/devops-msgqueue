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
    schema = {"type":"object","properties":{"id":{"type":"string"},"metadata":{"type":"object","properties":{"param1":{"type":"string"},"param2":{"type":"string"},"param3":{"type":"string"}},"required":["param1","param2","param3"]},"owner":{"type":"string"},"req_time":{"type":"integer"}},"required":["id","metadata","owner","req_time"]}
    if not validate(instance=body, schema=schema):
        return "body not valid"


@APP.route('/<uuid>', methods=['GET'])
def check_job(uuid):
    if request.method == 'GET':
        logging.info('api1')
        return jsonify({'api': 'one'})