from datetime import datetime
from typing import List
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
from app.users.model import Users

router = APIRouter()


@router.get("/friend")
def get_user_friends(
    decoded_token=Depends(auth_required), db_session=Depends(get_db)
) -> IResponseBase[List[Users]]:
    signin_id = decoded_token["user_id"]

    query = f"""
    SELECT U.*
         , S.name as school_name
      FROM USERS as U
     INNER JOIN RELATIONSHIPS as R
        ON U.signin_id = R.from_user_id
        OR U.signin_id = R.to_user_id
     INNER JOIN SCHOOLS S on U.school_id = S.id
     WHERE U.signin_id = '{signin_id}'
    ;
    """

    friend_profiles = exec_query(
        conn=db_session,
        query_str=query,
    )

    return create_response(friend_profiles)
