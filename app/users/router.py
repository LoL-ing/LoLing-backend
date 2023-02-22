from ipaddress import summarize_address_range
from typing import List
from fastapi import APIRouter, Depends, Path, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse


router = APIRouter()


@router.get("/")
def get_user():
    return {"[GET] test user"}
