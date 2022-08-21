import json
import os

import requests
from starlette.responses import JSONResponse
from starlette.status import *

import platform
from urllib import parse

from const.urls import RIOT_API_URLS
from dotenv.main import load_dotenv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

from datetime import datetime
import time

from db_connection.rds import (
    exec_insert_query,
    exec_multiple_queries,
    exec_query,
    get_rds_db_connection,
)
from query.riot import (
    DELETE_LOL_ACCOUNT,
    INSERT_LOL_ACCOUNT,
    INSERT_MATCH_INFO_ODS,
    INSERT_USER_LOL_ACCOUNT_MAP,
    DELETE_USER_LOL_ACCOUNT_MAP,
    DELETE_USERS_MATCH_MAP,
    INSERT_USERS_MATCH_MAP,
    SELECT_MATCH_ID_INFO_N,
    UPDATE_USERS_MATCH_ODS_YN,
    UPDATE_USERS_MATCH_ODS_YN_WHERE,
)

load_dotenv()
api_key = os.environ.get("RIOT_API_KEY")

season_start_date = str(
    time.mktime(
        datetime.strptime("2022-01-07 14:00:00", "%Y-%m-%d %H:%M:%S").timetuple()
    )
).split(".")[0]

global_rds_conn = get_rds_db_connection


def post_lol_info(signin_id: str, lol_name: str):
    global global_rds_conn

    # user 정보 DB INSERT
    # user_info 넣을 때, lol_name 만 insert 해두고 나머지를 update 할 지.. update 로 할 지? lock 때문에
    user_id_info = get_user_id(lol_name)
    user_info = get_user_info(user_id_info.get("id"))
    exec_query(
        global_rds_conn,
        DELETE_LOL_ACCOUNT,
        select_flag=False,
        input_params={"lol_name": lol_name},
    )

    exec_insert_query(
        global_rds_conn,
        INSERT_LOL_ACCOUNT,
        input_params={
            "lol_name": lol_name,
            "user_id": user_id_info.get("id"),
            "puuid": user_id_info.get("puuid"),
            "wins": user_info.get("wins"),
            "losses": user_info.get("losses"),
            "tier": " ".join([user_info.get("tier"), user_info.get("rank")]),
        },
    )
    print(user_info)

    exec_query(
        global_rds_conn,
        DELETE_USER_LOL_ACCOUNT_MAP,
        select_flag=False,
        input_params={
            "signin_id": signin_id,
            "lol_name": lol_name,
        },
    )

    exec_insert_query(
        global_rds_conn,
        INSERT_USER_LOL_ACCOUNT_MAP,
        input_params={
            "signin_id": signin_id,
            "lol_name": lol_name,
        },
    )

    exec_query(
        global_rds_conn,
        DELETE_USERS_MATCH_MAP,
        select_flag=False,
        input_params={
            "lol_name": lol_name,
        },
    )

    for queue_type in ["420", "440"]:
        match_ids = get_recent_games(lol_name, queue_type=queue_type)

        exec_multiple_queries(
            global_rds_conn,
            INSERT_USERS_MATCH_MAP,
            input_params=[
                {
                    "lol_name": lol_name,
                    "match_type": queue_type,
                    "match_id": match_id,
                }
                for match_id in match_ids
            ],
        )
    return JSONResponse(status_code=200, content=dict(msg="LOL 계정 정보 DB INSERT 성공"))


def get_user_id(lol_name: str):
    name = parse.quote(lol_name)
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
    print(riot_user_info_response)
    if (
        isinstance(riot_user_info_response, dict)
        and riot_user_info_response.get("status", {}).get("status_code") == 400
    ):
        return JSONResponse(status_code=400, content=dict(msg="잘못된 소환사 id"))

    if not riot_user_info_response and len(riot_user_info_response) < 1:
        return JSONResponse(status_code=404, content=dict(msg="잘못된 소환사 id"))

    return (
        riot_user_info_response[0]
        if isinstance(riot_user_info_response, list)
        else riot_user_info_response
    )


# 420 : 솔로랭크 440 : 자유랭크
def get_recent_games(lol_name: str, queue_type: str):
    user_id_data = get_user_id(lol_name)
    puuid = user_id_data.get("puuid")

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

    # 요청 횟수 초과 조건
    while response and not (
        isinstance(response, dict)
        and response.get("status", {}).get("status_code") == 429
    ):
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


def get_match_info_by_user(match_id: str, puuid: str):
    url = "/".join([RIOT_API_URLS["GET_MATCH_INFO"], match_id])
    params = {"api_key": api_key}
    response = requests.get(url, params=params).json()

    match_info = response.get("info", {})
    match_participants_info = match_info.get("participants")
    participants = response.get("metadata", {}).get("participants")

    result = list(
        filter(lambda info: info.get("puuid") == puuid, match_participants_info)
    )

    if not result and len(result) < 1:
        return {"status_code": HTTP_404_NOT_FOUND, "message": "일치하는 항목 없음"}

    result = result[0]

    return {
        "puuid": puuid,
        "match_id": match_id,
        "match_type": match_info.get("queueId"),
        "line_name": result.get("individualPosition"),
        "champ_name": result.get("championName"),
        "kills": result.get("kills"),
        "deaths": result.get("deaths"),
        "assists": result.get("assists"),
        "win": result.get("win"),
        "participants": participants,
    }


def get_match_info(match_id: str):
    url = "/".join([RIOT_API_URLS["GET_MATCH_INFO"], match_id])
    params = {"api_key": api_key}
    response = requests.get(url, params=params).json()

    return response


def get_match_info_ods(lol_name: str):
    global global_rds_conn

    match_ids = exec_query(
        global_rds_conn, SELECT_MATCH_ID_INFO_N, input_params={"lol_name": lol_name}
    )

    if not match_ids or len(match_ids) < 1:
        return {"status_code": HTTP_404_NOT_FOUND, "message": "모든 매치 정보 수집 했음"}

    ret = []
    for idx, data in enumerate(match_ids):
        match_id = data.get("match_id")

        url = "/".join([RIOT_API_URLS["GET_MATCH_INFO"], match_id])
        params = {"api_key": api_key}
        response = requests.get(url, params=params).json()
        if response.get("status", {}).get("status_code") == 429:
            print("요청 횟수 초과")
            break
        elif response.get("status", {}).get("status_code") == 403:
            print("Forbidden")
            break

        ret.append(
            {
                "match_id": match_id,
                "metadata": json.dumps(response.get("metadata"), ensure_ascii=False),
                "info": json.dumps(response.get("info"), ensure_ascii=False),
            }
        )
        if idx > 12:
            break
    if not ret:
        return {"status_code": HTTP_404_NOT_FOUND, "message": "API 요청 실패"}

    exec_multiple_queries(global_rds_conn, INSERT_MATCH_INFO_ODS, ret)

    update_query = (
        UPDATE_USERS_MATCH_ODS_YN
        + UPDATE_USERS_MATCH_ODS_YN_WHERE
        + str(tuple(list(map(lambda data: data.get("match_id"), ret))))
    ).replace(",)", ")") + ";"

    exec_query(
        global_rds_conn, update_query, select_flag=False, input_params={"ods_yn": "Y"}
    )

    return str(tuple(list(map(lambda data: data.get("match_id"), ret))))


def get_login(id: str, pwd: str):
    user_os = "linux"
    current_os = platform.platform()

    if "mac" in current_os:
        user_os = "mac"
    elif "linux" in current_os:
        user_os = "linux"
    elif "window" in current_os or "Window" in current_os:
        user_os = "window"

    webdriver_options = webdriver.ChromeOptions()
    webdriver_options.add_argument("headless")

    # webdirver옵션에서 headless기능을 사용하겠다 라는 내용
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")

    if user_os == "linux":
        options.binary_location = "/usr/bin/google-chrome"
        options.add_argument("--single-process")
        options.add_argument("--disable-dev-shm-usage")

    driver_path = (
        "/".join([os.path.dirname(os.path.realpath(__file__)), "chromedriver"])
        + "_"
        + user_os
        + (".exe" if user_os == "window" else "")
    )

    driver = webdriver.Chrome(
        executable_path=driver_path, options=webdriver_options, chrome_options=options
    )

    driver.get(RIOT_API_URLS["DEV_LOGIN_PAGE"])

    time.sleep(1)

    driver.find_element(By.NAME, "username").send_keys(id)
    driver.find_element(By.NAME, "password").send_keys(pwd)
    driver.find_element(By.NAME, "password").send_keys(Keys.ENTER)

    time.sleep(4)

    current_url = driver.current_url
    driver.quit()

    if "https://developer.riotgames.com/" in current_url:
        return JSONResponse(status_code=200, content=dict(msg="셀레니움 로그인 성공"))
    else:
        return JSONResponse(status_code=404, content=dict(msg="셀레니움 로그인 실패"))
