from dataclasses import dataclass
from http import HTTPStatus
from typing import Type


@dataclass
class ErrorMeta:
    http_status: HTTPStatus
    code: str
    description: str
    error_class: Type[Exception]
    is_technical: bool
    # i18n_key: str = "error.generic"
    # retryable: bool = False


class ErrorRegistry:
    _error_map: dict[int, ErrorMeta] = {}
    _class_map: dict[Type[Exception], ErrorMeta] = {}

    @classmethod
    def register(
        cls,
        code: str,
        http_status: int,
        description: str,
        is_technical: bool,
        **kwargs,
    ):
        def decorator(error_cls: Type[Exception]):
            if code in cls._error_map:
                raise ValueError(f"Error code {code} is already registered.")

            meta = ErrorMeta(
                http_status=http_status,
                code=code,
                description=description,
                error_class=error_cls,
                is_technical=is_technical,
                **kwargs,
            )
            cls._error_map[code] = meta
            cls._class_map[error_cls] = meta

            return error_cls

        return decorator

    @classmethod
    def get_meta_by_code(cls, code: int) -> ErrorMeta:
        if meta := cls._error_map.get(code):
            return meta
        raise KeyError(f"Unknown error code: {code}")

    @classmethod
    def get_meta_by_class(cls, error: Exception) -> ErrorMeta:
        if meta := cls._class_map.get(type(error)):
            return meta
        raise KeyError(f"Unknown error class: {type(error)}")

