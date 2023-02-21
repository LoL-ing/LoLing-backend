from sqlalchemy import (
    VARCHAR,
    Column,
    String,
    Text,
    Date,
    Integer,
    DateTime,
)
from db_connection.rds.orm import Base
from .base_model import BaseIdModel


class Attachments(BaseIdModel):
    __tablename__ = "ATTACHMENTS"
    __table_args__ = {"schema": "COMMUNITY"}
    image_url = Column(String(2083), nullable=False,
                       comment='attachment의 주소. 사진을 불러오기 위한 필수 요소이다.')
    order = Column(Integer, nullable=False,
                   comment='attachment의 게시 순서. 게시물 내에서 사용자가 지정한 게시 순서를 나타낸다.')
    post_id = Column(Integer, nullable=False,
                     comment='attachment가 속한 post의 고유번호. 어떤 게시물에 속해 있는지 구분하기 위한 필수 요소이다.')


class Boards(BaseIdModel):
    __tablename__ = "BOARDS"
    __table_args__ = {"schema": "COMMUNITY"}
    title = Column(String(10), nullable=False,
                   unique=True, comment='board의 제목이다.')
    description = Column(String(30), nullable=False, unique=True)


class Comments(BaseIdModel):
    __tablename__ = "COMMENTS"
    __table_args__ = {"schema": "COMMUNITY"}
    content = Column(Text, nullable=False,
                     comment='comment가 담고 있는 내용이다. text정보만 수용 가능하다. 댓글을 구성하는 핵심 요소이다.')
    like = Column(Integer, nullable=False, comment='comment가 받은 ‘좋아요’ 개수이다. ')
    parent_comment_id = Column(
        Integer, comment='대댓글의 개념처럼 comment의 상위 comment의 고유 번호이다. ')
    parent_post_id = Column(Integer, nullable=False,
                            comment='comment가 달린 게시글의 고유 번호이다. ')
    user_id = Column(Integer, nullable=False,
                     comment='comment를 작성한 user의 id. 댓글을 작성한 사용자의 고유번호를 담고 있는 중요 정보이다. ')


class Current_season_summaries(BaseIdModel):
    __tablename__ = "CURRENT_SEASON_SUMMARIES"
    __table_args__ = {"schema": "COMMUNITY"}
    summoner_id = Column(String(47), nullable=False,
                         comment='라이엇 API에서 제공하는 소환사를 구별하기 위한 고유 번호. 라이엇 API의 league 정보를 불러오는데 쓰이는 고유번호이다.  해당 Current Season Summary의 소환사를 가리킨다.')
    queue_id = Column(Integer, nullable=False,
                      comment='해당 Season Summary가 속한 queue 유형의 고유 번호이다.')
    tier_id = Column(Integer, nullable=False,
                     comment='해당 Season Summary가 속한 tier의 고유 번호이다.')
    rank = Column(String(3), nullable=False,
                  comment='해당 Current Season Summary의 tier를 세분화한 단계이다. ( I ~ IV )')
    lp = Column(Integer, nullable=False,
                comment='해당 current season summary의 league poInteger,이다.')
    wins = Column(Integer, nullable=False, default=0,
                  comment='해당 current season summary의 시즌 전체 승리 횟수이다.')
    losses = Column(Integer, nullable=False, default=0,
                    comment='해당 current season summary의 시즌 전체 패배 횟수이다.')


class Posts(BaseIdModel):
    __tablename__ = "POSTS"
    __table_args__ = {"schema": "COMMUNITY"}
    board_id = Column(Integer, nullable=False,
                      comment='게시물이 포함된 게시판의 id.  어떤 게시판에 속해 있는지 구분하기 위한 필수 요소이다.')
    content = Column(Text, nullable=False, comment='게시물의 내용이다.')
    like = Column(Integer, nullable=False, comment='게시물의 좋아요 수를 나타내는 요소이다.')
    scrap = Column(Integer, nullable=False, comment='게시물의 스크랩 수를 나타내는 요소이다.')
    title = Column(String(30), nullable=False, comment='게시물의 제목이다.')
    user_id = Column(Integer, nullable=False,
                     comment='게시물을 작성한 user의 id. 누가 작성하였는지 구분하기 위한 필수 요소이다.')
    view = Column(Integer, nullable=False, comment='게시물의 조회수를 나타내는 요소이다.')


class Reported_comments(BaseIdModel):
    __tablename__ = "REPORTED_COMMENTS"
    __table_args__ = {"schema": "COMMUNITY"}
    description = Column(String(300), nullable=False,
                         comment='신고된 comment 에 대한 신고 상세 설명이다.')
    reported_comment_id = Column(
        Integer, nullable=False, comment='신고당한 comment의 고유 번호(Comments)이다. ')
    reporter_user_id = Column(Integer, nullable=False,
                              comment='신고한 유저의 고유 번호(Users)이다. ')


class Reported_posts(BaseIdModel):
    __tablename__ = "REPORTED_POSTS"
    __table_args__ = {"schema": "COMMUNITY"}
    description = Column(String(300), nullable=False,
                         comment='post 신고에 대한 신고 상세 설명이다.')
    reported_post_id = Column(Integer, nullable=False,
                              comment='신고당한 post의 고유 번호(Posts)이다. ')
    reporter_user_id = Column(Integer, nullable=False,
                              comment='신고한 유저의 고유 번호(Users)이다. ')


class Reported_Users(BaseIdModel):
    __tablename__ = "REPORTED_USERS"
    __table_args__ = {"schema": "COMMUNITY"}
    reported_user_id = Column(Integer, nullable=False,
                              comment='신고당한 유저의 고유 번호(Users)이다.')
    reporter_user_id = Column(Integer, nullable=False,
                              comment='신고한 유저의 고유 번호(Users)이다. ')
    description = Column(String(300), nullable=False,
                         comment='user 신고에 대한 신고 상세 설명이다.')
