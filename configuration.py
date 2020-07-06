import json
from flask import Flask, Response, jsonify
from enum import Enum


class StatusCode(Enum):
    OK = "200"
    NOT_FOUND = "404"

class Method(Enum):
    # GET = "get"
    POST = "post"

class Response:
    def __init__(self, status_code, body):
        try:
            self.body = body
            self.status_code = StatusCode(status_code)
        except ValueError as e:
            print(f"Your config file passed invalid status code: {e}")
            raise SystemExit

    def __repr__(self):
        return f"Response {self.status_code}: {self.body}"

    @classmethod
    def fromDict(cls, dict):
        try:
            body = dict["body"]
            statusCode = StatusCode(dict["statusCode"])
            return cls(statusCode,body )
        except ValueError as e:
            print(f"Your config file passed invalid status code: {e}")
            raise SystemExit


class Endpoint:
    def __init__(self, endpoint, method, responses):
        try:
            self.endpoint = endpoint
            self.method = Method(method)
            self.responses = responses
        except ValueError as e:
            print(f"Your config file passed invalid method: {e}")
            raise SystemExit

    def __repr__(self):
        return f"Endpoint: \"{self.endpoint}\""

    @classmethod
    def fromDict(cls, dict,  responses):
        try:
            endpoint = f"/{dict['endpoint']}"
            method = Method(dict["method"])
            return cls(endpoint, method, responses)
        except ValueError as e:
            print(f"Your config file passed invalid method: {e}")
            raise SystemExit


class Environment:
    def __init__(self, name, endpoint_prefix, port, endpoints):
        self.name = name
        self.endpoint_prefix = endpoint_prefix
        self.port = port
        self.endpoints = endpoints

    def __repr__(self):
        return f"Environment: \"{self.name}\""

    @classmethod
    def fromDict(cls, dict, endpoints):
        name = dict['name']
        endpointPrefix = dict['endpointPrefix']
        port = dict['port']
        return cls (name, endpointPrefix, port, endpoints)


class Configuration:
    def __init__(self, path):
        self.path = path

    def load_configuration(self):
        with open(self.path, "r") as f:
            conf = json.load(f)

        data = conf["data"]

        environments = []
        for item in data:
            item = item["item"]
            endpoints = []
            for route in item["routes"]:
                responses = []
                for response in route["responses"]:
                    responses.append(Response.fromDict(response))
                endpoints.append(Endpoint.fromDict(route,responses))
            environments.append(Environment.fromDict(item, endpoints))

        return environments


class Server:
    def __init__(self, host, debug, environment):
        self.host = host
        self.debug = debug
        self.port = environment.port
        self.endpoint_prefix = environment.endpoint_prefix
        self.endpoints = environment.endpoints
    def setup(self):
        app = Flask(__name__)

        #funkcja służąca do zwrócenia funkcji view_func dla flaska. Używam tego + add_url_rule zamiast @app.route(), aby dodawać wszystkie endpointy z listy.
        def view_maker(body):
            def view_func():
                rv = eval(body)
                return jsonify(rv)
            return view_func

        for endpoint in self.endpoints:
            prefix = self.endpoint_prefix
            response = endpoint.responses[0]

            app.add_url_rule(
                f"/{prefix}{endpoint.endpoint}",
                endpoint.endpoint,
                methods=[endpoint.method.value.upper()], #endpointy nie mogą się powtarzać -> dodanie warunków zwrocenia wartości do klasy, dodawanie wielu metod do 1 endpointu
                view_func=view_maker(response.body)
            )
        return app


    def run(self):
        app = self.setup()
        app.run(self.host, self.port, self.debug)






