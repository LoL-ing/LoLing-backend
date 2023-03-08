from datetime import datetime
import time
from typing import Union
from fastapi import APIRouter, Depends
from app.apis.riot.controller import RiotApiController
from app.common.schema import IResponseBase, create_response
from app.users.crud import lol_profiles as lol_profiles_crud
from app.match_history.schema import IMatchHistoriesCreate
from app.database import get_db


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

    return match_histories
