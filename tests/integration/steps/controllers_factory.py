from src.controllers.users_controller import UsersController


def get_user_controller() -> UsersController:
    controller = UsersController()
    controller._BaseController__jsonify_response = lambda x, y: {
        'body': x, 'code': y}
    return controller
