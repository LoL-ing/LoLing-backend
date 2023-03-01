import json
from typing import Union
from app.database import get_db
from app.common.schema import IResponseBase, create_response
from app.common.utils import as_dict
from fastapi import APIRouter, Depends

from requests import Session
from app.users.model import Users

from app.users.crud import UserCRUD
from app.users.schema import IResUserGet, IUserCreate

router = APIRouter()

user_crud = UserCRUD()


@router.get(
    "/",
    response_model=IResponseBase[
        Union[
            IResUserGet,
            None,
        ]
    ],
)
def get_user(signin_id: str, db_session: Session = Depends(get_db)):
    user = user_crud.get(signin_id=signin_id, db_session=db_session)

    if user == None:
        return create_response(message="no users", data={})
    return create_response(data=as_dict(user), message="get_user")


@router.post("/")
def create_user(IUserCreate: IUserCreate, db_session: Session = Depends(get_db)):
    return user_crud.create(IUserCreate=IUserCreate, db_session=db_session)
