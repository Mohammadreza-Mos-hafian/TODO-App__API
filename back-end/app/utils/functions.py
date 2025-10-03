from typing import Dict

from sqlalchemy import select, and_
from sqlalchemy.exc import SQLAlchemyError

from app.enums import TaskStatus
from app.databases import SessionLocal
from app.models import User, Task

from markupsafe import escape

from datetime import datetime, date

import bcrypt, re, uuid


def encode(param: str):
    hash_param = bcrypt.hashpw(param.encode(), bcrypt.gensalt())
    return hash_param.decode()


def now_datatime():
    time_format = "%Y-%m-%d %H:%M:%S.%f"
    now = datetime.now().strftime(time_format)
    return datetime.strptime(now, time_format)


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


def task_status_color(number):
    colors = ["warning", "info", "success", "danger"]

    index = next((status.value for status in TaskStatus if status.value == number))

    return colors[index]


def validate_date(task_uuid, deadline):
    clean_date = str(deadline).strip().split("-")
    user_deadline = date(int(clean_date[0]), int(clean_date[1]), int(clean_date[2]))

    with SessionLocal() as session:
        try:
            stmt = (
                select(Task)
                .where(
                    Task.uuid == task_uuid,
                    Task.is_deleted == False
                )
            )

            task = session.execute(stmt).scalars().first()

            clean_task_deadline = str(task.deadline).strip().split("-")
            task_deadline = date(int(clean_task_deadline[0]), int(clean_task_deadline[1]), int(clean_task_deadline[2]))

            if user_deadline == task_deadline:
                return

            if user_deadline < date.today():
                raise ValueError(f"The deadline must be after {now_datatime().strftime('%Y-%m-%d')}.")
        except SQLAlchemyError as err:
            session.rollback()
            raise err
