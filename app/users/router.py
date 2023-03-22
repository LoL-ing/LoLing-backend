from datetime import datetime
from riotwatcher import ApiError
from app.apis.riot.controller import RiotApiController
from app.common.schema import IResponseBase, create_response
from app.common.utils import as_dict
from fastapi import APIRouter, Body, Depends, HTTPException
from app.users.crud import user as user_crud
from app.users.crud import lol_profiles as lol_profiles_crud
from app.users.schema import ILolProfilesCreate, IUserCreate, IUserRead
from app.database import exec_query, get_db
from app.auth.jwt import auth_required

router = APIRouter()


@router.get("/lolprofile", response_model=IResponseBase[IUserRead])
def get_my_lol_profile(
    decoded_token=Depends(auth_required), db_session=Depends(get_db)
):
    """
    summonerName: string;
    tierName: string;
    rank: number;
    winRate: number;
    wins: number;
    loses: number;
    champions: {img: string, win_rate: number, kda: number}[]; //string url로 주기바람
    positions: {img: string, win_rate: number, kda: number}[];
    """

    signin_id = decoded_token["user_id"]


@router.get("/profile", response_model=IResponseBase[IUserRead])
def get_my_profile(decoded_token=Depends(auth_required), db_session=Depends(get_db)):

    """
        - Header 의 token 을 파싱해서 user_id 를 받아온다
        - user 의 profile 정보를 불러온다
            -
        - return

        nickname: string;
        profileImg: string;
        description: string;
        mannerTierImg: string;
        like: number;
        hate: number;
        schoolName: string;
    }
    """
    signin_id = decoded_token["user_id"]

    user = user_crud.get(signin_id=signin_id, db_session=db_session)

    return create_response(data=user)


@router.get(
    "",
)
def get_user(signin_id: str, db_session=Depends(get_db)):
    user = user_crud.get(signin_id=signin_id, db_session=db_session)

    if user == None:
        return create_response(message="no users", data={})
    return create_response(data=as_dict(user), message="get_user")


@router.post("")
def create_user(
    summoner_name: str,
    signin_id: str = Body(),
    password: str = Body(),
    name: str = Body(),
    username: str = Body(),
    self_desc: str = Body(),
    phone_num: str = Body(),
    hashed_password: str = Body(),
    db_session=Depends(get_db),
):
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
                user_id=signin_id,
                last_updated_at=datetime(year=2023, month=1, day=1),
            ),
            db_session=db_session,
        )
    except:
        raise HTTPException(409, detail="같은 소환사 이름을 가진 사람이 존재합니다.")
    try:
        user_create = IUserCreate(
            signin_id=signin_id,
            password=password,
            hashed_password=password,
            name=name,
            username=username,
            self_desc=self_desc,
            phone_num=phone_num,
            curr_lol_account=puu_id,
        )
        user = user_crud.create(
            obj_in=user_create,
            db_session=db_session,
        )
    except Exception as e:
        print(e)

        raise HTTPException(409, detail="같은 이메일을 가진 사람이 존재합니다.")

    return create_response(data=user)
