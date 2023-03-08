from datetime import datetime
import time
from typing import Union
from fastapi import APIRouter, Depends
from app.apis.riot.controller import RiotApiController
from app.common.schema import IResponseBase, create_response
from app.users.crud import lol_profiles as lol_profiles_crud
from app.match_history.schema import IMatchHistoriesCreate
from app.database import get_db
from app.match_history.crud import match_history_crud

router = APIRouter()


@router.get("/")
def get_match_history():
    return {"[GET] test match_history"}


@router.post("")
def add_match_history(
    puu_id: Union[str, None] = "",
    summoner_name: Union[str, None] = "",
    db_session=Depends(get_db),
) -> IResponseBase[IMatchHistoriesCreate]:
    """
    1. 해당 summoner 의 `last_updated_at` 을 불러온다
    2. `last_updated_at` 이후의 전적 리스트를 불러온다
    3. 각 전적의 상세 정보를 불러온다.
    여기까지 함
    4. TODO: `MATCH_HISTORY` 에 갱신한다.
    """
    riot_api = RiotApiController(summoner_name=summoner_name)

    summoner_info = riot_api.get_summoner_info()
    puu_id = summoner_info.get("puuid", "")

    # * TODO token 기반 user get 으로 변경
    current_lol_profile = lol_profiles_crud.get(puu_id=puu_id, db_session=db_session)
    if current_lol_profile == None:
        return create_response(message="no lol_profile", data={})

    # 마지막 전적 갱신 시간
    last_updated_at = current_lol_profile.last_updated_at
    start_time = int(
        time.mktime(
            datetime.strptime(str(last_updated_at), "%Y-%m-%d %H:%M:%S").timetuple()
        )
    )
    match_histories = []
    match_ids = []
    match_ids = riot_api.get_match_list(count=5, start_time=start_time)

    while match_ids:
        print(len(match_histories))
        print(start_time)

        for match_id in match_ids:
            match_histories.append(riot_api.get_match_info_by_id(match_id=match_id))

        match_histories = sorted(
            match_histories,
            key=lambda item: item.get("info", {}).get("gameStartTimestamp"),
        )

        start_time = match_histories[0].get("info", {}).get("gameStartTimestamp")

        match_ids = riot_api.get_match_list(count=5, start_time=start_time)
        
        # 1번만 하기.. ㅠㅠ
        break
    match_histories_mapped = []
    for match in match_histories:
        
        for participant in match.get("info", {}).get("participants", []):
            match_histories_mapped.append(
                IMatchHistoriesCreate(
            level= participant.get("champLevel", ""),
            CS= participant.get("totalMinionsKilled", 0),
            item_0_id= participant.get("item0"),
            item_1_id= participant.get("item1"),
            item_2_id= participant.get("item2"),
            item_3_id= participant.get("item3"),
            item_4_id= participant.get("item4"),
            item_5_id= participant.get("item5"),
            item_6_id= participant.get("item6"),
            spell_0_id= participant.get("summoner1Id", ""),
            spell_1_id= participant.get("summoner2Id", ""),
            rune_0_id= participant.get("perks", {}).get("styles", [])[0].get("style"),
            rune_1_id= participant.get("perks", {}).get("styles", [])[1].get("style"),
            season= match.get('info', {}).get("gameVersion", ""),
            gold= participant.get("goldEarned", ""),
            play_duration= str(match.get('info', {}).get("gameDuration", "")),
            play_time= str(match.get('info', {}).get("gameStartTimestamp", "")),
            queue_type= match.get('info', {}).get("queueId", ""),
            summoner_name= participant.get("summonerName", ""),
            match_id= match.get("metadata",{}).get("matchId",""),
            line_name= participant.get("lane"),
            champion_name_en= participant.get("championName", ""),
            kill= participant.get("kills", ""),
            death= participant.get("deaths", ""),
            assist= participant.get("assists", ""),
            win_or_lose= 1 if participant.get("win", False) else 0,
                )
            )
    #* List<MatchHistories> create
    print(match_histories_mapped)
    match_history_crud.create_multiple(obj_in_list=match_histories_mapped, db_session=db_session)

    return create_response(data=match_histories, message=f"Riot 전적 정보 {len(match_histories)} 개 insert 완료")
