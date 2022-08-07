from fastapi import APIRouter, Depends, Path
from fastapi.responses import JSONResponse

from controller.friends import *

router = APIRouter()

@router.get("/friends")
def route_get_friends():
    return get_friends()