from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from app.databases import SessionLocal
from app.models import Task


class TaskRepository:
    @staticmethod
    def create(task: Task):
        with SessionLocal() as session:
            try:
                session.add(task)
                session.commit()
                session.refresh(task)

                return task.uuid
            except SQLAlchemyError as err:
                session.rollback()
                raise err
