import datetime
from typing import Union
from pydantic import BaseModel


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


class IUserCreate(BaseModel):
    # Column(String(30), primary_key=True)
    signin_id: str
    # Column(String(200), comment="앱 로그인 pw")
    password: str
    # Column(String(20), comment="실제 사용자 이름")
    name: str
    # Column(String(10))
    username: str
    # Column(String(200))
    self_desc: str
    # Column(String(11))
    phone_num: str
    # Column(String(200))
    profile_image_uri: str
