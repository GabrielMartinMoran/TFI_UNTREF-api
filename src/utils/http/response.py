from http.client import HTTPResponse
from typing import Any
from flask import jsonify


class Response:

    def __init__(self, status_code: int, body: Any) -> None:
        self.status_code = status_code
        self.body = body

    def jsonify(self) -> HTTPResponse:
        jsonified_response = jsonify(self.body)
        jsonified_response.status_code = self.status_code
        return jsonified_response
