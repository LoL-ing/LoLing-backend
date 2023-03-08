from enum import Enum
from typing import Any, Dict, Generic, Optional, TypeVar, Union
from pydantic.generics import GenericModel

T = TypeVar("T")


class IResponseBase(GenericModel, Generic[T]):
    message: str = ""
    meta: Dict = {}
    data: Optional[T]


class IOrderEnum(str, Enum):
    ascendent = "ascendent"
    descendent = "descendent"


DataType = TypeVar("DataType")
T = TypeVar("T")


def create_response(
    data: Optional[DataType],
    message: Optional[str] = "",
    meta: Optional[Union[Dict, Any]] = {},
) -> Union[Dict[str, DataType], DataType]:
    body_response = {"data": data, "message": message, "meta": meta}
    # It returns a dictionary to avoid doble
    # validation https://github.com/tiangolo/fastapi/issues/3021
    return {k: v for k, v in body_response.items() if v is not None}
