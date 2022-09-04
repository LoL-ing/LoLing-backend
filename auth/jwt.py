from fastapi import Depends, Header
from dotenv.main import load_dotenv
import jwt
import os

load_dotenv()
secret_key = os.environ.get("SECRET_KEY")
algorithm = os.environ.get("ALGORITHM")


def auth_required(Authorization: str = Header(None, title="JWT")) -> dict:
    try:
        if not Authorization:
            raise Exception
        print("Auth", Authorization)
        token = Authorization[7:]
        decoded_token = jwt.decode(token, secret_key, algorithms=algorithm)
        print("decoded_token", decoded_token)
        return decoded_token

    except (IndexError, jwt.PyJWTError):
        raise Exception
