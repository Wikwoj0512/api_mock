import logging
from typing import TYPE_CHECKING

from flask import Flask

from utils.logger import create_logger
from models.models_file import Environment, Endpoint

if TYPE_CHECKING:
    from typing import List
    from models.models_file import Environment, Endpoint


class Server:
    def __init__(self, host: str, port: int, endpoint_prefix: str, endpoints: 'List[Endpoint]', name: str,
                 debug=False, logging_level=logging.INFO) -> None:
        self.host = host
        self.debug = debug
        self.port = port
        self.endpoint_prefix = endpoint_prefix
        self.endpoints = endpoints
        self.name = name.replace(" ", "_")
        self.logging_level = logging_level

    @classmethod
    def factory(cls, host: str, environment: 'Environment', debug=False, logging_level=logging.INFO) -> object:
        return cls(host, environment.port, environment.endpoint_prefix, environment.endpoints, environment.name, debug,
                   logging_level)

    def setup(self):
        app = Flask(self.name)

        for endpoint in self.endpoints:
            prefix = self.endpoint_prefix
            responses = endpoint.responses
            methods = [response.method.value for response in responses]  # One path can not be added twice in flask, even with different methods
            # ->adding all the endpoins for one path to flask as one endpoint with multiple responses
            app.add_url_rule(
                f"{f'/{prefix}' if prefix else ''}{endpoint.endpoint}",
                endpoint.endpoint,
                methods=methods,
                view_func=endpoint.view_maker()
            )
        return app

    def run(self) -> None:
        app = self.setup()
        try:
            create_logger(self.name, self.logging_level)
        except FileNotFoundError as e:
            logger = create_logger(level=self.logging_level)
            logger.error("Invalid environment name \"%s\": %s", self.name, e)
            raise SystemExit
        app.run(self.host, self.port, self.debug)
