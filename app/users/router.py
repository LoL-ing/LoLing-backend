from app.apis.riot.controller import RiotApiController
from app.common.schema import create_response
from app.common.utils import as_dict
from fastapi import APIRouter
from app.users.crud import user as user_crud
from app.users.schema import IUserCreate

router = APIRouter()


@router.get(
    "",
)
async def get_user(signin_id: str):
    user = await user_crud.get(signin_id=signin_id)

    if user == None:
        return create_response(message="no users", data={})
    return create_response(data=as_dict(user), message="get_user")


@router.post("")
def create_user(IUserCreate: IUserCreate, summoner_name: str):
    riot_api = RiotApiController(summoner_name=summoner_name)
    summoner_info = riot_api.get_summoner_info()
    puu_id = summoner_info.get("puuid", "")
    return summoner_info
    return user_crud.create(IUserCreate=IUserCreate)
