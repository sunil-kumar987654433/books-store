


from typing import Any, Callable

from fastapi import Request, responses


class BooklyException(Exception):
    """
        This is the default base class of all bookly exception.
    """
    pass


class InvalidTokenException(BooklyException):
    """
        uer has provide an invalid or expired token.
    """
    pass

class RevokedToken(BooklyException):
    """
        uer has provide token is expired or blocklisted.
    """
    pass


class AccessTokenRequired(BooklyException):
    """
        uer has provide wrong token, Please provide access token.
    """
    pass

class RefreshTokenRequired(BooklyException):
    """
        uer has provide wrong token, Please provide Refresh token.
    """
    pass


class UserAlreadyExist(BooklyException):
    """
        this user aleady exist for given email.
    """
    pass


class InsufficientPermission(BooklyException):
    """
        user does't have the nacessary permission to perform this action.
    """
    pass

class BookNotFound(BooklyException):
    """
        Book not found.
    """
    pass


class TagNotFound(BooklyException):
    """
        Book not found.
    """
    pass

class NotFound(BooklyException):
    """
        Not found.
    """
    pass






def create_exeption_handlers(status_code: int, initial_detail: Any)->Callable[[Request, Exception], responses.JSONResponse]:
    async def exception_handlers(request: Request, exc: BooklyException):
        return responses.JSONResponse(
            content=initial_detail,
            status_code=status_code
        )
    return exception_handlers