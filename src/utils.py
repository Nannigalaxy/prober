import re
import ssl
from datetime import datetime

import OpenSSL
import requests
import yaml
from tld import get_tld


def read_yaml(url_filename: str) -> dict:
    try:
        file = requests.get(url_filename)
        file_content = file.text
    except:
        with open(url_filename, "r") as file:
            file_content = file.read()
    prime_service = yaml.safe_load(file_content)
    return prime_service


def re_url_checker(url: str) -> bool:
    pattern = "^http.*|^www\..*"
    re_func = lambda x: re.match(pattern, x)
    return bool(re_func(url))


def get_root_domain(url: str) -> str:
    res = get_tld(url, as_object=True)
    return res.fld


def get_domain_certificate(url: str):
    cert = ssl.get_server_certificate((url, 443))
    x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)
    b_date = str(x509.get_notAfter(), encoding="utf-8")[:8]
    exp_date = datetime.strptime(b_date, "%Y%m%d").date()
    cert_remain_days = (exp_date - datetime.now().date()).days
    cert_exp_date = exp_date.strftime("%d %B %Y")
    cert_issuer = x509.get_issuer().O
    cert_data = dict(
        expires_on=cert_exp_date, days_left=cert_remain_days, issuer=cert_issuer
    )
    return cert_data
