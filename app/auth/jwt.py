from fastapi import Depends, Header
from dotenv.main import load_dotenv
import jwt
import os

from app.common.config import settings


def auth_required(Authorization: str = Header(None, title="JWT")) -> dict:
    try:
        if not Authorization:
            raise Exception

        print("Auth", Authorization)

        token = Authorization[7:]
        decoded_token = jwt.decode(
            token, settings.SECRET_KEY, algorithms=settings.ALGORITHM
        )

        print("decoded_token", decoded_token)

        return decoded_token

    except (IndexError, jwt.PyJWTError):
        raise Exception
