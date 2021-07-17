from flask import jsonify
from src.controllers.base_controller import BaseController, http_method
from src.repositories.user_repository import UserRepository
from src.models.user import User
import src.utils.http_methods as http_methods


class UsersController(BaseController):

    def __init__(self):
        super().__init__()
        self.user_repository = UserRepository()

    @http_method(http_methods.POST)
    def create(self) -> dict:
        user = User.from_dict(self.get_json_body())
        if not user.is_valid():
            return self.validation_error(user.validation_errors)
        if self.user_repository.email_exists(user.email):
            return self.error('User with same email already exists')
        try:
            self.user_repository.insert(user)
        except Exception as ex:
            return self.error('An error has ocurred while creating user')
        # Enviamos mail de verificacion
        """
        try:
            user.send_verification_email()
        except Exception as ex:
            print(
                F'Ha ocurrido un error al enviar el mail de verificacion para el usuario {user.username}: {ex}')
        """
        return self.ok_success()

    @http_method(http_methods.GET, auth_required=True)
    def get_logged_user_data(self) -> dict:
        user_id = self.get_authenticated_user_id()
        user = self.user_repository.get_by_id(user_id, get_avatar=True)
        if not user:
            return self.error('Invalid user')
        return self.ok_success(user.to_dict())
