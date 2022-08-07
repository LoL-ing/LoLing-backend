from fastapi import APIRouter, Depends, Path, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from model.user.request import UserRegisterArgument

from controller.user import *
from controller.kakaouser import *

router = APIRouter()


@router.get("/get_user_info")
def route_get_user_info(user_id: str):
    return get_user_info(user_id=user_id)


@router.get("/email_auth")
def route_email_auth(email: str):
    return email_auth(email=email)


@router.post("/register", summary="회원가입", description="회원가입 정보 post")
def route_register(argument: UserRegisterArgument):
    return register(jsonable_encoder(argument))


@router.get("/sign_in")
async def route_sign_in(email: str, password: str):
    return await sign_in(email=email, password=password)


# kakao 로그인 시도흔적
@router.get("/kakao_auth")
def route_get_kakao_auth():
    return get_kakao_auth()


@router.get("/callback")
def route_get_token(request: Request):
    code = request.query_params["code"]
    return get_kakao_token(code)
