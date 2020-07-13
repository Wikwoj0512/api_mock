import logging
from typing import TYPE_CHECKING

from flask import Flask

from models.logger import create_logger

if TYPE_CHECKING:
    from typing import List
    from models.models_file import Environment, Endpoint


class Server:
    def __init__(self, host: str, port: int, endpoint_prefix: str, endpoints: 'List[Endpoint]', name: str,
                 debug=False) -> None:
        self.host = host
        self.debug = debug
        self.port = port
        self.endpoint_prefix = endpoint_prefix
        self.endpoints = endpoints
        self.name = name.replace(" ", "_")

    @classmethod
    def factory(cls, host: str, environment: 'Environment', debug=False) -> object:
        return cls(host, environment.port, environment.endpoint_prefix, environment.endpoints, environment.name, debug)

    def setup(self):
        app = Flask(self.name)

        for endpoint in self.endpoints:
            prefix = self.endpoint_prefix
            responses = endpoint.responses
            methods = [response.method.value for response in responses]  # endpointy nie mogą się powtarzać ->
            # dodanie warunków zwrocenia wartości do klasy, dodawanie wielu metod do 1 endpointu
            app.add_url_rule(
                f"/{prefix}{endpoint.endpoint}",
                endpoint.endpoint,
                methods=methods,
                view_func=endpoint.view_maker()
            )
        return app

    def run(self) -> None:
        app = self.setup()
        try:
            create_logger(self.name)
        except FileNotFoundError as e:
            create_logger()
            logger = logging.getLogger()
            logger.error("Invalid environment name \"%s\": %s", self.name, e)
            raise SystemExit
        app.run(self.host, self.port, self.debug)
