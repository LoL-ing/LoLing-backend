import datetime
from typing import Union
from pydantic import BaseModel

from app.users.model import UsersBase
from app.common.model import BaseLolProfile


class IUserCreate(UsersBase):
    pass


class IUserUpdate(UsersBase):
    pass


class ILolProfilesCreate(BaseLolProfile):
    pass


class ILolProfilesUpdate(BaseLolProfile):
    pass
