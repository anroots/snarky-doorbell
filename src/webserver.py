import psutil
import time
from flask import Flask
from flask import render_template
from flask import jsonify

app = Flask(__name__)


@app.route("/", methods=['GET'])
def hello():
    return render_template('hello.html')

@app.route("/stats", methods=['GET'])
def stats():
    stats = {
        'uptime':  round(time.time() - psutil.boot_time()),
        'time': (time.time()),
        'total_rings': 0,
        'rings_since_boot': 0,
        'current_volume': 0,
        'current_style': 0,
        'current_voice': 0,
        'last_ring': 0
    }
    return jsonify(stats)