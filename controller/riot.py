import os
import queue
import requests
import logging
from urllib import parse

from dotenv.main import load_dotenv
load_dotenv()
api_key = os.environ.get("RIOT_API_KEY")


def get_user_id(summoner_name: str):
    name = parse.quote(summoner_name)
    url = 'https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/' + name +'?api_key=' + api_key 
    response = requests.get(url).json()
    id = response['id']
    puuid = response['puuid']
    profile_icon_id = response['profileIconId']

    return id, puuid, profile_icon_id, summoner_name

def get_user_info(id: str):
    url = 'https://kr.api.riotgames.com/lol/league/v4/entries/by-summoner/' + id +'?api_key=' + api_key 
    response = requests.get(url).json()
    result = []
    if(response):
        for r in response:
            queue_type = r['queueType']
            tier = r['tier']
            rank = r['rank']
            wins = r['wins']
            losses = r['losses']
            result.append([queue_type, tier, rank, wins, losses])
    
    return result


def get_recent_games(puuid: str, queue_type: str):
    start = 0
    count = 100
    url = 'https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/'+ puuid + '/ids?startTime=1641528000&queue='+ queue_type +'&type=ranked&start=' + str(start) + '&count=' + str(count) +'&api_key=' + api_key

    response = requests.get(url).json()
    result = []
    
    while (response):
        result.extend(response)
        start+=count
        url = 'https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/'+ puuid + '/ids?startTime=1641528000&queue='+ queue_type +'&type=ranked&start=' + str(start) + '&count=' + str(count) +'&api_key=' + api_key
        response = requests.get(url).json()
    
    return result