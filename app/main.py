from pydantic import BaseModel, Field
from fastapi import Depends, FastAPI, Request
from requests import Session
from sqlalchemy import select

# Routes
from app.community.router import router as community_router
from app.users.router import router as users_router
from app.match_history.router import router as match_history_router

# Models
# * DB 생성 전 import 하여 불러오기
from app.common.model import *
from app.users.model import *
from app.community.model import *
from app.match_history.model import *

# DB config
from app.database import Base, engine, get_db

app = FastAPI()

# DB Create
Base.metadata.create_all(bind=engine)

# attach routers
app.include_router(users_router, prefix="/users", tags=["유저 등록 및 로그인"])
app.include_router(community_router, prefix="/community", tags=["커뮤니티"])
app.include_router(match_history_router, prefix="/match_history", tags=["유저 매치 히스토리"])


@app.get("/")
async def root(request: Request):
    url_list = [
        {"path": route.path, "name": route.name} for route in request.app.routes
    ]
    return url_list
