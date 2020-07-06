import json
from flask import Flask, Response, jsonify

class Response:
    def __init__(self, status_code, body):
        self.body = body
        self.status_code = status_code

    def __repr__(self):
        return f"Response {self.status_code}: {self.body}"

    @classmethod
    def fromDict(cls, dict):
        body = dict["body"]
        statusCode = dict["statusCode"]
        return cls(statusCode,body )

class Endpoint:
    def __init__(self, endpoint, method, responses):
        self.endpoint = endpoint
        self.method = method
        self.responses = responses

    def __repr__(self):
        return f"Endpoint: \"{self.endpoint}\""

    @classmethod
    def fromDict(cls, dict,  responses):
        endpoint = f"/{dict['endpoint']}"
        method = dict["method"]
        return cls(endpoint, method, responses)


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
        self.environment = environment
        self.endpoint_prefix = environment.endpoint_prefix
        self.endpoints = environment.endpoints
        self.port = environment.port

    def setup(self):
        app = Flask(__name__)

        view_maker = lambda body: (lambda: jsonify(eval(body)))

        for endpoint in self.endpoints:
            prefix = self.endpoint_prefix
            response = endpoint.responses[0]

            app.add_url_rule(
                f"/{prefix}{endpoint.endpoint}",
                endpoint.endpoint,
                methods=[endpoint.method.upper()], #endpointy nie mogą się powtarzać -> dodanie warunków zwrocenia wartości do klasy, dodawanie wielu metod do 1 endpointu
                view_func=view_maker(response.body)
            )
        return app


    def run(self):
        app = self.setup()
        app.run(self.host, self.port, self.debug)






