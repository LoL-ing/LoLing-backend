from mysql.connector.errors import Error as mysqlError
from model import ApiResponseCode

# LOLING DB 요청 실패
class LOLINGDBRequestFailException(Exception):
    def __init__(self, error_object):
        self.error_object = error_object

        # DB 오류시 기본 응답 코드
        self.response_code = ApiResponseCode.DB_ERROR
        self.response_message = "LOLING DB 요청에 실패했습니다."

        # DB에서 일어난 에러인지 체크
        if isinstance(error_object, mysqlError):
            # duplicate key
            if error_object.errno == 1062:
                self.response_code = ApiResponseCode.DUPLICATE
                self.response_message = "중복된 항목이 있습니다."

            # debug for development: TODO -> logger로 변경
            print(error_object)


class LOLINGRiotAPIFailException(Exception):
    def __init__(self, error_object):
        self.error_object = error_object

        # DB 오류시 기본 응답 코드
        self.response_code = ApiResponseCode.DB_ERROR
        self.response_message = "LOLING DB 요청에 실패했습니다."

        # DB에서 일어난 에러인지 체크
        if isinstance(error_object, mysqlError):
            # duplicate key
            if error_object.errno == 1062:
                self.response_code = ApiResponseCode.DUPLICATE
                self.response_message = "중복된 항목이 있습니다."

            # debug for development: TODO -> logger로 변경
            print(error_object)
