import os

from dotenv import load_dotenv
from sqlalchemy import (
    VARCHAR,
    Column,
    String,
    Date,
    Integer,
    DateTime,
)
from db_connection.rds.orm import Base


class User(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "USER"}
    signin_id = Column(String(30), primary_key=True)
    password = Column(String(20), comment="앱 로그인 pw")
    name = Column(String(20), comment="실제 사용자 이름")
    username = Column(String(10))
    self_desc = Column(String(200))
    phone_num = Column(String(11))
    manner_tier = Column(String(20))
    curr_lol_account = Column(String(30))
    like_cnt = Column(Integer)
    hate_cnt = Column(Integer)
    profile_image_uri = Column(String(200))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
