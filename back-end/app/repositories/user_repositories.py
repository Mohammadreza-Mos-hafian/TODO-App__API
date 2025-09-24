from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from app.databases import SessionLocal
from app.models import User


class UserRepository:
    def __init__(self):
        self.session = SessionLocal

    def create(self, user: User):
        with self.session() as session:
            try:
                session.add(user)
                session.commit()
                return {
                    "status": "success",
                    "message": "User registration was successful.",
                }
            except SQLAlchemyError as err:
                session.rollback()

                return {
                    "status": "DB Error",
                    "errors": str(err)
                }
