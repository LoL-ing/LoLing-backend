from ipaddress import summarize_address_range
from typing import List
from fastapi import APIRouter, Body, Depends, HTTPException, Path, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import jwt
from app.users.crud import user as user_crud
from app.database import get_db
from app.common.config import settings
from app.users.schema import IUserRead

router = APIRouter()


@router.post("/login")
def post_login(
    signin_id: str = Body(), password: str = Body(), db_session=Depends(get_db)
):
    """
    유저가 존재하는지 확인
        존재하지 않으면 404
        아이디, 비번이 틀렸다. 403

    token 을 생성
        user_id 정보를 담아서 보내주자

    token 을 return 해주자

    지금은 'accessToken' 만 반환하는데

    통상적으로는 'accessToken' + 'refreshToken'
    """
    user = user_crud.get(signin_id=signin_id, db_session=db_session)

    if user == None:
        raise HTTPException(404, detail="유저가 없네용")

    if user.hashed_password != password:
        raise HTTPException(403, detail="비밀번호가 틀리네.. 이런")

    # 아이디, 비밀번호가 맞는 유저 -> 로그인 로직을 실행
    # *토큰 생성
    token = jwt.encode(
        {
            "user_id": str(user.signin_id),
        },
        settings.SECRET_KEY,
        settings.ALGORITHM,
    )

    return token
