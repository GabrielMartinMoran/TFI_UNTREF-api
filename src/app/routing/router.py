from typing import List, Optional, Type, cast
import os
import pkgutil
from pydoc import locate
from flask import make_response

from src.app.controllers.base_controller import BaseController
from src.app.utils import global_variables, console_colors
from src.app.utils.auth.permission_level import PermissionLevel
from src.app.utils.logging.logger import Logger
from src.app.routing.controller_route import ControllerRoute
from src.app.routing.method_route import MethodRoute
from src.app.routing.token_parser import TokenParser
from src.app.routing.cors_solver import CORSSolver
from src.app.utils.http.response import Response

import src.app.controllers as controllers_module
from src.app.utils.auth.token import Token
from src.app.utils.http.request import Request

EXCLUDED_CONTROLLERS = ['base_controller']

BASE_API_URL = 'api'
ERROR_TEMPLATE = 'error.html'


class Router:

    def __init__(self) -> None:
        self.routes: List[ControllerRoute] = []
        self.http_methods = []
        self._register_instance()
        self._map_routes()

    @staticmethod
    def get_base_url() -> str:
        return BASE_API_URL

    @staticmethod
    def error_response(message, code):
        return make_response({
            'message': message
        }, code)

    @staticmethod
    def register_http_method(http_method) -> None:
        if global_variables.ROUTER_INSTANCE:
            global_variables.ROUTER_INSTANCE.http_methods.append(http_method)

    def route(self, request, path):
        split_path = path.split('/')  # Aunque sea un string vacio, el primer elemento siempre existe
        controller_name = split_path[0]
        method_name = F'/{split_path[1]}' if len(split_path) > 1 else '/'

        # CORS
        cors_solver = CORSSolver(request)
        if cors_solver.is_cors_request():
            wanted_method = self._get_routed_method(controller_name, method_name, cors_solver.get_wanted_http_metod())
            if wanted_method is None:
                return self.error_response('Not found', 404)
            return cors_solver.get_cors_response()

        routed_method = self._get_routed_method(controller_name, method_name, request.method)
        if routed_method is None:
            return self.error_response('Not found', 404)

        # If a token is required
        token_parser = TokenParser(request)
        if not self._has_permission(routed_method.min_permission_level, token_parser.token):
            return self.error_response('Unauthorized', 401)

        params = []
        if len(split_path) > 2:
            params = split_path[2:]
        try:
            return self._call_controller_method(routed_method, request, token_parser.token, *params)
        except TypeError as ex:
            print(
                F'{console_colors.ERROR}An error has ocurred with message:'
                F' {ex}{console_colors.ENDC}')
            return self.error_response('Bad method arguments', 400)
        except Exception as ex:
            print(F'{console_colors.ERROR}{ex}{console_colors.ENDC}')
            return self.error_response('Internal server error', 500)

    def print_routemap(self):  # pragma: no cover
        print(
            console_colors.HEADER + console_colors.UNDERLINE + '\nMapa de controllers utilizados:' +
            console_colors.ENDC
        )
        for route in self.routes:
            print(F'  • {console_colors.WARNING}{route.controller_name()}{console_colors.ENDC} -> '
                  F'{console_colors.OK}/{self.get_base_url()}/{route.route()}{console_colors.ENDC}')
            for method in route.methods:
                print(F'\t‣ {console_colors.CYAN}{method.http_type} {console_colors.ENDC}'
                      F'- {console_colors.WARNING}{method.get_path()}{console_colors.ENDC}')
            print('\n')

    def _register_instance(self):
        global_variables.ROUTER_INSTANCE = self

    def _map_routes(self):
        Logger.debug("Mapeo de rutas iniciado...")
        print(F'\n{console_colors.INFO}Comenzando el mapeo de rutas:{console_colors.ENDC}')
        # self.http_methods se llena al cargar los controlles ya que importa los modulos
        for controller in self._discover_controllers():
            controller_route = ControllerRoute(controller)
            self.routes.append(controller_route)
            for method in self.http_methods:
                if method['class_name'] == controller_route.controller_name():
                    controller_route.add_method(method['method_name'], method['type'], method['alias'],
                                                method['min_permission_level'])
        Logger.debug("Mapeo de rutas finalizado...")

    @classmethod
    def _discover_controllers_modules(cls):
        controllers_path = os.path.dirname(controllers_module.__file__)
        controllers_modules = [name for _, name, _ in pkgutil.iter_modules([controllers_path])]
        return [mod for mod in controllers_modules if mod not in EXCLUDED_CONTROLLERS]

    @classmethod
    def _get_controller_class(cls, module_name: str) -> Optional[Type[BaseController]]:
        controllers_rel_path = os.path.relpath(controllers_module.__file__).split('/')[:-1]
        class_name = module_name.title().replace('_', '')
        class_path = '.'.join(controllers_rel_path + [module_name, class_name])
        try:
            controller_class = cast(Type[BaseController], locate(class_path))
        except Exception as e:
            Logger.error(e)
            print(F' ⚠ {console_colors.WARNING}No se pudo importar el archivo {module_name}. '
                  F'Ignorando mapeo del controlador{console_colors.ENDC}')
            Logger.error(e)
            return None
        if not controller_class:
            print(F' ⚠ {console_colors.WARNING}No se hallo la clase del controllador {class_name}'
                  F' en el archivo {module_name}.'
                  F' Ignorando mapeo del controlador {class_name}!{console_colors.ENDC}')
            return None
        return controller_class

    def _discover_controllers(self) -> List[Type[BaseController]]:
        return [self._get_controller_class(controller_module) for controller_module in
                self._discover_controllers_modules() if controllers_module]

    def _get_routed_method(self, controller_name: str, method: str, http_method: str) -> Optional[MethodRoute]:
        for cont_route in self.routes:
            if cont_route.route() == controller_name:
                for cont_method in cont_route.methods:
                    if cont_method.get_path() == method and cont_method.http_type == http_method:
                        return cont_method
        return None

    @classmethod
    def _call_controller_method(cls, method_route: MethodRoute, request, token: Token, *method_params):
        internal_request = Request(request.method, request.path, request.json if len(request.data) > 0 else {},
                                   dict(request.args))
        controller_instance = method_route.controller_class(**{
            'request': internal_request,
            'token': token
        })
        method = getattr(controller_instance, method_route.method_name)
        result: Response = method(*method_params)
        return result.jsonify()

    @classmethod
    def _has_permission(cls, min_permission_level: PermissionLevel, token: Optional[Token]) -> bool:
        if token is None:
            return min_permission_level == PermissionLevel.PUBLIC
        return token.permission_level.value >= min_permission_level.value
