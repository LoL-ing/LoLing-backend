from db_connection.rds import get_rds_db_connection, exec_query, exec_insert_query
from dotenv.main import load_dotenv
import os
import bcrypt
import jwt
from model.user.request import UserRegisterArgument
from starlette.responses import JSONResponse
from query import user as query

load_dotenv()
secret_key = os.environ.get("SECRET_KEY")
algorithm = os.environ.get("ALGORITHM")


def get_user_info(user_id):
    rds_conn = get_rds_db_connection()
    user_data = {"user_id": user_id}

    user_response = exec_query(
        rds_conn, query.SELECT_USER, True, input_params=user_data
    )

    return user_response


# def insert_user_info(email, password):
#     rd


async def sign_in(email: str, password: str):
    is_exist = get_user_info(email)
    if is_exist:
        is_verified = bcrypt.checkpw(
            password.encode("utf-8"),
            bcrypt.hashpw(is_exist[0]["password"].encode("utf-8"), bcrypt.gensalt()),
        )
        # 회원가입시 비밀번호를 암호화해서 넣는걸로 만든 후에 바꾸기
        # if not user_info.email or not user_info.pw:
        #     return JSONResponse(status_code=400, content=dict(msg="Email and PW must be provided'"))
        # if not is_exist:
        #     return JSONResponse(status_code=400, content=dict(msg="NO_MATCH_USER"))
        # user = Users.get(email=user_info.email)
        # is_verified = bcrypt.checkpw(user_info.pw.encode("utf-8"), user.pw.encode('utf-8'))

        if is_verified:
            conn = get_rds_db_connection()

            lol_names = exec_query(
                conn, query.GET_USER_LOL_ACCOUNT, input_params={"email": email}
            )

            if not lol_names and len(lol_names) <= 0:
                return JSONResponse(
                    status_code=400, content=dict(msg="아이디에 해당하는 롤 계정이 존재하지 않습니다.")
                )

            token = jwt.encode(
                {"email": email, "lol_name": lol_names[0].get("LOL_NAME", "")},
                secret_key,
                algorithm,
            )

            return token
            # return {"access_token": token, "token_type": "bearer"}

        # 아이디는 있는데 비밀번호가 틀림
        else:
            return JSONResponse(status_code=400, content=dict(msg="패스워드가 일치하지 않습니다."))

    else:
        # 아이디(이메일)가 없음, 회원정보 없음
        return JSONResponse(status_code=400, content=dict(msg="등록된 회원이 아닙니다."))


def register(argument: UserRegisterArgument):
    rds_conn = get_rds_db_connection()
    user_data = {"email": argument.get("email"), "password": argument.get("password")}

    print("############### user_info 생성 ###############")
    exec_insert_query(rds_conn, query.INSERT_USER_REGISER, input_params=user_data)

    return JSONResponse(status_code=200, content=dict(msg="회원가입 성공"))


# 미지의 길...이메일 본인인증......
def email_auth(email):
    # 이미 존재하는 회원인지 확인
    is_exist = get_user_info(email)
    if is_exist:
        return JSONResponse(
            status_code=400, content=dict(msg="동일한 이메일로 가입한 회원이 존재합니다.")
        )
    # 없는 회원이면 인증 이메일 발송
    # else:

    # 디비에 비번 넣을떄 : hash_pw = bcrypt.hashpw(reg_info.pw.encode("utf-8"), bcrypt.gensalt())
    # 인증 처리
    return True
