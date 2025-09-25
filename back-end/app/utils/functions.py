import uuid
from typing import Dict

from sqlalchemy import select, and_
from sqlalchemy.exc import SQLAlchemyError

from app.databases import SessionLocal
from app.models import User

from markupsafe import escape

from datetime import datetime, timezone

import bcrypt, re


def encode(param: str):
    hash_param = bcrypt.hashpw(param.encode(), bcrypt.gensalt())
    return hash_param.decode()


def now_utc():
    return datetime.now(timezone.utc)


def create_uuid4() -> str:
    return str(uuid.uuid4())


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
            raise err


def check_user(email: str, password: str):
    with SessionLocal() as session:
        try:
            stmt = (
                select(User)
                .where(and_(
                    User.email == email,
                    User.is_deleted == False
                ))
            )

            user: User = session.execute(stmt).scalars().first()

            if not user or not bcrypt.checkpw(password.encode(), user.password.encode()):
                raise ValueError("Email or password is incorrect.")

            return user
        except SQLAlchemyError as err:
            session.rollback()
            raise err


def clean_data(data: Dict[str, str]) -> Dict[str, str]:
    for key, value in data.items():
        if isinstance(data[key], str):
            data[key] = escape(re.sub(r"<.*?>", "", value))
            data[key] = re.sub(r"\s+", " ", data[key]).strip()

    return data
