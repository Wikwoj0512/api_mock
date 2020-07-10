import logging
from time import sleep
from typing import TYPE_CHECKING

from flask import Flask, Response, jsonify, request

from models.logger import create_logger

if TYPE_CHECKING:
    from typing import List
    from models.models_file import Environment, Response, Endpoint

import re

param_search = re.compile("(\{\{ *([A-z0-9_]+){1}( *'[A-z0-9._]+'){1} *('[\S ]+')* *\}\})")
keywords_search = re.compile("(\{\{ *([A-z0-9_]+) *\}\})")


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

        # funkcja służąca do zwrócenia funkcji view_func dla flaska. Używam tego + add_url_rule zamiast @app.route(), aby dodawać wszystkie endpointy z listy.
        def view_maker(responses: 'List[Response]') -> object:

            def view_func(*args, **kwargs):
                for response in responses:
                    if request.method == response.method.value:
                        sleep(response.latency / 1000)
                        body = response.body
                        param_dict = {"urlParam": kwargs, "queryParam": request.args}
                        params = param_search.findall(body)
                        for param in params:
                            total = param[0]
                            type = param[1]
                            var_name = param[2].replace(" ", "").replace("'", "")
                            default = param[3]
                            replacement = (
                                param_dict[type][var_name] if var_name in param_dict[type] else default[1:-1])
                            body = body.replace(total, replacement, 1)

                        kwargs_dict = {"method": request.method, "hostname": request.host, "ip": request.remote_addr}
                        kwparams = keywords_search.findall(body)
                        for kwparam in kwparams:
                            total = kwparam[0]
                            name = kwparam[1]
                            if name in kwargs_dict: body = body.replace(total, kwargs_dict[name], 1)

                        return body
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
