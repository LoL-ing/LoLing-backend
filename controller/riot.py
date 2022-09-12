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
    exec_sql_file,
    get_rds_db_connection,
)
from exception import LOLINGDBRequestFailException
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

global_rds_conn = get_rds_db_connection()


def post_lol_info(signin_id: str, lol_name: str):
    global global_rds_conn

    # user 정보 DB INSERT
    # user_info 넣을 때, lol_name 만 insert 해두고 나머지를 update 할 지.. update 로 할 지? lock 때문에
    user_id_info = get_user_id(lol_name)
    user_info = get_user_info(user_id_info.get("id", ""))

    print(user_id_info, user_info)

    solo_5x5_info = {}
    flex_sr_info = {}
    for info in user_info:
        if info.get("queueType", "") == "RANKED_FLEX_SR":
            flex_sr_info = info
        elif info.get("queueType", "") == "RANKED_SOLO_5x5":
            solo_5x5_info = info
    exec_query(
        global_rds_conn,
        DELETE_LOL_ACCOUNT,
        select_flag=False,
        input_params={"lol_name": lol_name, "signin_id": signin_id},
    )

    exec_insert_query(
        global_rds_conn,
        INSERT_LOL_ACCOUNT,
        input_params={
            "signin_id": signin_id,
            "lol_name": lol_name,
            "user_id": user_id_info.get("id"),
            "puuid": user_id_info.get("puuid"),
            "wins": solo_5x5_info.get("wins"),
            "losses": solo_5x5_info.get("losses"),
            "tier": " ".join(
                [solo_5x5_info.get("tier", ""), solo_5x5_info.get("rank", "")]
            ),
            "wins_sr": flex_sr_info.get("wins"),
            "losses_sr": flex_sr_info.get("losses"),
            "tier_sr": " ".join(
                [flex_sr_info.get("tier", ""), flex_sr_info.get("rank", "")]
            ),
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
                    "queue_type": queue_type,
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

    print(137, riot_user_info_response)
    if (
        isinstance(riot_user_info_response, dict)
        and riot_user_info_response.get("status", {}).get("status_code") == 400
    ):
        raise LOLINGDBRequestFailException
        return JSONResponse(status_code=400, content=dict(msg="잘못된 소환사 id"))

    if not riot_user_info_response and len(riot_user_info_response) < 1:
        return JSONResponse(status_code=404, content=dict(msg="잘못된 소환사 id"))

    return riot_user_info_response


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
        "queue_type": match_info.get("queueId"),
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
        if idx > 20:
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


def put_fact(lol_name: str):
    global global_rds_conn
    dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

    """
    1. fact 이전인 모든 ODS fact 처리
    2. 모든 ODS 'Y' 상태로 update
    3. 해당 lol_name 에 대해서 mart / lol_account 에 update 시키기
    4. DB 가지고 있는 데이터 바탕으로 전체 승률, KDA update 
    """
    # 1, 2
    exec_sql_file("/".join([dir, "query", "fact", "users_match_history.sql"]))

    # 3
    exec_sql_file(
        "/".join([dir, "query", "mart", "update_lol_account_info.sql"]),
        p_lol_name=lol_name,
    )

    # 4
    exec_sql_file(
        "/".join([dir, "query", "mart", "mart_user_total.sql"]),
        p_lol_name=lol_name,
    )

    return JSONResponse(
        status_code=200, content=dict(msg=f"ODS 전체 FACT / {lol_name} MART 정보 update 성공")
    )
