from fastapi import HTTPException
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from uuid import UUID
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlmodel import SQLModel, select, func
from sqlmodel.sql.expression import Select
from sqlalchemy import exc

ModelType = TypeVar("ModelType", bound=SQLModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
SchemaType = TypeVar("SchemaType", bound=BaseModel)
T = TypeVar("T", bound=SQLModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        **Parameters**
        * `model`: A SQLModel model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    def get(self, *, id: Union[UUID, str], db_session=None) -> Optional[ModelType]:
        db_session = db_session
        query = select(self.model).where(self.model.id == id)
        response = db_session.execute(query)
        return response.scalar_one_or_none()

    def get_by_ids(
        self,
        *,
        list_ids: List[Union[UUID, str]],
        db_session=None,
    ) -> Optional[List[ModelType]]:
        db_session = db_session
        response = db_session.execute(
            select(self.model).where(self.model.id.in_(list_ids))
        )
        return response.scalars().all()

    def get_count(self, db_session=None) -> Optional[ModelType]:
        db_session = db_session
        response = db_session.execute(
            select(func.count()).select_from(select(self.model).subquery())
        )
        return response.scalar_one()

    def get_multi(
        self,
        *,
        skip: int = 0,
        limit: int = 100,
        query: Optional[Union[T, Select[T]]] = None,
        db_session=None,
    ) -> List[ModelType]:
        db_session = db_session
        if query is None:
            query = select(self.model).offset(skip).limit(limit).order_by(self.model.id)
        response = db_session.execute(query)
        return response.scalars().all()

    def create(
        self,
        *,
        obj_in: Union[CreateSchemaType, ModelType],
        created_by_id: Optional[Union[UUID, str]] = None,
        db_session=None,
    ) -> ModelType:
        db_session = db_session
        db_obj = self.model.from_orm(obj_in)  # type: ignore

        if created_by_id:
            db_obj.created_by_id = created_by_id

        try:
            db_session.add(db_obj)
            db_session.commit()
        except exc.IntegrityError:
            db_session.rollback()
            raise HTTPException(
                status_code=409,
                detail="Resource already exists",
            )
        # db_session.refresh(db_obj)
        return db_obj

    def create_multiple(
        self,
        *,
        obj_in_list: List[Union[CreateSchemaType, ModelType]],
        created_by_id: Optional[Union[UUID, str]] = None,
        db_session=None,
    ) -> ModelType:
        db_session = db_session

        db_obj_list = []

        for obj_in in obj_in_list:
            db_obj = self.model.from_orm(obj_in)

            if created_by_id:
                db_obj.created_by_id = created_by_id

            db_obj_list.append(db_obj)

        try:
            db_session.add_all(db_obj_list)
            db_session.commit()
        except exc.IntegrityError:
            db_session.rollback()
            raise HTTPException(
                status_code=409,
                detail="Resource already exists",
            )
        # refresh 의 역할?
        # db_session.refresh(db_obj)
        return db_obj

    def update(
        self,
        *,
        obj_current: ModelType,
        obj_new: Union[UpdateSchemaType, Dict[str, Any], ModelType],
        db_session=None,
    ) -> ModelType:
        db_session = db_session
        obj_data = jsonable_encoder(obj_current)

        if isinstance(obj_new, dict):
            update_data = obj_new
        else:
            update_data = obj_new.dict(
                exclude_unset=True
            )  # This tells Pydantic to not include the values that were not sent
        for field in obj_data:
            if field in update_data:
                setattr(obj_current, field, update_data[field])

        db_session.add(obj_current)
        db_session.commit()
        db_session.refresh(obj_current)
        return obj_current

    def remove(self, *, id: Union[UUID, str], db_session=None) -> ModelType:
        db_session = db_session
        response = db_session.execute(select(self.model).where(self.model.id == id))
        obj = response.scalar_one()
        db_session.delete(obj)
        db_session.commit()
        return obj
