from sqlalchemy import (
    VARCHAR,
    Column,
    String,
    Text,
    Date,
    Integer,
    DateTime,
)
from sqlmodel import Field
from app.common.model import BaseIdModel


class Attachments(BaseIdModel, table=True):
    __tablename__ = "ATTACHMENTS"
    __table_args__ = {"schema": "COMMUNITY"}
    image_url: str = Field(
        max_length=203,
        nullable=False,
        description="attachment의 주소. 사진을 불러오기 위한 필수 요소이다.",
    )
    order: int = Field(
        nullable=False,
        description="attachment의 게시 순서. 게시물 내에서 사용자가 지정한 게시 순서를 나타낸다.",
    )
    post_id: int = Field(
        nullable=False,
        description="attachment가 속한 post의 고유번호. 어떤 게시물에 속해 있는지 구분하기 위한 필수 요소이다.",
    )


class Boards(BaseIdModel, table=True):
    __tablename__ = "BOARDS"
    __table_args__ = {"schema": "COMMUNITY"}
    title: str = Field(
        max_length=10, nullable=False, unique=True, description="board의 제목이다."
    )
    description: str = Field(max_length=30, nullable=False, unique=True)


class Comments(BaseIdModel, table=True):
    __tablename__ = "COMMENTS"
    __table_args__ = {"schema": "COMMUNITY"}
    content: str = Field(
        nullable=False,
        description="comment가 담고 있는 내용이다. text정보만 수용 가능하다. 댓글을 구성하는 핵심 요소이다.",
    )
    like: int = Field(nullable=False, description="comment가 받은 ‘좋아요’ 개수이다. ")
    parent_comment_id: int = Field(
        description="대댓글의 개념처럼 comment의 상위 comment의 고유 번호이다. "
    )
    parent_post_id: int = Field(
        nullable=False, description="comment가 달린 게시글의 고유 번호이다. "
    )
    user_id: int = Field(
        nullable=False,
        description="comment를 작성한 user의 id. 댓글을 작성한 사용자의 고유번호를 담고 있는 중요 정보이다. ",
    )


class Posts(BaseIdModel, table=True):
    __tablename__ = "POSTS"
    __table_args__ = {"schema": "COMMUNITY"}
    board_id: int = Field(
        nullable=False,
        description="게시물이 포함된 게시판의 id.  어떤 게시판에 속해 있는지 구분하기 위한 필수 요소이다.",
    )
    content: str = Field(nullable=False, description="게시물의 내용이다.")
    like: int = Field(nullable=False, description="게시물의 좋아요 수를 나타내는 요소이다.")
    scrap: int = Field(nullable=False, description="게시물의 스크랩 수를 나타내는 요소이다.")
    title: str = Field(max_length=30, nullable=False, description="게시물의 제목이다.")
    user_id: int = Field(
        nullable=False, description="게시물을 작성한 user의 id. 누가 작성하였는지 구분하기 위한 필수 요소이다."
    )
    view: int = Field(nullable=False, description="게시물의 조회수를 나타내는 요소이다.")


class Reported_comments(BaseIdModel, table=True):
    __tablename__ = "REPORTED_COMMENTS"
    __table_args__ = {"schema": "COMMUNITY"}
    description: str = Field(
        max_length=30, nullable=False, description="신고된 comment 에 대한 신고 상세 설명이다."
    )
    reported_comment_id: int = Field(
        nullable=False, description="신고당한 comment의 고유 번호(Comments)이다. "
    )
    reporter_user_id: int = Field(
        nullable=False, description="신고한 유저의 고유 번호(Users)이다. "
    )


class Reported_posts(BaseIdModel, table=True):
    __tablename__ = "REPORTED_POSTS"
    __table_args__ = {"schema": "COMMUNITY"}
    description: str = Field(
        max_length=30, nullable=False, description="post 신고에 대한 신고 상세 설명이다."
    )
    reported_post_id: int = Field(
        nullable=False, description="신고당한 post의 고유 번호(Posts)이다. "
    )
    reporter_user_id: int = Field(
        nullable=False, description="신고한 유저의 고유 번호(Users)이다. "
    )


class Reported_Users(BaseIdModel, table=True):
    __tablename__ = "REPORTED_USERS"
    __table_args__ = {"schema": "COMMUNITY"}
    reported_user_id: int = Field(
        nullable=False, description="신고당한 유저의 고유 번호(Users)이다."
    )
    reporter_user_id: int = Field(
        nullable=False, description="신고한 유저의 고유 번호(Users)이다. "
    )
    description: str = Field(
        max_length=30, nullable=False, description="user 신고에 대한 신고 상세 설명이다."
    )
