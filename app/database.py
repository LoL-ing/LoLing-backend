from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.common.config import settings

DB_URL = f"mysql+pymysql://{settings.RDS_USERNAME}:{settings.RDS_PASSWORD}@{settings.RDS_HOSTNAME}:{settings.RDS_PORT}"

engine = create_engine(DB_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
target_meta = Base.metadata


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
