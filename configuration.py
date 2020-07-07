import json
from flask import Flask, Response, jsonify, request
from enum import Enum


class StatusCode(Enum):
    OK = "200"
    NOT_FOUND = "404"

class Method(Enum):
    GET = "get"
    POST = "post"

class Response:
    def __init__(self, status_code, body, method):
        self.body = body
        try:
            self.status_code = StatusCode(status_code)
        except ValueError as e:
            print(f"Your config file passed invalid status code: {e}")#logi
            raise SystemExit
        try:
            self.method = Method(method)
        except:
            raise SystemExit

    def __repr__(self):
        return f"Response {self.method} {self.status_code}: {self.body}"

    @classmethod
    def fromDict(cls, dict, method):
        body = dict["body"]
        statusCode = dict["statusCode"]
        method = method
        return cls(statusCode, body, method)


class Endpoint:
    def __init__(self, endpoint,  responses):
        self.responses = responses
        self.endpoint = endpoint


    def __repr__(self):
        return f"Endpoint: \"{self.endpoint}\" responses: {self.responses}"

    @classmethod
    def fromDict(cls, dict):

        endpoint = f"/{dict['endpoint']}"
        response = dict["responses"][0]
        responses = [Response.fromDict(response, dict["method"])]
        return cls(endpoint, responses)

    @classmethod
    def responseFromDict(cls, dic):
        response = dic["responses"][0]
        # print(dic["responses"])
        return Response.fromDict(response, dic["method"])


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
                used = False
                for endpoint in endpoints:
                    if endpoint.endpoint == f"/{route['endpoint']}":
                        used = True
                        endpoint.responses.append(Endpoint.responseFromDict(route))
                if not used: endpoints.append(Endpoint.fromDict(route))
            # print(endpoints)

            environments.append(Environment.fromDict(item, endpoints))

        return environments


class Server:
    def __init__(self, host, port, endpoint_prefix, endpoints, debug=False):
        self.host = host
        self.debug = debug
        self.port = port
        self.endpoint_prefix = endpoint_prefix
        self.endpoints = endpoints

    @classmethod
    def factory(cls, host, environment, debug=False):
        return cls(host, environment.port, environment.endpoint_prefix, environment.endpoints, debug)

    def setup(self):
        app = Flask(__name__)

        #funkcja służąca do zwrócenia funkcji view_func dla flaska. Używam tego + add_url_rule zamiast @app.route(), aby dodawać wszystkie endpointy z listy.
        def view_maker(responses):
            def view_func():

                for response in responses:
                    if request.method == response.method.value.upper():
                        return jsonify(eval(response.body))
                return Response(status_code=404)
            return view_func



        for endpoint in self.endpoints:
            prefix = self.endpoint_prefix
            responses = endpoint.responses
            methods = [response.method.value.upper() for response in responses] #endpointy nie mogą się powtarzać -> dodanie warunków zwrocenia wartości do klasy, dodawanie wielu metod do 1 endpointu
            # print(self.endpoints)/
            app.add_url_rule(
                f"/{prefix}{endpoint.endpoint}",
                endpoint.endpoint,
                methods=methods,
                view_func=view_maker(responses)
            )
        return app


    def run(self):
        app = self.setup()
        app.run(self.host, self.port, self.debug)






