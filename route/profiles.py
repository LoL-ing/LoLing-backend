from auth.jwt import auth_required
from fastapi import APIRouter, Depends, Path, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from controller.profiles import *

router = APIRouter()


@router.get("/lol_account")
def route_get_lol_account(user_id: str):

    return get_lol_account(user_id=user_id)

@router.get("/profiles")
def route_get_profiles(lol_name: str):
    return get_all_profiles(lol_name=lol_name)


@router.get("")
def route_get_profile(user_info: dict = Depends(auth_required)):
    lol_name = user_info.get("lol_name")
    return get_profile(lol_name=lol_name)
