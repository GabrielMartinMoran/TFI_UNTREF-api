from flask import jsonify
from src.utils.http import http_methods


class CORSSolver:

    REQUEST_METHOD_HEADER = 'Access-Control-Request-Method'
    ALLOW_ORIGIN_HEADER = 'Access-Control-Allow-Origin'
    ORIGIN_HEADER = 'Origin'
    ALLOW_METHODS_HEADER = 'Access-Control-Allow-Methods'
    ALLOW_HEADERS_HEADER = 'Access-Control-Allow-Headers'
    REQUESTS_HEADERS_HEADER = 'Access-Control-Request-Headers'
    MAX_AGE_HEADER = 'Access-Control-Max-Age'
    ALLOW_CREDENTIALS_HEADER = 'Access-Control-Allow-Credentials'
    MAX_AGE = 86400

    def __init__(self, request):
        self.request = request

    def is_cors_request(self) -> bool:
        return self.request.method == http_methods.OPTIONS

    def get_wanted_http_metod(self) -> str:
        return self.request.headers[self.REQUEST_METHOD_HEADER]

    def get_cors_response(self):
        response = jsonify(ssuccess=True)
        req_h = self.request.headers
        response.headers[self.ALLOW_ORIGIN_HEADER] = req_h[self.ORIGIN_HEADER]
        response.headers[self.ALLOW_METHODS_HEADER] = req_h[self.REQUEST_METHOD_HEADER]
        response.headers[self.ALLOW_HEADERS_HEADER] = req_h[self.REQUESTS_HEADERS_HEADER]
        response.headers[self.MAX_AGE_HEADER] = self.MAX_AGE
        response.headers[self.ALLOW_CREDENTIALS_HEADER] = 'true'
        return response
