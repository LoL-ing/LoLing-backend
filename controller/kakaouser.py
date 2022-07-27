from urllib import response
from fastapi import FastAPI, Request
import requests
from starlette.responses import RedirectResponse
from db_connection.mongo import get_db_connection
from db_connection.rds import get_rds_db_connection, exec_query, exec_insert_query
import json

REST_API_KEY = 'fea04d110f5bcad28342dc2f41563a09'
REDIRECT_URI = 'http://54.153.85.38/callback'

# 인가 코드 받기


def get_kakao_auth():

    url = "https://kauth.kakao.com/oauth/authorize?response_type=code&client_id={0}&redirect_uri={1}".format(
        REST_API_KEY, REDIRECT_URI)
    return RedirectResponse(url)


# 토큰 받기
""" 불필요한 고통의 연속...
 괴로움의 구렁텅이..."""


def get_kakao_token(code):
    # 토큰 받기
    kauth_response = requests.post("https://kauth.kakao.com/oauth/token",
                                   data={
                                       "grant_type": "authorization_code",
                                       "client_id": REST_API_KEY,
                                       "redirect_uri": REDIRECT_URI,
                                       "code": code,
                                   }
                                   )
    print(kauth_response.json())
    access_token = kauth_response.json().get("access_token")

    # 유저 ID 가져오기
    headers = {
        "Authorization": "Bearer "+access_token,
        "Content-type": "application/x-www-form-urlencoded;charset=utf-8"
    }

    profile_request = requests.post(
        "https://kapi.kakao.com/v2/user/me", headers=headers)

    user_id = profile_request.json().get("id")
    user_id = str(user_id)
    print(user_id)

    user_response = get_user_info(user_id)

    if user_response:
        # 있으면 랜딩페이지로 이동
        return user_response
    else:
        rds_conn = get_rds_db_connection()
        user_data = {
            "kakao_id": user_id,
            "lol_name": "test"
        }
        insert_query = """
        INSERT INTO USER (lol_name, kakao_id)
        VALUES (%(lol_name)s, %(user_id)s)
        ;
        """
        user_response = exec_insert_query(
            rds_conn, insert_query, input_params=user_data)

        # 없으면 디비에 추가 + 회원가입 설정하는 곳으로 보내주기
        return user_response


def get_user_info(user_id):
    rds_conn = get_rds_db_connection()
    user_data = {
        "user_id": user_id
    }
    select_query = """
    SELECT *
      FROM USER
     WHERE kakao_id = %(user_id)s
    ;
    """
    user_response = exec_query(
        rds_conn, select_query, True, input_params=user_data)

    return user_response
