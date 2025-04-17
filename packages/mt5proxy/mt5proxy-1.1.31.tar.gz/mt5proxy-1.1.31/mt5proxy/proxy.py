#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: qicongsheng
import datetime

import pytz
from flask import Flask, jsonify
from flask.globals import request
from flask_httpauth import HTTPBasicAuth

from . import mt5client

app = Flask(__name__)
auth = HTTPBasicAuth()

users = {
    "admin": "password"
}


@app.route("/get_symbols", methods=["get", "post"])
@auth.login_required
def get_symbols():
    return mt5client.get_symbols()


@app.route("/copy_rates_from", methods=["get", "post"])
@auth.login_required
def copy_rates_from():
    symbol = request.args.to_dict().get("symbol").upper()
    time_frame = request.args.to_dict().get("time_frame").upper()
    date_from = request.args.to_dict().get("date_from")
    count = request.args.to_dict().get("count")
    date_from = datetime.datetime.strptime(date_from, "%Y%m%d%H%M%S").astimezone(pytz.timezone("Etc/UTC"))
    return mt5client.copy_rates_from(symbol, time_frame, date_from, count)


@app.route("/copy_rates_range", methods=["get", "post"])
@auth.login_required
def copy_rates_range():
    symbol = request.args.to_dict().get("symbol").upper()
    time_frame = request.args.to_dict().get("time_frame").upper()
    date_from = request.args.to_dict().get("date_from")
    date_from = datetime.datetime.strptime(date_from, "%Y%m%d%H%M%S").astimezone(pytz.timezone("Etc/UTC"))
    date_to = request.args.to_dict().get("date_to")
    date_to = datetime.datetime.strptime(date_to, "%Y%m%d%H%M%S").astimezone(pytz.timezone("Etc/UTC"))
    return mt5client.copy_rates_range(symbol, time_frame, date_from, date_to)


@app.route("/get_all_bar_times", methods=["get", "post"])
@auth.login_required
def get_all_bar_times():
    symbol = request.args.to_dict().get("symbol").upper()
    time_frame = request.args.to_dict().get("time_frame").upper()
    return mt5client.get_all_bar_times(symbol, time_frame)


@app.route("/get_all_bars", methods=["get", "post"])
@auth.login_required
def get_all_bars():
    symbol = request.args.to_dict().get("symbol").upper()
    time_frame = request.args.to_dict().get("time_frame").upper()
    return mt5client.get_all_bars(symbol, time_frame)


@auth.get_password
def get_password(username):
    if username in users:
        return users.get(username)
    return None


@auth.error_handler
def unauthorized():
    return jsonify({"error": "Unauthorized access"}), 401


@app.errorhandler(404)
def page_not_found(error):
    return "Leave me alone."


@app.errorhandler(400)
def page_not_found(error):
    return "FUCK OFF!"


def start(debug=False, host='0.0.0.0', port=8082):
    app.run(debug=debug, host=host, port=port, threaded=True)


if __name__ == "__main__":
    start()
