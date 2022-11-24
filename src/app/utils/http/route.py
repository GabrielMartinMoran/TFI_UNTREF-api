from typing import Optional, Callable

from src.app.routing.router import Router
from src.app.utils.auth.permission_level import PermissionLevel


def _normalize_alias(alias: str) -> Optional[str]:
    if alias is not None and len(alias) > 0:
        return F'/{alias}' if alias[0] != '/' else alias
    return None


def route(method_type: str, alias: str = None,
          min_permission_level: PermissionLevel = PermissionLevel.USER) -> Callable:
    def wrapper(func):
        Router.register_http_method({
            'type': method_type,
            'alias': _normalize_alias(alias),
            'class_name': func.__qualname__.split('.')[0],
            'method_name': func.__name__,
            'min_permission_level': min_permission_level
        })
        return func

    return wrapper
