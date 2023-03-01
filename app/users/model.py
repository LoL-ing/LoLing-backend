from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy.sql import func

from sqlalchemy import (
    Column,
    String,
    Integer,
    DateTime,
)
from sqlmodel import Field
from app.common.model import BaseIdModel, BaseLolProfile, SQLModel

from app.database import Base


class UsersBase(SQLModel):
    signin_id: str = Field(max_length=30, primary_key=True)
    password: str = Field(max_length=200, description="앱 로그인 pw")
    name: str = Field(max_length=20, description="실제 사용자 이름")
    username: str = Field(max_length=10)
    self_desc: str = Field(max_length=200)
    phone_num: str = Field(max_length=11)


class Users(UsersBase, table=True):
    __tablename__ = "USERS"
    hashed_password: str = Field(max_length=200, description="암호화 pw")
    manner_tier: Optional[str] = Field(max_length=20, nullable=True)
    curr_lol_account: Optional[str] = Field(max_length=30, nullable=True)
    like_cnt: int = Field(default=0)
    hate_cnt: int = Field(default=0)
    profile_image_uri: str = Field(max_length=200, nullable=True)
    updated_at: datetime = Field(
        default_factory=lambda: datetime.utcnow() + timedelta(hours=9),
        sa_column_kwargs={"onupdate": lambda: datetime.utcnow() + timedelta(hours=9)},
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.utcnow() + timedelta(hours=9)
    )


class Relationships(BaseIdModel, table=True):
    __tablename__ = "RELATIONSHIPS"
    accepted: int = Field(
        nullable=False,
        description="request가 response 되었는지(Y = 1/N = 0)에 대한 상태를 나타낸다.",
    )
    from_user_id: int = Field(
        nullable=False, description="matching이나 friend request를 거는 user의 고유 번호. "
    )
    message_id: str = Field(
        max_length=24,
        unique=True,
        description="matching이나 friend request를 거는 user가, 받는 user에게 보내는 메세지.",
    )
    to_user_id: int = Field(
        nullable=False, description="matching이나 friend request를 받는 user 의 고유 번호. "
    )
    type: str = Field(
        max_length=8,
        nullable=False,
        description="해당 relationship이 매칭 요청인지, 친구 요청 인지를 구분한다.",
    )


class Lol_profiles(BaseLolProfile, table=True):
    __tablename__ = "LOL_PROFILES"
    profile_icon_id: int = Field(
        nullable=False, description="해당 lol profile이 설정한 profile icon의 고유 번호."
    )
    region: str = Field(
        max_length=5,
        description="해당 LoL 계정이 속해 있는 지역 정보. summoner_id의 지역을 구분하기 위한 필수 요소이다.",
    )
    summoner_id: str = Field(
        max_length=47,
        unique=True,
        description="라이엇 API에서 제공하는 소환사를 구별하기 위한 고유 번호.라이엇 API의 league 정보를 불러오는데 쓰이는 고유번호이다.",
    )
    summoner_level: int = Field(
        nullable=False, description="해당 lol profile의 롤 계정 레벨이다."
    )
    summoner_name: str = Field(
        max_length=20, description="해당 lol profile의 롤에서 사용하고 있는 소환사 이름이다."
    )
    user_id: int = Field(
        nullable=False, description="해당 lol profile을 등록한 user의 고유 번호이다."
    )
    last_updated_at: datetime = Field()
