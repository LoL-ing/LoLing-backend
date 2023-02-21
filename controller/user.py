import json
from pathlib import Path
from typing import Any, Dict, List

from controller.champions import get_all_champions
from db_connection import rds
from db_connection.rds import (
    close_rds_db_connection,
    get_rds_db_connection,
    exec_query,
    exec_insert_query,
)
from dotenv.main import load_dotenv
import os
import bcrypt
import jwt
from schemas.user.request import UserRegisterArgument
from starlette.responses import JSONResponse
from schemas import ApiResponseCode
from mysql.connector.errors import Error as mysqlError
from exception import LOLINGDBRequestFailException
from starlette.status import *
from query import user as query
from controller import profiles as profile

from pydantic import EmailStr, BaseModel
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig


load_dotenv()
secret_key = os.environ.get("SECRET_KEY")
algorithm = os.environ.get("ALGORITHM")


def get_user_info(user_id):
    """
    유저 정보 조회
    """
    rds_conn = get_rds_db_connection()
    user_data = {"user_id": user_id}

    user_response = exec_query(
        rds_conn, query.SELECT_USER, True, input_params=user_data
    )

    return user_response


async def sign_in(email: str, password: str):
    """ "
    로그인 - 토큰 반환
    """
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
                {"email": email, "lol_name": lol_names[0].get("lol_name", "")},
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
    """
    회원가입
    """

    # 비밀번호 확인
    if argument.password != argument.password_confirm:
        return HTTP_400_BAD_REQUEST, {
            "code": ApiResponseCode.INVALID_PARAMETER,
            "message": "비밀번호와 비밀번호 확인 값이 일치하지 않습니다.",
        }

    try:
        rds_conn = get_rds_db_connection()
        user_data = {
            "email": argument.email,
            "password": argument.password,
        }

        print("############### user_info 생성 ###############")
        exec_insert_query(rds_conn, query.INSERT_USER_REGISER, input_params=user_data)

    except mysqlError as mysql_error:
        rds_conn.rollback()
        raise LOLINGDBRequestFailException(mysql_error)

    except Exception:
        rds_conn.rollback()
        raise

    finally:
        close_rds_db_connection(rds_conn)

    return HTTP_200_OK, {"code": ApiResponseCode.OK, "message": "회원가입 완료"}


# 미지의 길...이메일 본인인증......
def email_auth(email):
    """
    email 중복 확인
    """
    is_exist = get_user_info(email)
    if is_exist:
        return HTTP_409_CONFLICT, {
            "code": ApiResponseCode.DUPLICATE,
            "message": "동일한 이메일로 가입한 회원이 존재합니다.",
        }

    return HTTP_200_OK, {"code": ApiResponseCode.OK, "message": "이메일 중복 확인 완료"}
    # 없는 회원이면 인증 이메일 발송
    # else:

    # 디비에 비번 넣을떄 : hash_pw = bcrypt.hashpw(reg_info.pw.encode("utf-8"), bcrypt.gensalt())
    # 인증 처리
    return True


# 컨트롤러 만든 사람들이 주석추가 할것 ~~~~
def get_friends(lol_name: str):

    rds_conn = get_rds_db_connection()
    where_arg = {"lol_name": lol_name}
    friend_lol_names = exec_query(
        rds_conn, query.GET_FRIENDS_LOL_NAME, input_params=where_arg
    )

    return friend_lol_names


def get_friend_profiles(lol_name: str):

    rds_conn = get_rds_db_connection()
    friends = get_friends(lol_name)
    friend_profiles = []
    for friend in friends:
        friend_profiles.append(profile.get_profile(friend.get("friend_lol_name", "")))

    # 파이썬에서의 포문은 each를 가져옴, index 1,2등을 당연히 가져오는것이 아님.

    # where_arg = {"friend_lol_name" : friends}
    # friend_lol_name 이 키값중 하나인것임
    # friend_profiles= exec_query(rds_conn, query.GET_FRIEND_PROFILES, input_params= where_arg)

    return friend_profiles


def get_friend_profiles_new(lol_name: str):
    rds_conn = get_rds_db_connection()
    CHAMPION_IMG_BASE_URL = "https://opgg-static.akamaized.net/meta/images/lol/1205/champion/{0}.png?image=q_auto,f_webp,w_164&v=1646382437273"
    friends = get_friends(lol_name)

    select_query = (
        query.GET_FRIEND_PROFILES
        + query.GET_FRIEND_PROFILES_WHERE
        + str(
            tuple(list(map(lambda data: data.get("friend_lol_name"), friends)))
        ).replace(",)", ")")
        + ";"
    )

    friend_profiles = exec_query(rds_conn, select_query)
    friend_profiles = list(
        map(
            lambda data: {
                **data,
                "champ_info": json.loads(data.get("champ_info"))
                if data.get("champ_info") not in ["", None]
                else [{} for _ in range(3)],
                "line_info": json.loads(data.get("line_info"))
                if data.get("line_info") not in ["", None]
                else [{} for _ in range(3)],
                "champ_info_sr": json.loads(data.get("champ_info_sr"))
                if data.get("champ_info_sr") not in ["", None]
                else [{} for _ in range(3)],
                "line_info_sr": json.loads(data.get("line_info_sr"))
                if data.get("line_info_sr") not in ["", None]
                else [{} for _ in range(3)],
            },
            friend_profiles,
        )
    )

    sample_data = list(
        map(
            lambda data: {
                "nickname": data.get("lol_name"),
                "profileImg": CHAMPION_IMG_BASE_URL.format(
                    data.get("champ_info", [])[0].get("CHAMP_NAME")
                ),
                "line": data.get("line_info", [])[0].get("LINE_NAME"),
                "mannerTierImg": "../assets/images/diamond.png",
                "championImg": CHAMPION_IMG_BASE_URL.format(
                    data.get("champ_info", [])[0].get("CHAMP_NAME")
                ),
                "winRate": str(
                    round(
                        data.get("total_win_rate")
                        if data.get("total_win_rate") != None
                        else 0,
                        2,
                    ),
                )[-2:]
                + "%",
                "winLose": str(
                    round(
                        data.get("total_win_rate")
                        if data.get("total_win_rate") != None
                        else 0,
                        2,
                    ),
                )[-2:]
                + "%",
                "lineImg_1": data.get("line_info", [])[0].get("LINE_NAME"),
                "lineImg_2": data.get("line_info", [])[1].get("LINE_NAME"),
                "line_winRate_1": "{0:.0f}%".format(
                    round(data.get("line_info", [])[0].get("LINE_WIN_RATE", 0), 2) * 100
                ),
                "line_winRate_2": "{0:.0f}%".format(
                    round(data.get("line_info", [])[1].get("LINE_WIN_RATE", 0), 2) * 100
                ),
                "line_kda_1": str(
                    round((data.get("line_info"))[0].get("LINE_KDA", 0), 2)
                ),
                "line_kda_2": str(
                    round((data.get("line_info"))[1].get("LINE_KDA", 0), 2)
                ),
                "championImg_1": CHAMPION_IMG_BASE_URL.format(
                    data.get("champ_info", [])[0].get("CHAMP_NAME")
                ),
                "championImg_2": CHAMPION_IMG_BASE_URL.format(
                    data.get("champ_info", [])[1].get("CHAMP_NAME")
                ),
                "championImg_3": CHAMPION_IMG_BASE_URL.format(
                    data.get("champ_info", [])[2].get("CHAMP_NAME")
                ),
                "champ_winRate_1": "{0:.0f}%".format(
                    round(data.get("champ_info", [])[0].get("CHAMP_WIN_RATE", 0), 2)
                    * 100
                ),
                "champ_winRate_2": "{0:.0f}%".format(
                    round(data.get("champ_info", [])[1].get("CHAMP_WIN_RATE", 0), 2)
                    * 100
                ),
                "champ_winRate_3": "{0:.0f}%".format(
                    round(data.get("champ_info", [])[2].get("CHAMP_WIN_RATE", 0), 2)
                    * 100
                ),
                "champ_kda_1": str(
                    round((data.get("champ_info"))[0].get("CHAMP_KDA", 0), 2)
                ),
                "champ_kda_2": str(
                    round((data.get("champ_info"))[1].get("CHAMP_KDA", 0), 2)
                ),
                "champ_kda_3": str(
                    round((data.get("champ_info"))[2].get("CHAMP_KDA", 0), 2)
                ),
            },
            friend_profiles,
        )
    )

    return sample_data


class EmailSchema(BaseModel):
    email: List[EmailStr]
    body: Dict[str, Any]


async def post_email_verification(email: EmailSchema) -> JSONResponse:
    conf = ConnectionConfig(
        MAIL_USERNAME=os.environ.get("MAIL_USERNAME"),
        MAIL_PASSWORD=os.environ.get("MAIL_PASSWORD"),
        MAIL_FROM=os.environ.get("MAIL_FROM"),
        MAIL_PORT=587,
        MAIL_SERVER="smtp.naver.com",
        MAIL_FROM_NAME=os.environ.get("MAIL_FROM_NAME"),
        MAIL_TLS=True,
        MAIL_SSL=False,
        USE_CREDENTIALS=True,
        VALIDATE_CERTS=True,
        TEMPLATE_FOLDER=Path(__file__).parent.parent / "templates",
    )

    message = MessageSchema(
        subject="LoLing Verification Mail",
        recipients=email.dict().get("email"),
        template_body=email.dict().get("body"),
    )

    fm = FastMail(conf)
    await fm.send_message(message, template_name="email_verification_template.html")
    return JSONResponse(status_code=200, content={"message": "email has been sent"})
