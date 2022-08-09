from fastapi import APIRouter, Depends, Path
from fastapi.responses import JSONResponse

from controller.riot import *

router = APIRouter()


@router.get("/user_id")
def route_get_user_id(summoner_name: str):
    return get_user_id(summoner_name=summoner_name)

@router.get("/user_info")
def route_get_user_info(id: str):
    return get_user_info(id=id)

@router.get("/recent_games")
def route_get_recent_games(puuid: str, queue_type: str):
   #  queue_type 솔랭 = 420 / 자랭 = 440
    return get_recent_games(puuid = puuid, queue_type=queue_type)