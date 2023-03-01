from ipaddress import summarize_address_range
from typing import List
from fastapi import APIRouter, Depends, Path, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from app.common.schema import IResponseBase

from app.match_history.schema import IMatchHistoriesCreate


router = APIRouter()


@router.get("/")
def get_match_history():
    return {"[GET] test match_history"}


@router.post("")
def add_match_history(
    body: IMatchHistoriesCreate,
) -> IResponseBase[IMatchHistoriesCreate]:
    pass
