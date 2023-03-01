import datetime
from typing import Union
from pydantic import BaseModel

from app.users.model import UsersBase


class IResUserGet(BaseModel):
    hashed_password: Union[str, None]
    name: Union[str, None]
    username: Union[str, None]
    self_desc: Union[str, None]
    phone_num: Union[str, None]
    manner_tier: Union[str, None]
    curr_lol_account: Union[str, None]
    like_cnt: Union[int, None]
    hate_cnt: Union[int, None]
    profile_image_uri: Union[str, None]
    created_at: Union[datetime.datetime, None]
    updated_at: Union[datetime.datetime, None]

    class Config:
        arbitrary_types_allowed: True


class IUserCreate(UsersBase):
    pass
