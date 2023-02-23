from enum import Enum
from typing import Dict, Generic, Optional, TypeVar
from pydantic.generics import GenericModel

T = TypeVar("T")


class IResponseBase(GenericModel, Generic[T]):
    message: str = ""
    meta: Dict = {}
    data: Optional[T]


class IOrderEnum(str, Enum):
    ascendent = "ascendent"
    descendent = "descendent"
