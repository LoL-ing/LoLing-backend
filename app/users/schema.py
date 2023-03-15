from datetime import datetime
from typing import Union
from pydantic import BaseModel

from app.users.model import UsersBase
from app.common.model import BaseLolProfile


class IUserCreate(UsersBase):
    hashed_password: str


class IUserUpdate(UsersBase):
    pass


class ILolProfilesCreate(BaseModel):
    puu_id: str
    profile_icon_id: int
    region: str
    summoner_id: str
    summoner_level: int
    summoner_name: str
    user_id: str
    last_updated_at: datetime


class ILolProfilesUpdate(BaseLolProfile):
    pass
