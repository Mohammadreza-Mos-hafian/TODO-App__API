from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from app.databases import SessionLocal
from app.models import User

import bcrypt


def check_unique_email(email: str):
    with SessionLocal() as session:
        try:
            stmt = (
                select(User).where(
                    User.email == email,
                    User.is_deleted == False
                )
            )

            if session.execute(stmt).scalar():
                raise ValueError("The email already exists.")

        except SQLAlchemyError as err:
            session.rollback()
            raise


def check_user(email: str, password: str):
    with SessionLocal() as session:
        try:
            stmt = (
                select(User)
                .where(
                    User.email == email,
                    User.is_deleted == False
                )
            )

            user: User = session.execute(stmt).scalars().first()

            if not user or not bcrypt.checkpw(password.encode(), user.password.encode()):
                raise ValueError("Email or password is incorrect.")

            return user
        except SQLAlchemyError as err:
            session.rollback()
            raise
