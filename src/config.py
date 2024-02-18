from __future__ import annotations

import pathlib
from dataclasses import dataclass
from functools import lru_cache
from typing import Union
from urllib import parse

from kombu import Queue
from starlette.config import Config
from starlette.datastructures import Secret
from typing_extensions import Self

configuration = Config(".env")


@dataclass
class CeleryConfig:
    broker_url = configuration("CELERY_BROKER_URL")
    result_backend = configuration("CELERY_RESULT_BACKEND")




environment_name = configuration.get("APP_ENVIRONMENT")
settings = get_settings(config_name=environment_name)

