import os
import queue
import requests
from starlette.responses import JSONResponse
import logging
from urllib import parse
from const.urls import RIOT_API_URLS
from dotenv.main import load_dotenv
from datetime import datetime
import time

load_dotenv()
api_key = os.environ.get("RIOT_API_KEY")

season_start_date = str(
    time.mktime(
        datetime.strptime("2022-01-07 14:00:00", "%Y-%m-%d %H:%M:%S").timetuple()
    )
).split(".")[0]


def get_user_id(summoner_name: str):
    name = parse.quote(summoner_name)
    url = "/".join([RIOT_API_URLS["GET_USER_ID"], name])
    params = {"api_key": api_key}
    riot_user_response = requests.get(url, params=params).json()

    if riot_user_response.get("status", {}).get("status_code") == 404:
        return JSONResponse(status_code=404, content=dict(msg="잘못된 소환사 이름"))

    return riot_user_response


def get_user_info(id: str):
    url = "/".join([RIOT_API_URLS["GET_USER_INFO"], id])
    params = {"api_key": api_key}

    riot_user_info_response = requests.get(url, params=params).json()

    if (
        isinstance(riot_user_info_response, dict)
        and riot_user_info_response.get("status", {}).get("status_code") == 400
    ):
        return JSONResponse(status_code=400, content=dict(msg="잘못된 소환사 id"))

    if riot_user_info_response and len(riot_user_info_response) < 1:
        return JSONResponse(status_code=404, content=dict(msg="잘못된 소환사 id"))

    return riot_user_info_response[0]


def get_recent_games(puuid: str, queue_type: str):

    start = 0
    count = 100

    url = "/".join(
        [
            RIOT_API_URLS["GET_ASIA_RECENT_GAMES"],
            puuid,
            "ids",
        ]
    )

    params = {
        "startTime": season_start_date,
        "queue": queue_type,
        "type": "ranked",
        "start": str(start),
        "count": str(count),
        "api_key": api_key,
    }

    response = requests.get(url, params=params).json()

    result = []

    while response:
        result.extend(response)

        start += count

        params = {
            "startTime": season_start_date,
            "queue": queue_type,
            "type": "ranked",
            "start": str(start),
            "count": str(count),
            "api_key": api_key,
        }

        response = requests.get(url, params=params).json()

    return result


def get_match_info(matchid: str, puuid: str):
    url = RIOT_API_URLS["GET_MATCH_INFO"] + matchid + "?api_key=" + api_key
    response = requests.get(url).json()
    match_info = response["info"]["participants"]
    result = []

    for r in match_info:
        if r["puuid"] == puuid:
            individualPosition = r["individualPosition"]
            championName = r["championName"]
            kills = r["kills"]
            deaths = r["deaths"]
            assists = r["assists"]
            win = r["win"]
            result.append(
                [individualPosition, championName, kills, deaths, assists, win]
            )

    return result
