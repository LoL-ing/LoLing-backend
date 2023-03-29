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


@router.get("/lolprofile")
def get_my_lol_profile(
    # decoded_token=Depends(auth_required),
    db_session=Depends(get_db)
):
    """
    1. 치훈이가 짠 쿼리 -> (LOL_PROFILES, CURRENT_SEASON_SUMMARIES)
    2. MOST CHAMP 3개 가져오고
    3. MOST LINE 3개 가져오기
    4. 합쳐
    5. 내일 학교 가기 (와라 좀 ㅋㅋ)


    summonerName: string;
    tierName: string;
    rank: number;
    winRate: number;
    wins: number;
    loses: number;
    champions: {img: string, win_rate: number, kda: number}[]; //string url로 주기바람
    positions: {img: string, win_rate: number, kda: number}[];
    """
    # * 화이팅!
    signin_id = "t@t.com"

    # 1번 쿼리
    query = """
        SELECT LP.summoner_name, T.name as tier_name, CSS.queue_id, CSS.rank , CSS.wins, CSS.losses, CSS.id as current_season_summary_id, CSS.queue_id as queue_id FROM USERS U
          LEFT OUTER JOIN LOL_PROFILES LP
            ON U.curr_lol_account = LP.puu_id
          LEFT OUTER JOIN CURRENT_SEASON_SUMMARIES CSS
            ON CSS.puu_id = LP.puu_id
          LEFT OUTER JOIN TIERS T
            ON T.id = CSS.tier_id
         WHERE U.signin_id = %(signin_id)s
         ;
    """

    summoner_info = exec_query(db_session, query, input_params={
                               'signin_id': signin_id})

    query_2 = f"""
        SELECT MCS.*, C.image_url as image_url, CSS.queue_id as queue_id
          FROM MOST_CHAMPION_SUMMARIES MCS
          LEFT OUTER JOIN CHAMPIONS C
            ON C.name_en = MCS.champion_name
          LEFT OUTER JOIN CURRENT_SEASON_SUMMARIES CSS
            ON CSS.id = MCS.current_season_summary_id
         WHERE current_season_summary_id in ({','.join(map(lambda item: str(item.get("current_season_summary_id")), summoner_info))})

         ;
    """

    most_champs = exec_query(db_session, query_2)

    most_champs = list(map(lambda item: {'queue_id': item.get('queue_id'), 'img': item.get('image_url'), 'win_rate':  item.get(
        'win_rate', 0), 'kda': item.get('kda', 0), 'champion_name': item.get('champion_name')}, most_champs))

    query_3 = f"""
        SELECT MLS.*, L.image_url as image_url, CSS.queue_id as queue_id, L.name as line_name
          FROM MOST_LINE_SUMMARIES MLS
          LEFT OUTER JOIN `LINES` L
            ON L.name = MLS.line_name
          LEFT OUTER JOIN CURRENT_SEASON_SUMMARIES CSS
            ON CSS.id = MLS.current_season_summary_id
         WHERE MLS.current_season_summary_id in ({','.join(map(lambda item: str(item.get("current_season_summary_id")), summoner_info))})

         ;
    """
    most_lines = exec_query(db_session, query_3)

    most_lines = list(map(lambda item: {'queue_id': item.get('queue_id'), 'img': item.get('image_url'), 'win_rate':  item.get(
        'win_rate', 0), 'kda': item.get('kda', 0), 'line': item.get('line_name', 'NONE')}, most_lines))

    ret = []

    for info in summoner_info:
        champs = list(filter(lambda item: item.get("queue_id") ==
                             info.get("queue_id"), most_champs))
        lines = list(filter(lambda item: item.get("queue_id")
                            == info.get("queue_id"), most_lines))

        ret.append({**info, "champions": champs,
                    "positions": lines, })

    return ret


@ router.get("/profile", response_model=IResponseBase[IUserRead])
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


@ router.get(
    "",


)
def get_user(signin_id: str, db_session=Depends(get_db)):
    user = user_crud.get(signin_id=signin_id, db_session=db_session)

    if user == None:
        return create_response(message="no users", data={})
    return create_response(data=as_dict(user), message="get_user")


@ router.post("")
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
            school_id=1,
        )
        user = user_crud.create(
            obj_in=user_create,
            db_session=db_session,
        )
    except Exception as e:
        print(e)

        raise HTTPException(409, detail="같은 이메일을 가진 사람이 존재합니다.")

    return create_response(data=user)
