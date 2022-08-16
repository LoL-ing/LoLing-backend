import os

import requests
from starlette.responses import JSONResponse

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


# 420 : 솔로랭크 440 : 자유랭크
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


def get_login(id: str, pwd: str):
    user_os = "linux"
    current_os = platform.platform()

    if 'mac' in current_os:
        user_os = 'mac'
    elif 'linux' in current_os:
        user_os = 'linux'
    elif 'window' in current_os or 'Window' in current_os:
        user_os = 'window'

    webdriver_options = webdriver.ChromeOptions()
    webdriver_options.add_argument("headless")
    
    # webdirver옵션에서 headless기능을 사용하겠다 라는 내용
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')

    if user_os == "linux":
        options.binary_location = "/usr/bin/google-chrome"
        options.add_argument("--single-process")
        options.add_argument("--disable-dev-shm-usage")
    
    driver_path = (
        "/".join([os.path.dirname(os.path.realpath(__file__)), "chromedriver"])
        + "_"
        + user_os
        + (".exe" if user_os == 'window' else '') 
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

    if current_url == "https://developer.riotgames.com/":
        return JSONResponse(status_code=200, content=dict(msg="셀레니움 로그인 성공"))
    else:
        return JSONResponse(status_code=404, content=dict(msg="셀레니움 로그인 실패"))
