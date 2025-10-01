from flask_jwt_extended import get_jwt_identity

from marshmallow import ValidationError

from sqlalchemy.exc import SQLAlchemyError

from app.databases import SessionLocal
from app.repositories import TaskRepository
from app.schemas import CreateSchema, TaskSchema
from app.utils import show_task_status


class UserTaskService:
    @staticmethod
    def create_task(data):
        schema = CreateSchema()

        try:
            credentials = schema.load(data, session=SessionLocal)
            task = TaskRepository.create(credentials)

            return {
                "status": "success",
                "task": task
            }
        except ValidationError as err:
            return {
                "status": "error",
                "errors": err.messages
            }
        except SQLAlchemyError as err:
            return {
                "status": "DB Error",
                "errors": str(err)
            }

    @staticmethod
    def show_all_tasks(data):
        schema = TaskSchema(many=True)
        page, per_page = data["page"], data["per_page"]

        try:
            tasks, total = TaskRepository.read(get_jwt_identity(), page, per_page, True)

            total_pages = (total + per_page - 1) // per_page
            next_page = page + 1 if page < total_pages else None
            prev_page = page - 1 if page > 1 else None

            return {
                "status": "success",
                "page": page,
                "per_page": per_page,
                "total": total,
                "total_pages": total_pages,
                "next_page": next_page,
                "prev_page": prev_page,
                "tasks": schema.dump(tasks)
            }
        except SQLAlchemyError as err:
            return {
                "status": "error",
                "errors": str(err)
            }

    @staticmethod
    def edit_task():
        pass

    @staticmethod
    def delete_task():
        pass
