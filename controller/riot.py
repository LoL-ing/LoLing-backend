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

from util import center_str_by_unciode_len, get_customized_logger

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

logger = get_customized_logger()


def post_lol_info(signin_id: str, lol_name: str):
    """
    1. 첫 회원가입 시, lol_account 에 대한 정보 API call 하여 솔랭, 자유랭 나누어서 update
    2. 최근 유저가 플레이 한 match_id 들을 MATCHES.USERS_MATCH_MAP 에 insert
    """

    global global_rds_conn
    # user 정보 DB INSERT
    # user_info 넣을 때, lol_name 만 insert 해두고 나머지를 update 할 지.. update 로 할 지? lock 때문에
    user_id_info = get_user_id(lol_name)
    user_info = get_user_info(user_id_info.get("id", ""))

    exec_query(
        global_rds_conn,
        DELETE_LOL_ACCOUNT,
        select_flag=False,
        input_params={"lol_name": lol_name, "signin_id": signin_id},
    )

    # 이번 시즌 게임 이력이 없으면 빈 리스트 반환
    if not user_info:
        exec_insert_query(
            global_rds_conn,
            INSERT_LOL_ACCOUNT,
            input_params={
                "signin_id": signin_id,
                "lol_name": lol_name,
                "user_id": None,
                "puuid": None,
                "wins": None,
                "losses": None,
                "tier": "UNRANKED",
                "wins_sr": None,
                "losses_sr": None,
                "tier_sr": "UNRANKED",
            },
        )
        return JSONResponse(status_code=400, content=dict(msg="이번 시즌 게임 이력 없음"))

    solo_5x5_info = {}
    flex_sr_info = {}
    for info in user_info:
        if info.get("queueType", "") == "RANKED_FLEX_SR":
            flex_sr_info = info
        elif info.get("queueType", "") == "RANKED_SOLO_5x5":
            solo_5x5_info = info

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
            )
            if solo_5x5_info.get("tier", "") != ""
            else "UNRANKED",
            "wins_sr": flex_sr_info.get("wins"),
            "losses_sr": flex_sr_info.get("losses"),
            "tier_sr": " ".join(
                [flex_sr_info.get("tier", ""), flex_sr_info.get("rank", "")]
            )
            if flex_sr_info.get("tier", "") != ""
            else "UNRANKED",
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
    """
    lol_name 을 받아서 riot api 내의 고유 id, puuid 받음
    """
    name = parse.quote(lol_name)
    url = "/".join([RIOT_API_URLS["GET_USER_ID"], name])
    params = {"api_key": api_key}
    riot_user_response = requests.get(url, params=params).json()

    if riot_user_response.get("status", {}).get("status_code") == 404:
        return JSONResponse(status_code=404, content=dict(msg="잘못된 소환사 이름"))

    return riot_user_response


def get_user_info(user_id: str):
    url = "/".join([RIOT_API_URLS["GET_USER_INFO"], parse.quote(user_id)])
    params = {"api_key": api_key}
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
        "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7,ja;q=0.6",
        "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://developer.riotgames.com",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    riot_user_info_response = requests.get(
        url, headers=headers, params=parse.urlencode(params)
    ).json()

    if (
        isinstance(riot_user_info_response, dict)
        and riot_user_info_response.get("status", {}).get("status_code") == 400
    ):
        # TODO 없는 소환사 아이디에 대한 오류 분기 추가해야함
        return []

    if not riot_user_info_response and len(riot_user_info_response) < 1:
        return []

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
    """ """
    global global_rds_conn

    # ODS 데이터 수집 전, match id 최신화
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

    # DB 에 있는 match id 중, ODS 수집 하지 않은 match id 만 가져오기
    match_ids = exec_query(
        global_rds_conn, SELECT_MATCH_ID_INFO_N, input_params={"lol_name": lol_name}
    )

    if not match_ids or len(match_ids) < 1:
        return {"status_code": HTTP_404_NOT_FOUND, "message": "모든 매치 정보 수집 했음"}

    ret = []
    for idx, data in enumerate(match_ids):
        match_id = data.get("match_id")
        print(f"{idx} 번 : {match_id}".center(50, "-"))

        url = "/".join([RIOT_API_URLS["GET_MATCH_INFO"], match_id])
        params = {"api_key": api_key}
        response = requests.get(url, params=params).json()
        if response.get("status", {}).get("status_code") == 429:
            print(f"요청 횟수 초과 {idx} 개 요청".center(100, "-"))
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
        # if idx > 20:
        #     break
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
    """
    셀레니움 로그인
    """
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
    """
    한 유저에 대한 정보 갱신
    """
    dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

    logger.info(center_str_by_unciode_len(" users_match_history.sql ", 100, "-"))

    ####### fact #######
    # 1. fact 이전인 모든 ODS fact 처리후 모든 ODS 'Y' 상태로 update
    exec_sql_file("/".join([dir, "query", "fact", "users_match_history.sql"]))

    logger.info(center_str_by_unciode_len(" update_lol_account_info.sql ", 100, "-"))

    ####### mart #######
    # 2. 해당 lol_name 에 대해서 mart / lol_account 에 update 시키기
    exec_sql_file(
        "/".join([dir, "query", "mart", "update_lol_account_info.sql"]),
        p_lol_name=lol_name,
    )

    logger.info(center_str_by_unciode_len(" mart_user_total.sql ", 100, "-"))
    # 3. DB 가지고 있는 데이터 바탕으로 전체 승률, KDA update
    exec_sql_file(
        "/".join([dir, "query", "mart", "mart_user_total.sql"]),
        p_lol_name=lol_name,
    )

    return JSONResponse(
        status_code=200, content=dict(msg=f"ODS 전체 FACT / {lol_name} MART 정보 update 성공")
    )
