from typing import List, Any
from src.utils.http.response import Response


class BaseController:

    def __init__(self):
        self.request = None
        self.token = None
        self.response = None

    def on_request(self):
        pass

    def after_request(self):
        pass

    def ok(self, data={}) -> Response:
        return Response(200, data)

    def created_ok(self, created_id: Any = None):
        body = {}
        if created_id:
            body = {'id': str(created_id)}
        return Response(201, body)

    def get_json_body(self):
        return self.request.json

    def error(self, message: str):
        return Response(500, {'message': message})

    def validation_error(self, validation_errors: List[str]) -> Response:
        return Response(400, {'message': f'Validation error: {", ".join(validation_errors)}'})

    def get_authenticated_user_id(self):
        if self.token and 'id' in self.token:
            return self.token['id']
        return None
