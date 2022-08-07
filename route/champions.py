from fastapi import APIRouter, Depends, Path
from fastapi.responses import JSONResponse

from controller.champions import *

router = APIRouter()


@router.get("/champions")
def route_get_champions():
    return get_all_champions()