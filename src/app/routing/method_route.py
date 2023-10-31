from src.app.utils.auth.permission_level import PermissionLevel


class MethodRoute:

    def __init__(self, controller_class: type, method_name: str, http_type: str, alias: str,
                 min_permission_level: PermissionLevel) -> None:
        self.controller_class = controller_class
        self.method_name = method_name
        self.http_type = http_type
        self.alias = alias
        self.min_permission_level = min_permission_level

    def get_path(self) -> str:
        return self.alias if self.alias is not None else F'/{self.method_name}'
