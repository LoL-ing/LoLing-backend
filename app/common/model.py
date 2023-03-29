from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy import (
    Column,
    String,
    Integer,
    DateTime,
)
from sqlalchemy.sql import func

from sqlmodel import SQLModel as _SQLModel, Field


class SQLModel(_SQLModel):
    class Config:
        arbitrary_types_allowed = True

    pass
    # @declared_attr  # type: ignore
    # def __tablename__(cls) -> str:
    #     return cls.__name__


class BaseIdModel(SQLModel):
    id: Optional[int] = Field(
        primary_key=True,
        index=True,
        nullable=False,
    )
    updated_at: datetime = Field(
        nullable=True,
        default_factory=lambda: datetime.utcnow() + timedelta(hours=9),
        sa_column_kwargs={"onupdate": lambda: datetime.utcnow() + timedelta(hours=9)},
    )
    created_at: datetime = Field(
        nullable=True, default_factory=lambda: datetime.utcnow() + timedelta(hours=9)
    )


class BaseLolProfile(SQLModel):
    puu_id: str = Field(
        max_length=78,
        primary_key=True,
        nullable=False,
        description="라이엇 API에서 제공하는 글로벌한 소환사의 고유 번호. lol profile을 구분하기 위한 필수 요소이다. 또한 라이엇 API에서 Match ID를 불러오는데 쓰이는 고유번호이다.",
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.utcnow() + timedelta(hours=9),
        sa_column_kwargs={"onupdate": lambda: datetime.utcnow() + timedelta(hours=9)},
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.utcnow() + timedelta(hours=9)
    )


class Champions(SQLModel, table=True):
    __tablename__ = "CHAMPIONS"
    name_en: str = Field(
        max_length=20,
        nullable=False,
        unique=True,
        description="champion의 영어 이름이다.",
        primary_key=True,
    )
    name_kr: str = Field(
        max_length=15,
        nullable=False,
        unique=True,
        description="champion 의 한글 이름이다. (API 요청 시 영어 이름이 오기에 필요)",
    )
    image_url: str = Field(
        max_length=2083, nullable=True, description="champion 에 해당하는 image 의 url 값이다."
    )


class Items(BaseIdModel, table=True):
    __tablename__ = "ITEMS"
    name: str = Field(max_length=50, nullable=False, description="item 의 이름이다.")
    image_url: str = Field(
        max_length=2083, nullable=True, description="champion 에 해당하는 image 의 url 값이다."
    )


class Lines(SQLModel, table=True):
    __tablename__ = "LINES"
    name: str = Field(
        max_length=10,
        nullable=False,
        description="line 의 이름이다.",
        primary_key=True,
    )
    image_url: str = Field(
        max_length=2083, nullable=True, description="line 에 해당하는 image 의 url 값이다."
    )


class Profile_icons(BaseIdModel, table=True):
    __tablename__ = "PROFILE_ICONS"
    image_url: str = Field(
        max_length=2083,
        nullable=True,
        description="profile_icon 에 해당하는 image 의 url 값이다.",
    )


class Queues(BaseIdModel, table=True):
    __tablename__ = "QUEUES"
    type: str = Field(
        max_length=30,
        nullable=False,
        unique=True,
        description="라이엇 API에서 제공하는 큐 종류를 나타낸 문자열. 큐 종류의 구체적인 이름을 알 수 있다.",
    )


class Runes(BaseIdModel, table=True):
    __tablename__ = "RUNES"
    name: str = Field(
        max_length=20, nullable=False, unique=True, description="rune 의 이름이다."
    )
    image_url: str = Field(
        max_length=2083, nullable=True, description="rune 에 해당하는 image 의 url 값이다."
    )


class Schools(BaseIdModel, table=True):
    __tablename__ = "SCHOOLS"
    name: str = Field(
        max_length=25,
        nullable=False,
        unique=True,
        description="user가 다니는school의 이름이다. 각 user가 속한 학교의 이름을 알리는데 필요하다.",
    )
    school_type: str = Field(
        max_length=1,
        nullable=True,
        description="초등학교, 중학교, 고등학교, 대학교를 구분한 요소이다. 학교별 구분을 용이하게 하는 목적으로 사용한다.",
    )


class Tiers(BaseIdModel, table=True):
    __tablename__ = "TIERS"
    name: str = Field(
        max_length=20, nullable=False, unique=True, description="tier 의 이름이다."
    )
    image_url: str = Field(
        max_length=2083, nullable=True, description="tier 에 해당하는 image 의 url 값이다."
    )


class Spells(BaseIdModel, table=True):
    __tablename__ = "SPELLS"
    name: str = Field(
        max_length=30, nullable=False, unique=True, description="spell의 공식 명칭이다."
    )
    image_url: str = Field(
        max_length=2083,
        nullable=True,
        description="profile icon 에 해당하는 image 의 url 값이다.",
    )
