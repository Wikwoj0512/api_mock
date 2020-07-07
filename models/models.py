from enum import Enum
import logging
logger = logging.getLogger("main")

class StatusCode(Enum):
    OK = "200"
    NOT_FOUND = "404"

class Method(Enum):
    GET = "GET"
    POST = "POST"

class Response:
    def __init__(self, status_code, body, method):

        self.body = body
        try:
            self.status_code = StatusCode(status_code)
        except ValueError as e:
            logger.error(f"Your config file passed invalid status code: {e}")
            raise SystemExit
        try:
            self.method = Method(method.upper())
        except ValueError as e:
            logger.error(f"Your config file passed invalid method: {e}")
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
