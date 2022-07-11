from fastapi import FastAPI, Request
from controller import get_friends, get_all_champions, get_all_profiles, get_lol_account
from dotenv.main import load_dotenv
from os import environ

from db_connection.rds import get_rds_db_connection
# from db_connection.rds.insert_dummy import insert_friends, delete_friends
app = FastAPI()
load_dotenv()

@app.get("/")
async def root(request:Request):
    url_list = [
        {'path': route.path, 'name': route.name}
        for route in request.app.routes
    ]
    return url_list

@app.get("/friends")
def route_get_friends():
    return get_friends()

@app.get("/lol_account")
def route_get_lol_account():
    return get_lol_account()

@app.get("/profiles")
def route_get_profiles():
    return get_all_profiles()

@app.get("/champions")
def route_get_champions():
    return get_all_champions()
