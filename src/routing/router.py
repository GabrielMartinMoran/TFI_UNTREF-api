from typing import List
import os
import sys
import pathlib
import importlib
from flask.json import jsonify
import pymongo
from flask import make_response
from src.utils import console_colors, global_variables, text_formatters
from src.utils.logger import Logger
from .controller_route import ControllerRoute
from .method_route import MethodRoute
from .token_parser import TokenParser
from .cors_solver import CORSSolver


CONTROLLERS_FOLDER = 'controllers'
CONTROLLERS_EXTENSION = '.py'
EXCLUDED_CONTROLLERS = ['base_controller', '__init__']

BASE_API_URL = 'api'
ERROR_TEMPLATE = 'error.html'


class Router:

    def __init__(self) -> None:
        self.routes: List[ControllerRoute] = []
        self.http_methods = []
        self.__register_instance()
        self.__map_routes()

    @staticmethod
    def get_base_url() -> str:
        return BASE_API_URL

    @staticmethod
    def error_response(message, code):
        return make_response({'message': message}, code)

    @staticmethod
    def register_http_method(http_method) -> None:
        if global_variables.ROUTER_INSTANCE:
            global_variables.ROUTER_INSTANCE.http_methods.append(http_method)

    def route(self, request, path):
        splitted_path = path.split('/') # Aunque sea un string vacio, el primer elemento siempre existe
        controller_name = splitted_path[0]
        method_name = F'/{splitted_path[1]}' if len(splitted_path) > 1 else '/'

        # CORS
        cors_solver = CORSSolver(request)
        if cors_solver.is_cors_request():
            wanted_method = self.__get_routed_method(controller_name, method_name, cors_solver.get_wanted_http_metod())
            if wanted_method is None:
                return self.error_response('Not found', 404)
            return cors_solver.get_cors_response()

        routed_method = self.__get_routed_method(controller_name, method_name, request.method)
        if routed_method is None:
            return self.error_response('Not found', 404)

        # Si requiere token
        token_parser = TokenParser(request)
        if routed_method.auth_required and not token_parser.valid_token():
            return self.error_response('Unauthorized', 401)

        params = []
        if len(splitted_path) > 2:
            params = splitted_path[2:]
        try:
            return self.__call_controller_method(routed_method, request, token_parser.get_token(), *params)
        except TypeError as ex:
            print(
                F'{console_colors.ERROR}An error has ocurred with message:'
                F' {ex}{console_colors.ENDC}')
            return self.error_response('Bad method arguments', 400)
        except Exception as ex:
            print(F'{console_colors.ERROR}{ex}{console_colors.ENDC}')
            return self.error_response('Internal server error', 500)

    def print_routemaps(self): # pragma: no cover
        print(console_colors.HEADER + console_colors.UNDERLINE + '\nMapa de controllers utilizados:' + console_colors.ENDC)
        for route in self.routes:
            print(F'  • {console_colors.WARNING}{route.controller_name()}{console_colors.ENDC} -> '
                  F'{console_colors.OK}/{self.get_base_url()}/{route.route()}{console_colors.ENDC}')
            for method in route.methods:
                print(F'\t‣ {console_colors.CYAN}{method.http_type} {console_colors.ENDC}'
                      F'- {console_colors.WARNING}{method.get_path()}{console_colors.ENDC}')
            print('\n')

    def __register_instance(self):
        global_variables.ROUTER_INSTANCE = self

    def __map_routes(self):
        Logger.get_logger(__file__).debug("Mapeo de rutas Start...")
        print(F'\n{console_colors.INFO}Comenzando el mapeo de rutas:{console_colors.ENDC}')
        # self.http_methods se llena al cargar los controlles ya que importa los modulos
        for contr in self.__discover_controllers():
            controller_route = ControllerRoute(contr)
            self.routes.append(controller_route)
            for meth in self.http_methods:
                if meth['class_name'] == controller_route.controller_name():
                    controller_route.add_method(meth['method_name'], meth['type'], meth['alias'], meth['auth_required'])
        Logger.get_logger(__file__).debug("Mapeo de rutas Done...")

    def __discover_controllers_modules(self):
        controllers_path = os.path.join(pathlib.Path(
            __file__).parent.parent.absolute(), CONTROLLERS_FOLDER)
        sys.path.append(controllers_path)
        mod_list = [fil[:-3]
                    for fil in os.listdir(controllers_path) if fil[-3:] == CONTROLLERS_EXTENSION]
        return [mod for mod in mod_list if mod not in EXCLUDED_CONTROLLERS]

    def __get_controller_class(self, module_name):
        try:
            controller_module = importlib.import_module(module_name)
        except ImportError as e:
            print(F' ⚠ {console_colors.WARNING}No se pudo importar el archivo'
                  F' {module_name}{CONTROLLERS_EXTENSION}. '
                  F'Ignorando mapeo del controlador{console_colors.ENDC}')
            Logger.get_logger(__file__).error(e)
            return None
        class_name = text_formatters.snake_to_camel(module_name)
        try:
            return getattr(controller_module, class_name)
        except AttributeError:
            print(F' ⚠ {console_colors.WARNING}No se hallo la clase del controllador {class_name}'
                  F' en el archivo {module_name}{CONTROLLERS_EXTENSION}.'
                  F'Ignorando mapeo del controlador {class_name}!{console_colors.ENDC}')
        return None

    def __discover_controllers(self):
        return list(filter(None.__ne__,map(self.__get_controller_class, self.__discover_controllers_modules())))

    def __get_routed_method(self, controller, method, http_type) -> bool:
        for cont_route in self.routes:
            if cont_route.route() == controller:
                for cont_method in cont_route.methods:
                    if cont_method.get_path() == method and cont_method.http_type == http_type:
                        return cont_method
        return None

    def __call_controller_method(self, method_route: MethodRoute, request, token, *method_params):
        controller_instance = method_route.controller_class()
        controller_instance.request = request
        controller_instance.token = token
        method = getattr(controller_instance, method_route.method_name)
        controller_instance.on_request()
        result = method(*method_params)
        controller_instance.response = result
        controller_instance.after_request()
        return result
