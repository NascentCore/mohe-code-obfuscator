from http import HTTPStatus

from . import ErrorRegistry


@ErrorRegistry.register(
    code="UsersServiceNotAvailable",
    http_status=HTTPStatus.SERVICE_UNAVAILABLE,
    description="",
    is_technical=True,
    # i18n_key="user.not_found"
)
class UsersServiceNotAvailable(Exception):
    pass


@ErrorRegistry.register(
    code="BasesServiceNotAvailable",
    http_status=HTTPStatus.SERVICE_UNAVAILABLE,
    description="",
    is_technical=True,
    # i18n_key="user.not_found"
)
class BasesServiceNotAvailable(Exception):
    pass
