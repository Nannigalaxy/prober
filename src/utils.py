import yaml
import requests

def read_yaml(url_filename: str) -> dict:
    file = requests.get(url_filename)
    prime_service = yaml.safe_load(file.text)
    return prime_service
