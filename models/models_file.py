import logging
from enum import Enum
from http import HTTPStatus
from time import sleep
from typing import TYPE_CHECKING

from flask import Response as FResponse
from flask import request, jsonify
from yaml import load, Loader

from utils.tools import ReSearching, abspath

if TYPE_CHECKING:
    from typing import List


class AppConfiguration:
    def __init__(self, mockoon_file, flask_debug, logging_level, host):
        self.mockoon_file = abspath(mockoon_file)
        self.flask_debug = flask_debug
        self.logging_level = logging_level
        self.host = host

    @classmethod
    def fromDict(cls, data: dict) -> object:
        mockoon_file = data.get("mockoon_file", "mockoon_files/mockoon_configuration.json")
        flask_debug = data.get("flask_debug", False)

        logging_level = data.get('logging_level', logging.INFO)
        if type(logging_level) == str:
            logging_level = logging._nameToLevel.get(logging_level, logging.INFO)
        if logging_level is None:
            logging_level = logging.INFO

        host = data.get('host_addr', "0.0.0.0")
        default_keys = ["mockoon_file", "flask_debug", 'logging_level', 'host_addr']
        logger = logging.getLogger(__name__)
        for key in default_keys:
            if key not in data.keys():
                logger.info("Key missing: %s, loading from default", key)

        return cls(mockoon_file, flask_debug, logging_level, host)

    @classmethod
    def fromFile(cls, path="config.yaml"):
        path = abspath(path)
        try:
            with open(path) as f:
                config = load(f, Loader=Loader)
        except FileNotFoundError:
            logger = logging.getLogger(__name__)
            logger.error("Configuration file not found. Starting from defaults")
            config = {}
        return cls.fromDict(config)


class Method(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"


class Response:
    def __init__(self, status_code: int, body: str, method: str, latency: int, headers: dict) -> None:
        logger = logging.getLogger(__name__)
        self.body = body
        self.latency = latency
        self.headers = headers
        try:
            self.status_code = HTTPStatus(status_code)
        except ValueError as e:
            logger.error("Your config file passed invalid status code: %s", e)
            raise SystemExit
        try:
            self.method = Method(method.upper())
        except ValueError as e:
            logger.error("Your config file passed invalid method: %s", e)
            raise SystemExit

    def __repr__(self) -> str:
        return f"Response {self.method} after {self.latency} {self.status_code}: {self.body}"

    @classmethod
    def fromDict(cls, data: dict, method: str) -> object:
        body = data.get("body")
        statusCode = int(data.get("statusCode"))
        method = method
        latency = data.get("latency")
        headers = data.get("headers",[])
        new_headers = {header.get("key"): header.get("value") for header in headers}
        return cls(statusCode, body, method, latency, new_headers)


class Endpoint:
    def __init__(self, endpoint: str, responses: "List[Response]", headers: dict) -> None:
        self.responses = responses
        self.endpoint = f"/{endpoint}"
        self.headers = headers

    def __repr__(self) -> str:
        return f"Endpoint: \"{self.endpoint}\" responses: {self.responses}"

    @classmethod
    def fromDict(cls, data: dict, headers: 'List[dict]') -> object:
        endpoint = cls.adapt_route(data['endpoint'])
        response = data["responses"][0]
        responses = [Response.fromDict(response, data["method"])]

        new_headers = {header.get("key"): header.get("value") for header in headers}

        return cls(endpoint, responses, new_headers)

    @classmethod
    def responseFromDict(cls, data: dict) -> object:
        response = data["responses"][0]
        return Response.fromDict(response, data["method"])

    @classmethod
    def adapt_route(cls, route: str) -> str:
        params = ReSearching.search_path(route)
        for param in params:
            route = route.replace(param, f"<{param[1:]}>", 1)
        # mockoon passes url Variables as ":var", and flask requires "<var>".
        # Therefor we need to replace all ":string" with "<string>".
        # Allowed signs in variable names are "A-z0-9_", as "-" is treated differently by mockoon and flask
        return route

    def view_maker(self) -> callable:
        def view_func(*args, **kwargs):
            for response in self.responses:
                if request.method == response.method.value:
                    sleep(response.latency / 1000)
                    body = response.body
                    param_dict = {"urlParam": kwargs, "queryParam": request.args, "header": request.headers}
                    params = ReSearching.search_params(body)
                    for param in params:
                        total = param[0]
                        type = param[1]
                        var_name = param[2][1:-1]
                        default = param[3][1:-1]
                        replacement = total
                        if type in param_dict: replacement = (
                            param_dict[type][var_name] if var_name in param_dict[type] else default)
                        body = body.replace(total, replacement, 1)
                    kwargs_dict = {"method": request.method, "hostname": request.host, "ip": request.remote_addr}
                    kwparams = ReSearching.search_keywoards(body)
                    for kwparam in kwparams:
                        total = kwparam[0]
                        name = kwparam[1]
                        if name in kwargs_dict: body = body.replace(total, kwargs_dict[name], 1)
                    responseheaders = self.headers
                    responseheaders.update(response.headers)
                    response = FResponse(body, headers=responseheaders, status=response.status_code)
                    return response

        return view_func


class Environment:
    def __init__(self, name: str, endpoint_prefix: str, port: int, endpoints: 'List[Endpoint]') -> None:
        self.name = name
        self.endpoint_prefix = endpoint_prefix
        self.port = port
        self.endpoints = endpoints

    def __repr__(self) -> str:
        return f"Environment: \"{self.name}\""

    @classmethod
    def fromDict(cls, dict: dict, endpoints: 'List[Endpoint]') -> object:
        name = dict['name']
        endpointPrefix = dict['endpointPrefix']
        port = dict['port']
        return cls(name, endpointPrefix, port, endpoints)
