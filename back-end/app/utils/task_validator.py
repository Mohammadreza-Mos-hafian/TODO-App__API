from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from app.enums import TaskStatus
from app.databases import SessionLocal
from app.models import Task
from app.utils import now_datatime

from datetime import date


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
                raise ValueError(f"Deadline must be after {now_datatime().strftime('%Y-%m-%d')}.")
        except SQLAlchemyError as err:
            session.rollback()
            raise
