from db_connection.rds import get_rds_db_connection, exec_query, exec_insert_query
from dotenv.main import load_dotenv
import os
import bcrypt
import jwt
from model.user import userArgument
from starlette.responses import JSONResponse

load_dotenv()
secret_key = os.environ.get("SECRET_KEY")
algorithm = os.environ.get("ALGORITHM")


def get_user_info(user_id):
    rds_conn = get_rds_db_connection()
    user_data = {
        "user_id": user_id
    }
    select_query = """
    SELECT *
      FROM USER
     WHERE signin_id = %(user_id)s
    ;
    """
    user_response = exec_query(
        rds_conn, select_query, True, input_params=user_data)

    return user_response

# def insert_user_info(email, password):
#     rd


async def sign_in(email, password):
    is_exist = get_user_info(email)
    if is_exist:
        is_verified = bcrypt.checkpw(
            password.encode('utf-8'), bcrypt.hashpw(is_exist[0]['password'].encode("utf-8"), bcrypt.gensalt()))
        # 회원가입시 비밀번호를 암호화해서 넣는걸로 만든 후에 바꾸기 
        # if not user_info.email or not user_info.pw:
        #     return JSONResponse(status_code=400, content=dict(msg="Email and PW must be provided'"))
        # if not is_exist:
        #     return JSONResponse(status_code=400, content=dict(msg="NO_MATCH_USER"))
        # user = Users.get(email=user_info.email)
        # is_verified = bcrypt.checkpw(user_info.pw.encode("utf-8"), user.pw.encode('utf-8'))    
        
        if is_verified:
            token = jwt.encode({"email": email}, secret_key, algorithm)
            return token
            # return {"access_token": token, "token_type": "bearer"}

        #아이디는 있는데 비밀번호가 틀림
        else:
            return JSONResponse(status_code=400, content=dict(msg="패스워드가 일치하지 않습니다."))
    else:
        #아이디(이메일)가 없음, 회원정보 없음
        return JSONResponse(status_code=400, content=dict(msg="등록된 회원이 아닙니다."))

def register(argument:userArgument):
    rds_conn = get_rds_db_connection()
    user_data = {
        "email": argument.get("email"),
        "password" : argument.get("password")
    }
    insert_query = """
    INSERT INTO LoLing.USER(
        signin_id,
        password,
        manner_tier,
        like_cnt,
        hate_cnt,
        created_at,
        updated_at
    ) VALUES(
        %(email)s,
        %(password)s,
        '골드',
        0,
        0,
        now(),
        null
    )
    """
    print("############### user_info 생성 ###############")
    return exec_insert_query(rds_conn, insert_query, input_params=user_data)

# 미지의 길...이메일 본인인증......
def email_auth(email):
    #이미 존재하는 회원인지 확인
    is_exist = get_user_info(email)
    if is_exist:
        return JSONResponse(status_code=400, content=dict(msg="동일한 이메일로 가입한 회원이 존재합니다."))
    #없는 회원이면 인증 이메일 발송
    # else:
        
        # 디비에 비번 넣을떄 : hash_pw = bcrypt.hashpw(reg_info.pw.encode("utf-8"), bcrypt.gensalt())
    #인증 처리
    return True