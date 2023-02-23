from sqlalchemy.sql import func

from sqlalchemy import (
    Column,
    String,
    Integer,
    DateTime,
)
from app.common.model import BaseIdModel

from app.database import Base


class Users(Base):
    __tablename__ = "USERS"
    __table_args__ = {"schema": "USER"}
    signin_id = Column(String(30), primary_key=True)
    hashed_password = Column(String(200), comment="앱 로그인 pw")
    name = Column(String(20), comment="실제 사용자 이름")
    username = Column(String(10))
    self_desc = Column(String(200))
    phone_num = Column(String(11))
    manner_tier = Column(String(20))
    curr_lol_account = Column(String(30))
    like_cnt = Column(Integer)
    hate_cnt = Column(Integer)
    profile_image_uri = Column(String(200))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class Relationships(BaseIdModel):
    __tablename__ = "RELATIONSHIPS"
    __table_args__ = {"schema": "USER"}
    accepted = Column(
        Integer,
        nullable=False,
        comment="request가 response 되었는지(Y = 1/N = 0)에 대한 상태를 나타낸다.",
    )
    from_user_id = Column(
        Integer, nullable=False, comment="matching이나 friend request를 거는 user의 고유 번호. "
    )
    message_id = Column(
        String(24),
        unique=True,
        comment="matching이나 friend request를 거는 user가, 받는 user에게 보내는 메세지.",
    )
    to_user_id = Column(
        Integer, nullable=False, comment="matching이나 friend request를 받는 user 의 고유 번호. "
    )
    type = Column(
        String(8), nullable=False, comment="해당 relationship이 매칭 요청인지, 친구 요청 인지를 구분한다."
    )


class Lol_profiles(Base):
    __tablename__ = "LOL_PROFILES"
    __table_args__ = {"schema": "USER"}
    puu_id = Column(
        String(78),
        primary_key=True,
        nullable=False,
        comment="라이엇 API에서 제공하는 글로벌한 소환사의 고유 번호. lol profile을 구분하기 위한 필수 요소이다. 또한 라이엇 API에서 Match ID를 불러오는데 쓰이는 고유번호이다.",
    )
    profile_icon_id = Column(
        Integer, nullable=False, comment="해당 lol profile이 설정한 profile icon의 고유 번호."
    )
    region = Column(
        String(5), comment="해당 LoL 계정이 속해 있는 지역 정보. summoner_id의 지역을 구분하기 위한 필수 요소이다."
    )
    summoner_id = Column(
        String(47),
        unique=True,
        comment="라이엇 API에서 제공하는 소환사를 구별하기 위한 고유 번호.라이엇 API의 league 정보를 불러오는데 쓰이는 고유번호이다.",
    )
    summoner_level = Column(
        Integer, nullable=False, comment="해당 lol profile의 롤 계정 레벨이다."
    )
    summoner_name = Column(String(20), comment="해당 lol profile의 롤에서 사용하고 있는 소환사 이름이다.")
    user_id = Column(
        Integer, nullable=False, comment="해당 lol profile을 등록한 user의 고유 번호이다."
    )
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
