import sys
import pathlib

sys.path.append(str(pathlib.Path(__file__).resolve().parents[3]))

from enum import Enum
from typing import Optional
from urllib import parse
import requests
from riotwatcher import LolWatcher, ApiError


from app.common.config import settings


class RiotApiUrl(Enum):
    GET_USER_ID = "https://us.api.riotgames.com/lol/summoner/v4/summoners/by-name"
    GET_USER_INFO = "https://us.api.riotgames.com/lol/league/v4/entries/by-summoner"
    GET_ASIA_RECENT_GAMES = (
        "https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid"
    )
    GET_MATCH_INFO = "https://asia.api.riotgames.com/lol/match/v5/matches"

    def __str__(self):
        return self.value


class RiotApiController:
    def __init__(self, summoner_name: str, signin_id: Optional[str] = ""):
        self.signin_id = signin_id
        self.summoner_name = parse.quote(summoner_name)
        self.api_key = settings.RIOT_API_KEY
        self.my_region = "kr"
        self.lol_watcher = LolWatcher(self.api_key)

        self.summoner_info = self.lol_watcher.summoner.by_name(
            self.my_region, self.summoner_name
        )

        self.puu_id = self.summoner_info.get("puuid", "")
        self.id = self.summoner_info.get("id", "")

        self.base_headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
            "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7,ja;q=0.6",
            "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": "https://developer.riotgames.com",
            "Content-Type": "application/x-www-form-urlencoded",
            "api_key": self.api_key,
        }

        self.base_params = {}

    def get_summoner_info(self):

        return self.lol_watcher._summoner.by_name(
            region=self.my_region, summoner_name=self.summoner_name
        )

    def get_league_info(self):
        return self.lol_watcher.league.by_summoner(self.my_region, self.id)

    def get_match_list(self, start_time: int, count: int):
        ret = self.lol_watcher.match.matchlist_by_puuid(
            puuid=self.puu_id,
            region=self.my_region,
            start_time=start_time,
            count=count,
        )
        return ret

    def get_match_info_by_id(self, match_id: str):
        return self.lol_watcher.match.by_id(region=self.my_region, match_id=match_id)


riot_api = RiotApiController("꼽 죽")
