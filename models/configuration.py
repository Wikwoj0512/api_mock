import json
from typing import TYPE_CHECKING

# from .logger import create_logger
from logging import getLogger
from .models_file import Endpoint, Environment, abspath

if TYPE_CHECKING:
    from typing import List


class ServicesConfiguration:
    def __init__(self, path: str) -> None:
        self.path = abspath(path)

    def load_configuration(self) -> 'List[Environment]':
        try:

            with open(self.path, "r") as f:
                conf = json.load(f)
        except FileNotFoundError as e:
            logger = getLogger("main")
            logger.error("File %s not found: %s", {self.path}, e)
            raise SystemExit

        data = conf["data"]

        environments = []
        for item in data:
            item = item["item"]
            endpoints = []

            for route in item["routes"]:
                used = False
                for endpoint in endpoints:
                    if endpoint.endpoint == f"/{Endpoint.adapt_route(route['endpoint'])}":
                        used = True
                        endpoint.responses.append(Endpoint.responseFromDict(route))
                if not used: endpoints.append(Endpoint.fromDict(route))

            environments.append(Environment.fromDict(item, endpoints))

        return environments
