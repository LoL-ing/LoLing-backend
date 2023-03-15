from datetime import datetime
from riotwatcher import ApiError
from app.apis.riot.controller import RiotApiController
from app.common.schema import create_response
from app.common.utils import as_dict
from fastapi import APIRouter, Depends, HTTPException
from app.users.crud import user as user_crud
from app.users.crud import lol_profiles as lol_profiles_crud
from app.users.schema import ILolProfilesCreate, IUserCreate
from app.database import get_db

router = APIRouter()


@router.get(
    "",
)
def get_user(signin_id: str, db_session=Depends(get_db)):
    user = user_crud.get(signin_id=signin_id, db_session=db_session)

    if user == None:
        return create_response(message="no users", data={})
    return create_response(data=as_dict(user), message="get_user")


@router.post("")
def create_user(body: IUserCreate, summoner_name: str, db_session=Depends(get_db)):
    try:
        riot_api = RiotApiController(summoner_name=summoner_name)
        summoner_info = riot_api.get_summoner_info()
        puu_id = summoner_info.get("puuid", "")
    except Exception as e:
        raise HTTPException(404, detail="소환사 이름을 찾을 수 없습니다.")
    try:
        lol_profiles_crud.create(
            obj_in=ILolProfilesCreate(
                puu_id=puu_id,
                profile_icon_id=summoner_info.get("profileIconId"),
                region="KR",
                summoner_id=summoner_info.get("id"),
                summoner_level=summoner_info.get("summonerLevel"),
                summoner_name=summoner_name,
                user_id=body.signin_id,
                last_updated_at=datetime(year=2023, month=1, day=1),
            ),
            db_session=db_session,
        )
    except:
        raise HTTPException(409, detail="같은 소환사 이름을 가진 사람이 존재합니다.")
    try:
        user = user_crud.create(obj_in=body, db_session=db_session)
    except:
        raise HTTPException(409, detail="같은 이메일을 가진 사람이 존재합니다.")

    return create_response(data=user)
