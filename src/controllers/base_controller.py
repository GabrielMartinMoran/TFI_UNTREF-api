from src.routing.router import Router
from typing import Optional
from flask import jsonify
from src.utils import global_variables


def normalize_alias(alias: str) -> Optional[str]:
    if alias is not None and len(alias) > 0:
        return F'/{alias}' if alias[0] != '/' else alias
    return None


def http_method(method_type: str, alias: str = None, auth_required: bool = False):
    def wrapper(func):
        Router.register_http_method({
            'type': method_type,
            'alias': normalize_alias(alias),
            'class_name': func.__qualname__.split('.')[0],
            'method_name': func.__name__,
            'auth_required': auth_required
        })
        return func

    return wrapper


class BaseController:

    def __init__(self):
        self.request = None
        self.token = None
        self.response = None

    def on_request(self):
        pass

    def after_request(self):
        pass

    def __jsonify_response(self, data, status_code):
        response = jsonify(data)
        response.status_code = status_code
        return response

    def ok_success(self, data={}):  # pylint: disable=no-self-use
        return self.__jsonify_response(data, 200)

    def created_ok(self, created_id):
        return self.__jsonify_response({'id': str(created_id)}, 201)

    def get_json_body(self):
        return self.request.json

    def error(self, message):  # pylint: disable=no-self-use
        return self.__jsonify_response({'message': message}, 500)

    def validation_error(self, validation_errors):  # pylint: disable=no-self-use
        #return self.__jsonify_response({'invalid_properties': attributes_with_errors}, 400)
        return self.__jsonify_response({'message': f'Validation error: {", ".join(validation_errors)}'}, 400)

    def get_authenticated_user_id(self):
        if self.token and 'id' in self.token:
            return self.token['id']
        return None
