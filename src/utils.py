import yaml


def read_yaml(filename: str) -> dict:
    with open(filename, 'r') as file:
        prime_service = yaml.safe_load(file)
        return prime_service
