from typing import Optional

from src.app.routing.router import Router


def _normalize_alias(alias: str) -> Optional[str]:
    if alias is not None and len(alias) > 0:
        return F'/{alias}' if alias[0] != '/' else alias
    return None


def route(method_type: str, alias: str = None, user_auth_required: bool = True, device_auth_required: bool = False):
    def wrapper(func):
        Router.register_http_method({
            'type': method_type,
            'alias': _normalize_alias(alias),
            'class_name': func.__qualname__.split('.')[0],
            'method_name': func.__name__,
            'user_auth_required': user_auth_required,
            'device_auth_required': device_auth_required
        })
        return func

    return wrapper
