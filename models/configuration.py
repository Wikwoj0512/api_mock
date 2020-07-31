import json

from logging import getLogger
from typing import TYPE_CHECKING

from .models_file import Endpoint, Environment, abspath

if TYPE_CHECKING:
    from typing import List




def load_configuration(path: str) -> 'List[Environment]':
    path = abspath(path)
    try:

        with open(path, "r", encoding="utf8") as f:
            conf = json.load(f)
    except FileNotFoundError as e:
        logger = getLogger(__name__)
        logger.error("File %s not found: %s", {path}, e)
        raise SystemExit

    data = conf["data"]

    environments = []
    for environment in data:
        environment = environment["item"]
        endpoints = []

        for route in environment["routes"]:
            used = False
            for endpoint in endpoints:
                if endpoint.endpoint == f"/{Endpoint.adapt_route(route['endpoint'])}":
                    used = True
                    endpoint.responses.append(Endpoint.responseFromDict(route))
            if not used:
                endpoints.append(Endpoint.fromDict(route, environment.get("headers")))

        environments.append(Environment.fromDict(environment, endpoints))

    return environments
