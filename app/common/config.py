import os
from pydantic import BaseSettings, PostgresDsn, validator, EmailStr, AnyHttpUrl
from typing import Optional, Dict, Any, Union, List
import secrets


class Settings(BaseSettings):
    APP_ENV: str
    RDS_HOSTNAME: str
    RDS_PORT: str
    RDS_DB_NAME: str
    RDS_USERNAME: str
    RDS_PASSWORD: str

    MONGO_USERNAME: str
    MONGO_PASSWORD: str
    RIOT_AP_ID: str
    RIOT_API_URL_KR: str

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 1  # 1 hour
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 100  # 100 days

    RIOT_API_KEY: str

    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_FROM_NAME: str

    class Config:
        case_sensitive = True
        env_file = os.path.abspath(os.getcwd()) + "/.env"


settings = Settings()
