from fastapi import FastAPI, Request
from route import champions, friends, profiles, profiles, users
from dotenv.main import load_dotenv
from fastapi.encoders import jsonable_encoder
from os import environ
from exception import *

app = FastAPI()
load_dotenv()

# attach routers
app.include_router(champions.router, prefix="/champions", tags=["챔피언"])
app.include_router(friends.router, prefix="/friends", tags=["친구"])
app.include_router(profiles.router, prefix="/profiles", tags=["프로필"])
app.include_router(users.router, prefix="/users", tags=["유저 등록 및 로그인"])

@app.get("/")
async def root(request: Request):
    url_list = [
        {"path": route.path, "name": route.name} for route in request.app.routes
    ]
    return url_list

# error handling








