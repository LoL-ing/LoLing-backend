from typing import Optional
from fastapi import APIRouter, Depends, Path
from fastapi.responses import JSONResponse

from controller.riot import *

router = APIRouter()


@router.post(
    "/init",
    summary="lol_account 정보 update",
    description="자랭 솔랭 구분하여 win, loss, tier, match_id DB insert",
)
def route_post_lol_info(signin_id: str, lol_name: str):
    return post_lol_info(signin_id, lol_name)


@router.post(
    "/ods",
    summary="match_id 들로 실제 match 정보 DB insert",
    description="MATCHES.USERS_MATCH_MAP 에서 아직 매치 정보 수집하지 않은 match_id 들만 불러와서, match 정보 DB(MATCHES.MATCHES_ODS) insert",
)
def route_get_match_info(lol_name: str):
    return get_match_info_ods(lol_name=lol_name)


@router.put(
    "/history/by-user",
    summary="ODS -> 한 매치의 유저별 정보를 추출 / 추출한 data 바탕으로 축약 데이터 통계",
    description="MATCHES.USERS_MATCH_MAP -> (fact query) MATCHES.USERS_MATCH_HISTORY -> (mart query) USERS.LOL_ACCOUNT",
)
def route_put_history_by_user(lol_name: str):
    return put_history_by_user(lol_name=lol_name)


# TODO 전체 유저 전적 갱신 만들기
@router.post("/history/all")
def route_put_history_all():
    pass


@router.post(
    "/login",
    summary="실제 lol id, pwd 로 인증",
    description="OS별 chormedriver 와 selenium 으로 라이엇 로그인 YN",
)
def route_get_selenium_login(id: str, pwd: str):
    return get_login(id=id, pwd=pwd)


# @router.get("/user_id")
# def route_get_user_id(lol_name: str):
#     return get_user_id(lol_name=lol_name)


# @router.get("/user_info")
# def route_get_user_info(id: str):
#     return get_user_info(id=id)


# @router.get("/recent_games")
# def route_get_recent_games(puuid: str, queue_type: str):
#     #  queue_type 솔랭 = 420 / 자랭 = 440
#     return get_recent_games(puuid=puuid, queue_type=queue_type)


# @router.get("/match_info/by-puuid")
# def route_get_match_info(match_id: str, puuid: str):
#     return get_match_info_by_user(match_id=match_id, puuid=puuid)


# @router.get("/match-info")
# def route_get_match_info(match_id: str):
#     return get_match_info(match_id=match_id)
