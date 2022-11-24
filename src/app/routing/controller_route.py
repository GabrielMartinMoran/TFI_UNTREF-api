from typing import List
from src.app.routing.method_route import MethodRoute
from src.app.utils.auth.permission_level import PermissionLevel


class ControllerRoute:
    def __init__(self, controller_class: type) -> None:
        self.controller_class = controller_class
        self.methods: List[MethodRoute] = []

    def add_method(self, method_name: str, http_type: str, alias: str, min_permission_level: PermissionLevel) -> None:
        met_route = MethodRoute(self.controller_class, method_name, http_type, alias, min_permission_level)
        self.methods.append(met_route)

    def route(self) -> str:
        controller_name = self.controller_name()
        return controller_name.lower().replace('controller', '')

    def controller_name(self) -> str:
        return self.controller_class.__name__
