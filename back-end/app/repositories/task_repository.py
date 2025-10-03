from sqlalchemy import select, desc, func
from sqlalchemy.exc import SQLAlchemyError

from app.databases import SessionLocal
from app.models import Task, User
from app.utils import now_datatime


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

    @staticmethod
    def get_task(task_uuid):
        with SessionLocal() as session:
            try:
                stmt = (
                    select(Task)
                    .where(
                        Task.uuid == task_uuid,
                        Task.is_deleted == False
                    )
                )

                return session.execute(stmt).scalars().first()
            except SQLAlchemyError as err:
                session.rollback()
                raise err

    @staticmethod
    def read(user_uuid: str, page: int = 1, per_page: int = 5, return_total=False):
        offset_value = (page - 1) * per_page

        with SessionLocal() as session:
            try:
                subq = (
                    select(User.id)
                    .where(
                        User.uuid == user_uuid,
                        User.is_deleted == False
                    )
                )

                stmt = (
                    select(Task)
                    .where(
                        Task.is_deleted == False,
                        Task.user_id.in_(subq)
                    )
                    .order_by(desc("created_at"))
                    .offset(offset_value)
                    .limit(per_page)
                    .distinct()
                )

                total = session.execute(
                    select(func.count(Task.id))
                    .where(
                        Task.user_id.in_(subq),
                        Task.is_deleted == False
                    )
                ).scalar() if return_total else None

                tasks = session.execute(stmt).scalars().all()

                if return_total:
                    return tasks, total

                return tasks
            except SQLAlchemyError as err:
                session.rollback()
                raise err

    @staticmethod
    def update(task_uuid: str, data):
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

                if task:
                    task.title = data["title"] if data["title"] else task.title
                    task.deadline = data["deadline"] if data["deadline"] else task.deadline
                    task.status = data["status"] if data["status"] else task.status
                    task.description = data["description"] if data["description"] else task.description

                    session.commit()
                else:
                    raise ValueError("Task not found.")

            except SQLAlchemyError as err:
                session.rollback()
                raise err

    @staticmethod
    def delete(task_uuid):
        with SessionLocal() as session:
            try:
                stmt = (
                    select(Task)
                    .where(Task.uuid == task_uuid)
                )

                task: Task = session.execute(stmt).scalars().first()

                task.is_deleted = True
                task.deleted_at = now_datatime()

                session.add(task)
                session.commit()
            except SQLAlchemyError as err:
                session.rollback()
                raise err
