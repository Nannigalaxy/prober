from os import environ

import requests
from flask import Flask, render_template, request
from flask_moment import Moment

from utils import (get_domain_certificate, get_root_domain, re_url_checker,
                   read_yaml)

YAML_FILE_URL = environ.get('FEED_YAML') # Path to source yaml file

app = Flask(__name__)
moment = Moment(app)


def get_feed_data(filename):
    input_feed = read_yaml(filename)
    map_target = input_feed["map"]
    status_check = input_feed["status-check"]
    target_info = input_feed["target"]
    return dict(
        map_target=map_target, status_check=status_check, target_info=target_info
    )


def probe_api(url: str):
    try:
        response = requests.get(url)
    except Exception as e:
        return str(e)
    return str(response.status_code)


def get_domain_metadata(domain_list: str):
    domain_data = {}
    for domain in domain_list:
        domain_data[domain] = get_domain_certificate(domain)
    return domain_data


def get_metadata(target_info):
    domain_list = []
    for target in target_info:
        for entity in target_info[target]:
            for value in entity.values():
                if re_url_checker(value):
                    domain_list.append(get_root_domain(value))

    domain_list = list(set(domain_list))
    domain_data = get_domain_metadata(domain_list)
    return domain_data


@app.route("/probe_status", methods=["GET"])
def probe_status():
    query_url = str(request.args.get("url"))
    request_status = probe_api(query_url)
    return request_status


@app.route("/", methods=["GET"])
def index():
    feed_data = get_feed_data(YAML_FILE_URL)
    map_target = feed_data["map_target"]
    status_check = feed_data["status_check"]
    target_info = feed_data["target_info"]
    domain_data = get_metadata(target_info)
    return render_template(
        "status.html",
        column_model=map_target,
        status_check=status_check,
        target_data=target_info,
        link_checker=re_url_checker,
        domain_data=domain_data,
    )
