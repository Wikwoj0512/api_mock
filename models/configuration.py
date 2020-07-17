import json
import os
import sys
from typing import TYPE_CHECKING

from .models_file import Endpoint, Environment

if TYPE_CHECKING:
    from typing import List


class ServicesConfiguration:
    def __init__(self, path: str) -> None:
        if path[1] != ":": path = os.path.join(sys.argv[1], path)
        self.path = path

    def load_configuration(self) -> 'List[Environment]':
        with open(self.path, "r") as f:
            conf = json.load(f)

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
