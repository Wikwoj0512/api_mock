from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import List

import logging
from enum import Enum


logger = logging.getLogger("main")


class StatusCode(Enum):
    OK = "200"
    NOT_FOUND = "404"


class Method(Enum):
    GET = "GET"
    POST = "POST"


class Response:
    def __init__(self, status_code: str, body: str, method: str) -> None:
        self.body = body
        try:
            self.status_code = StatusCode(status_code)
        except ValueError as e:
            logger.error("Your config file passed invalid status code: %s", e)
            raise SystemExit
        try:
            self.method = Method(method.upper())
        except ValueError as e:
            logger.error("Your config file passed invalid method: %s", e)
            raise SystemExit

    def __repr__(self) -> str:
        return f"Response {self.method} {self.status_code}: {self.body}"

    @classmethod
    def fromDict(cls, data: dict, method: str) -> object:
        body = data["body"]
        statusCode = data["statusCode"]
        method = method
        return cls(statusCode, body, method)


class Endpoint:
    def __init__(self, endpoint: str, responses: "List[Response]") -> None:
        self.responses = responses
        self.endpoint = endpoint

    def __repr__(self) -> str:
        return f"Endpoint: \"{self.endpoint}\" responses: {self.responses}"

    @classmethod
    def fromDict(cls, data: dict) -> object:
        endpoint = f"/{data['endpoint']}"
        response = data["responses"][0]
        responses = [Response.fromDict(response, data["method"])]
        return cls(endpoint, responses)

    @classmethod
    def responseFromDict(cls, data: dict) -> object:
        response = data["responses"][0]
        return Response.fromDict(response, data["method"])


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
