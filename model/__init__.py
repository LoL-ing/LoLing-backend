# API Response code

from enum import Enum


class ApiResponseCode(str, Enum):
    OK = "OK"

    INVALID_PARAMETER = "INVALID_PARAMETER"  # 잘못된 body
    DATE_RANGE_EXCEEDED = "DATE_RANGE_EXCEEDED"

    BAD_REQUEST = "BAD_REQUEST"
    NO_PERMISSION = "NO_PERMISSION"
    NOT_FOUND = "NOT_FOUND"
    NO_AUTH_HEADER = "NO_AUTH_HEADER"
    EXPIRED = "EXPIRED"
    UNPAID = "UNPAID"

    # DB 관련 오류
    DUPLICATE = "DUPLICATE"  # duplicate key
    DB_ERROR = "DB_ERROR"  # 기타 db 오류
