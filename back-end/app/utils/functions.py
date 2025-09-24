from sqlalchemy import select, and_
from sqlalchemy.exc import SQLAlchemyError

from app.databases import SessionLocal
from app.models import User

import bcrypt


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
