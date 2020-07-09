import json
import logging

from enum import Enum
from flask import Flask, Response, jsonify, request

from models.logger import create_logger


class Server:
    def __init__(self, host, port, endpoint_prefix, endpoints, name, debug=False):
        self.host = host
        self.debug = debug
        self.port = port
        self.endpoint_prefix = endpoint_prefix
        self.endpoints = endpoints
        self.name = name.replace(" ", "_")

    @classmethod
    def factory(cls, host, environment, debug=False):
        return cls(host, environment.port, environment.endpoint_prefix, environment.endpoints, environment.name, debug)

    def setup(self):
        app = Flask(self.name)

        # funkcja służąca do zwrócenia funkcji view_func dla flaska. Używam tego + add_url_rule zamiast @app.route(), aby dodawać wszystkie endpointy z listy.
        def view_maker(responses):
            def view_func():

                for response in responses:
                    if request.method == response.method.value:
                        return jsonify(eval(response.body))
                return Response(status_code=404)

            return view_func

        for endpoint in self.endpoints:
            prefix = self.endpoint_prefix
            responses = endpoint.responses
            methods = [response.method.value for response in responses]  # endpointy nie mogą się powtarzać ->
            # dodanie warunków zwrocenia wartości do klasy, dodawanie wielu metod do 1 endpointu
            app.add_url_rule(
                f"/{prefix}{endpoint.endpoint}",
                endpoint.endpoint,
                methods=methods,
                view_func=view_maker(responses)
            )
        return app

    def run(self):
        app = self.setup()
        try:
            create_logger(self.name)
        except FileNotFoundError as e:
            create_logger()
            logger = logging.getLogger()
            logger.error("Invalid environment name \"%s\": %s",self.name, e)
            raise SystemExit
        app.run(self.host, self.port, self.debug)
