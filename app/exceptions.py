from fastapi import HTTPException, status


class BadRequestException400(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class UnauthorizedException401(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)


class ForbiddenException403(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)


class NotFoundExpection404(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class ConflictException409(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)


class InternalServerError500(HTTPException):
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail
        )


class NotImplemented501(HTTPException):
    def __init__(self, detail: str):
        super().__init(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail=detail)


class BadGateway502(HTTPException):
    def __init__(self, detail: str):
        super().__init(status_code=status.HTTP_502_BAD_GATEWAY, detail=detail)


class ServiceUnavailable503(HTTPException):
    def __init__(self, detail: str):
        super().__init(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=detail)


class GatewayTimeout504(HTTPException):
    def __init__(self, detail: str):
        super().__init(status_code=status.HTTP_504_GATEWAY_TIMEOUT, detail=detail)
