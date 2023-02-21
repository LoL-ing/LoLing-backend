from sqlalchemy import (
    VARCHAR,
    Column,
    String,
    Date,
    Integer,
    DateTime,
)
from db_connection.rds.orm import Base
from sqlalchemy.sql import func


class BaseIdModel(Base):
    id = Column(Integer, nullable=False, primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    __abstract__ = True
