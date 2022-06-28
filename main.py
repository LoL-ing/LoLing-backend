from fastapi import FastAPI
from controller import get_friends, get_all_champions, get_all_profiles
from dotenv.main import load_dotenv
from os import environ
from db_connection.rds import exec_fetch_query, get_rds_db_connection, close_rds_db_connection

app = FastAPI()
load_dotenv()

@app.get("/")
async def root():
    return {"config": environ.get("RDS_HOSTNAME")}

@app.get("/Friends")
def route_get_friends():
    return get_friends()

@app.get("/Profiles")
def route_get_profiles():
    return get_all_profiles()

@app.get("/Champions")
def route_get_champions():
    return get_all_champions()
