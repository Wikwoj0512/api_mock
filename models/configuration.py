import json
from typing import TYPE_CHECKING

from .models_file import Endpoint, Environment

if TYPE_CHECKING:
    from typing import List

class Configuration:
    def __init__(self, path: str) -> None:
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
                    if endpoint.endpoint == f"/{route['endpoint']}":
                        used = True
                        endpoint.responses.append(Endpoint.responseFromDict(route))
                if not used: endpoints.append(Endpoint.fromDict(route))

            environments.append(Environment.fromDict(item, endpoints))

        return environments