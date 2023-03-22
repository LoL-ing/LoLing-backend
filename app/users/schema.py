from datetime import datetime
from typing import Optional, Union
from pydantic import BaseModel

from app.users.model import UsersBase
from app.common.model import BaseLolProfile, Schools


class IUserRead(UsersBase):
    hashed_password: str
    manner_tier: Optional[str]
    curr_lol_account: Optional[str]
    like_cnt: int
    hate_cnt: int
    profile_image_uri: Optional[str]

    school: Schools


class IUserCreate(UsersBase):
    hashed_password: str
    curr_lol_account: Optional[str]


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
