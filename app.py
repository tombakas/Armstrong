#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

from flask import Flask
from flask import request
from flask import render_template

import script

app = Flask(__name__)


@app.route('/get-tables', methods=['POST'])
def poop():
    data = request.get_json()
    print(data)
    j = script.process_request(data)
    html = render_template("tables.html", table=j)
    return json.dumps({'success': True, 'data': html}), 200, {'ContentType': 'application/json'}


@app.route('/')
def hello_world():
    return render_template("index.html")


def create_app(debug=True):
    app = Flask(__name__)
    app.debug = debug

    return app


if __name__ == "__main__":
    app.run()
