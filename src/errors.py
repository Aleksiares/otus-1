from starlette.status import HTTP_404_NOT_FOUND
from fastapi import HTTPException


class NotFoundHTTPException(HTTPException):
    status_code = HTTP_404_NOT_FOUND
    detail = "User not found"

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)
