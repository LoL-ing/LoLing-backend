from fastapi import FastAPI, Request
from controller import get_friends, get_all_champions, get_all_profiles, get_lol_account
from controller.kakaouser import *
from controller.user import *
from dotenv.main import load_dotenv
from os import environ

from db_connection.rds import get_rds_db_connection
# from db_connection.rds.insert_dummy import insert_friends, delete_friends
app = FastAPI()
load_dotenv()


@app.get("/")
async def root(request: Request):
    url_list = [
        {'path': route.path, 'name': route.name}
        for route in request.app.routes
    ]
    return url_list


@app.get("/friends")
def route_get_friends():
    return get_friends()


@app.get("/lol_account")
def route_get_lol_account():

    return get_lol_account()


@app.get("/profiles")
def route_get_profiles():
    return get_all_profiles()


@app.get("/champions")
def route_get_champions():
    return get_all_champions()


@app.get("/get_user_info")
def route_get_user_info(user_id: str):
    return get_user_info(user_id=user_id)


@app.get("/register")
def route_register():
    return register()


@app.get("/sign_in")
async def route_sign_in(user_id: str, password: str):
    return await sign_in(user_id=user_id, password=password)


@app.get("/kakao_auth")
def route_get_kakao_auth():
    return get_kakao_auth()


@app.get("/callback")
# 사람들의 말을 들어야하는 이유가 있으며 사람듣ㄹ의 말을 들어야하는 이유가 잇다.
def route_get_token(request: Request):
    code = request.query_params['code']
    return get_kakao_token(code)

# @app.get("/login")
# def route_login():
#     return
