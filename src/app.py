from os import environ 
import re

import requests
from flask import Flask, render_template, request
from flask_moment import Moment

from utils import read_yaml

YAML_FILE = environ.get('FEED_YAML') # Path to source yaml file

app = Flask(__name__)
moment = Moment(app)


def probe_api(url: str):
    try:
        response = requests.get(url)
    except Exception as e:
        return str(e)
    return str(response.status_code)


def get_feed_data(filename):
    input_feed = read_yaml(filename)
    map_target = input_feed["map"]
    status_check = input_feed["status-check"]
    target_info = input_feed["target"]
    return dict(
        map_target=map_target, status_check=status_check, target_info=target_info
    )


@app.route("/probe_status", methods=["GET"])
def probe_status():
    query_url = str(request.args.get('url'))
    request_status = probe_api(query_url)
    return request_status


@app.route("/", methods=["GET"])
def index():
    feed_data = get_feed_data(YAML_FILE)
    map_target = feed_data["map_target"]
    status_check = feed_data["status_check"]
    target_info = feed_data["target_info"]
    pattern = "^http.*|^www\..*"
    re_func = lambda x: re.match(pattern, x)
    return render_template(
        "status.html",
        column_model=map_target,
        status_check=status_check,
        target_data=target_info,
        link_checker=re_func
    )
