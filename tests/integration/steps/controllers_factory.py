from src.controllers.auth_controller import AuthController


def get_auth_controller() -> AuthController:
    controller = AuthController()
    controller._BaseController__jsonify_response = lambda x, y: {
        'body': x, 'code': y}
    return controller
