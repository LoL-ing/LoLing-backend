from fastapi import Depends, FastAPI, Request
from requests import Session
from sqlalchemy import select
from db_connection.rds.orm import Base, engine, get_db
from route import champions, profiles, profiles, users, riot
from dotenv.main import load_dotenv
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from os import environ
from exception import *
from models import Base
from models.user_models import User

app = FastAPI()
load_dotenv()

# DB Create
Base.metadata.create_all(bind=engine)

# attach routers
app.include_router(champions.router, prefix="/champions", tags=["챔피언"])
app.include_router(profiles.router, prefix="/profiles", tags=["프로필"])
app.include_router(users.router, prefix="/users", tags=["유저 등록 및 로그인"])
app.include_router(riot.router, prefix="/riot", tags=["라이엇 API 테스트"])

from pydantic import BaseModel, Field


class UserRegisterArgument(BaseModel):
    signin_id: str = Field(..., title="sigin id", regex="[^@]+@[^@]+\.[^@]+")
    password: str = Field(..., title="password")
    name: str = Field(..., title="")
    username: str = Field(..., title="")
    self_desc: str = Field(..., title="")
    phone_num: int = Field(..., title="")


@app.post("/orm-test")
async def orm_test(
    UserRegisterArgument: UserRegisterArgument, db: Session = Depends(get_db)
):
    user_dto = User(
        signin_id=UserRegisterArgument.signin_id,
        password=UserRegisterArgument.password,
        name=UserRegisterArgument.name,
        username=UserRegisterArgument.username,
        self_desc=UserRegisterArgument.self_desc,
        phone_num=UserRegisterArgument.phone_num,
    )
    db.add(user_dto)
    db.commit()
    db.refresh(user_dto)

    return user_dto


@app.get("/orm-test")
async def orm_test(db: Session = Depends(get_db)):
    query = select(User)
    return db.execute(query).scalars().all()


@app.get("/")
async def root(request: Request):
    url_list = [
        {"path": route.path, "name": route.name} for route in request.app.routes
    ]
    return url_list


# error handling
@app.exception_handler(LOLINGDBRequestFailException)
async def loling_db_request_fail_exception_handler(
    request: Request, exc: LOLINGDBRequestFailException
):
    return JSONResponse(
        status_code=400,
        content={"code": exc.response_code, "message": exc.response_message},
    )
