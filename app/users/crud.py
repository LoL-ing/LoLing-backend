from fastapi import HTTPException

from sqlalchemy import select
from app.users.schema import IUserCreate, IResUserGet
from requests import Session

from app.users.model import Users


class UserCRUD:
    def get(self, signin_id: str, db_session: Session) -> IResUserGet:
        query = select(Users).where(Users.signin_id == signin_id)
        response = db_session.execute(query)
        return response.scalar_one_or_none()

    def create(self, IUserCreate: IUserCreate, db_session: Session):
        user = Users(
            signin_id=IUserCreate.signin_id,
            hashed_password=IUserCreate.password,
            password=IUserCreate.password,
            name=IUserCreate.name,
            username=IUserCreate.username,
            self_desc=IUserCreate.self_desc,
            phone_num=IUserCreate.phone_num,
        )

        try:
            db_session.add(user)
            db_session.commit()
        except Exception as E:
            db_session.rollback()
            raise E
            raise HTTPException(
                status_code=409,
                detail="Resource already exists",
            )
        db_session.refresh(user)
        return user
