import json
import os
import re

import psutil
import time

import redis
from flask import Flask
from flask import render_template
from flask import jsonify

app = Flask(__name__)
r = redis.StrictRedis(host='localhost', port=6379, db=0)
log_path = '/opt/doorbell/logs'


@app.route("/", methods=['GET'])
def hello():
    return render_template('hello.html')


@app.route("/stats", methods=['GET'])
def stats():
    doorbell_stats = {
        'uptime': int(round(time.time() - psutil.boot_time())),
        'time': int(round(time.time())),
        'total_rings': int(r.get('total_rings')),
        'rings_since_boot': int(r.get('rings_since_boot')),
        'current_volume': int(r.get('volume')),
        'current_style': int(r.get('style')),
        'current_voice': int(r.get('voice')),
        'last_ring': int(round(float(r.get('last_ring'))))
    }
    return jsonify(doorbell_stats)


def is_ringing():
    return time.time() - float(r.get('last_ring')) < 3


@app.route("/poll", methods=['GET'])
def poll():
    request_time = time.time()

    while not is_ringing():
        if time.time() - request_time > 60:
            break
        time.sleep(1)

    return jsonify({
        'currently_ringing': is_ringing(),
        'last_ring': float(r.get('last_ring')),
        'time': time.time()
    })


@app.route("/log/<int:year>/<int:month>", methods=['GET'])
def log(year, month):
    path = '%s/%s-%s.json' % (log_path,year, month)

    if not os.path.exists(path):
        return jsonify({'error': 'Log file not found'}), 404

    with open(path) as data_file:
        logs = json.load(data_file)

    return jsonify(logs)


@app.route("/logs", methods=['GET'])
def logs():
    files = os.listdir(log_path)
    log_routes = []
    for file in files:
        if not file.endswith('.json'):
            continue
        m = re.match(r'^(?P<year>[0-9]{4})-(?P<month>[0-9]{2})\.json$', file)
        log_routes.append('/log/%s/%s' % (m.group('year'), m.group('month')))

    return jsonify(log_routes)