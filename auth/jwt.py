from fastapi import Depends, Header
from dotenv.main import load_dotenv
import jwt
import os

load_dotenv()
secret_key = os.environ.get("SECRET_KEY")
algorithm = os.environ.get("ALGORITHM")


def auth_required(Authorization: str = Header(None, title="JWT")) -> str:
    try:
        if not Authorization:
            raise Exception

        token = Authorization[7:]
        decoded_token = jwt.decode(token, secret_key, algorithms=algorithm)

        return decoded_token.get("identity")

    except (IndexError, jwt.PyJWTError):
        raise Exception
