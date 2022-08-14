from ipaddress import summarize_address_range
from fastapi import APIRouter, Depends, Path, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from model.user.request import UserRegisterArgument

from controller.user import *
from controller.kakaouser import *

router = APIRouter()


@router.get("/get_user_info", summary="유저 등록 여부 조회")
def route_get_user_info(user_id: str):
    return get_user_info(user_id=user_id)


@router.get("/email_auth", summary="이메일 중복 확인")
def route_email_auth(email: str):
    status_code, result = email_auth(email)

    return JSONResponse(status_code=status_code, content=result)


@router.post("/register", summary="회원가입", description="회원가입 정보 post")
def route_register(argument: UserRegisterArgument):
    status_code, result = register(jsonable_encoder(argument))

    return JSONResponse(status_code=status_code, content=result)


@router.get("/sign_in")
async def route_sign_in(email: str, password: str):
    return await sign_in(email=email, password=password)


######## kakao 로그인 시도흔적 #########
@router.get("/kakao_auth")
def route_get_kakao_auth():
    return get_kakao_auth()


@router.get("/callback")
def route_get_token(request: Request):
    code = request.query_params["code"]
    return get_kakao_token(code)
