from http.client import HTTPResponse
from typing import Union, List
from flask import jsonify


class Response:

    def __init__(self, status_code: int, body: Union[dict, list]) -> None:
        self._status_code = status_code
        self._body = body

    @property
    def status_code(self) -> int:
        return self._status_code

    @property
    def body(self) -> Union[dict, list]:
        return self._body

    @staticmethod
    def success(body: Union[dict, list] = None) -> 'Response':
        return Response(status_code=200, body=body or {})

    @staticmethod
    def created_successfully(created_id: str = None) -> 'Response':
        return Response(status_code=201, body={
            'id': created_id
        } if created_id else {})

    @staticmethod
    def bad_request(message: str = None, validation_errors: List[str] = None) -> 'Response':
        messages = []
        if message:
            messages.append(message)
        if validation_errors:
            messages.append(f'Validation error: {", ".join(validation_errors)}')
        return Response(status_code=400, body={
            'message': '. '.join(messages)
        } if messages else {})

    @staticmethod
    def conflict(message: str = None) -> 'Response':
        return Response(status_code=409, body={
            'message': message
        } if message else {})

    @staticmethod
    def server_error(message: str = None) -> 'Response':
        return Response(status_code=500, body={
            'message': message
        } if message else {})

    def jsonify(self) -> HTTPResponse:
        jsonified_response = jsonify(self.body)
        jsonified_response.status_code = self.status_code
        return jsonified_response
