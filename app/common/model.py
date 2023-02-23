from sqlalchemy import (
    VARCHAR,
    Column,
    String,
    Date,
    Integer,
    DateTime,
)
from sqlalchemy.sql import func

from app.database import Base


class BaseIdModel(Base):
    id = Column(Integer, autoincrement=True, nullable=False, primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    __abstract__ = True

    class Config:
        orm_mode: True
        arbitrary_types_allowed: True


# ---


class Champions(BaseIdModel):
    __tablename__ = "CHAMPIONS"
    __table_args__ = {"schema": "COMMON"}
    name_en = Column(
        String(20), nullable=False, unique=True, comment="champion의 영어 이름이다."
    )
    name_kr = Column(
        String(15),
        nullable=False,
        unique=True,
        comment="champion 의 한글 이름이다. (API 요청 시 영어 이름이 오기에 필요)",
    )
    image_url = Column(
        String(2083), nullable=True, comment="champion 에 해당하는 image 의 url 값이다."
    )


class Items(BaseIdModel):
    __tablename__ = "ITEMS"
    __table_args__ = {"schema": "COMMON"}
    name = Column(String(50), nullable=False, comment="item 의 이름이다.")
    image_url = Column(
        String(2083), nullable=True, comment="champion 에 해당하는 image 의 url 값이다."
    )


class Lines(BaseIdModel):
    __tablename__ = "LINES"
    __table_args__ = {"schema": "COMMON"}
    name = Column(String(10), nullable=False, unique=True, comment="line 의 이름이다.")
    image_url = Column(
        String(2083), nullable=True, comment="line 에 해당하는 image 의 url 값이다."
    )


class Profile_icons(BaseIdModel):
    __tablename__ = "PROFILE_ICONS"
    __table_args__ = {"schema": "COMMON"}
    image_url = Column(
        String(2083), nullable=True, comment="profile_icon 에 해당하는 image 의 url 값이다."
    )


class Queues(BaseIdModel):
    __tablename__ = "QUEUES"
    __table_args__ = {"schema": "COMMON"}
    type = Column(
        String(30),
        nullable=False,
        unique=True,
        comment="라이엇 API에서 제공하는 큐 종류를 나타낸 문자열. 큐 종류의 구체적인 이름을 알 수 있다.",
    )


class Runes(BaseIdModel):
    __tablename__ = "RUNES"
    __table_args__ = {"schema": "COMMON"}
    name = Column(String(20), nullable=False, unique=True, comment="rune 의 이름이다.")
    image_url = Column(
        String(2083), nullable=True, comment="rune 에 해당하는 image 의 url 값이다."
    )


class Schools(BaseIdModel):
    __tablename__ = "SCHOOLS"
    __table_args__ = {"schema": "COMMON"}
    name = Column(
        String(25),
        nullable=False,
        unique=True,
        comment="user가 다니는school의 이름이다. 각 user가 속한 학교의 이름을 알리는데 필요하다.",
    )
    school_type = Column(
        String(1),
        nullable=True,
        comment="초등학교, 중학교, 고등학교, 대학교를 구분한 요소이다. 학교별 구분을 용이하게 하는 목적으로 사용한다.",
    )


class Tiers(BaseIdModel):
    __tablename__ = "TIERS"
    __table_args__ = {"schema": "COMMON"}
    name = Column(String(20), nullable=False, unique=True, comment="tier 의 이름이다.")
    image_url = Column(
        String(2083), nullable=True, comment="tier 에 해당하는 image 의 url 값이다."
    )


class Spells(BaseIdModel):
    __tablename__ = "SPELLS"
    __table_args__ = {"schema": "COMMON"}
    name = Column(String(20), nullable=False, unique=True, comment="spell의 공식 명칭이다.")
    image_url = Column(
        String(2083), nullable=True, comment="profile icon 에 해당하는 image 의 url 값이다."
    )
