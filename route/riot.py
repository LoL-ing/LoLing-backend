from typing import Optional
from fastapi import APIRouter, Depends, Path
from fastapi.responses import JSONResponse

from controller.riot import *

router = APIRouter()


@router.post("/lol_info")
def route_post_lol_info(signin_id: str, lol_name: str):
    return post_lol_info(signin_id, lol_name)


@router.post("/match-info/ods")
def route_get_match_info(lol_name: str):
    return get_match_info_ods(lol_name=lol_name)


@router.post("/match-info/fact-mart")
def route_put_fact(lol_name: str):
    return put_fact(lol_name=lol_name)


@router.post("/login")
def route_get_selenium_login(id: str, pwd: str):
    return get_login(id=id, pwd=pwd)


@router.get("/user_id")
def route_get_user_id(lol_name: str):
    return get_user_id(lol_name=lol_name)


@router.get("/user_info")
def route_get_user_info(id: str):
    return get_user_info(id=id)


@router.get("/recent_games")
def route_get_recent_games(puuid: str, queue_type: str):
    #  queue_type 솔랭 = 420 / 자랭 = 440
    return get_recent_games(puuid=puuid, queue_type=queue_type)


@router.get("/match_info/by-puuid")
def route_get_match_info(match_id: str, puuid: str):
    return get_match_info_by_user(match_id=match_id, puuid=puuid)


@router.get("/match-info")
def route_get_match_info(match_id: str):
    return get_match_info(match_id=match_id)
