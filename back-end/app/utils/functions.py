from typing import Dict

from sqlalchemy import select, and_
from sqlalchemy.exc import SQLAlchemyError

from app.databases import SessionLocal
from app.models import User

from markupsafe import escape

import bcrypt, re


def encode(param: str):
    hash_param = bcrypt.hashpw(param.encode(), bcrypt.gensalt())
    return hash_param.decode()


def check_unique_email(email: str) -> bool | dict[str, str]:
    with SessionLocal() as session:
        try:
            stmt = (
                select(User).where(and_(
                    User.email == email,
                    User.is_deleted == False,
                ))
            )

            return False if session.execute(stmt).first() else True
        except SQLAlchemyError as err:
            session.rollback()

            return {
                "status": "DB Error",
                "errors": str(err)
            }


def clean_data(data: Dict[str, str]) -> Dict[str, str]:
    for key, value in data.items():
        if isinstance(data[key], str):
            data[key] = escape(re.sub(r"<.*?>", "", value))
            data[key] = re.sub(r"\s+", " ", data[key]).strip()
    data["email"] = re.sub(r"[^\w@.\-]", "", data["email"]).lower()
    return data
