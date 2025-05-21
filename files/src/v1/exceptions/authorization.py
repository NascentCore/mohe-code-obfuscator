from http import HTTPStatus

from . import ErrorRegistry


@ErrorRegistry.register(
    code="AuthorizationNotProvided",
    http_status=HTTPStatus.UNAUTHORIZED,
    description="Authorization header not provided or empty",
    is_technical=False,
    # i18n_key="user.not_found"
)
class AuthorizationNotProvided(Exception):
    pass


@ErrorRegistry.register(
    code="AuthorizationInvalid",
    http_status=HTTPStatus.UNAUTHORIZED,
    description="Authorization header invalid",
    is_technical=False,
    # i18n_key="user.not_found"
)
class AuthorizationInvalid(Exception):
    pass


@ErrorRegistry.register(
    code="Forbidden",
    http_status=HTTPStatus.FORBIDDEN,
    description="Forbidden",
    is_technical=False,
    # i18n_key="user.not_found"
)
class Forbidden(Exception):
    pass
