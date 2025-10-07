from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from app.databases import SessionLocal
from app.models import User


class UserRepository:
    @staticmethod
    def create(user: User) -> User:
        with SessionLocal() as session:
            try:
                session.add(user)
                session.commit()
                session.refresh(user)

                return user
            except SQLAlchemyError as err:
                session.rollback()
                raise

    @staticmethod
    def get_user(user_uuid: str):
        with SessionLocal() as session:
            try:
                stmt = (
                    select(User)
                    .where(
                        User.uuid == user_uuid,
                        User.is_deleted == False
                    )
                )

                return session.execute(stmt).scalars().first()
            except SQLAlchemyError as err:
                raise
