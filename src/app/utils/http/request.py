from typing import Union


class Request:

    def __init__(self, method: str, path: str, body: Union[dict, list]) -> str:
        self._method = method
        self._path = path
        self._body = body

    @property
    def method(self) -> str:
        return self._method

    @property
    def path(self) -> str:
        return self._path

    @property
    def body(self) -> Union[dict, list]:
        return self._body

    @staticmethod
    def from_body(body: Union[dict, list]) -> 'Request':
        return Request(None, None, body)
