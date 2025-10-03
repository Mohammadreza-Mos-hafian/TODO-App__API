from flask_jwt_extended import get_jwt_identity

from marshmallow import ValidationError

from sqlalchemy.exc import SQLAlchemyError

from app.databases import SessionLocal
from app.repositories import TaskRepository
from app.schemas import CreateSchema, TaskSchema, EditSchema
from app.utils import validate_date


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
    def get_task(data: str):
        schema = TaskSchema()
        try:
            task = TaskRepository.get_task(data)

            if not task:
                return {
                    "status": "error",
                    "errors": "Task not found."
                }

            return schema.dump(task)
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
                "status": "DB Error",
                "errors": str(err)
            }

    @staticmethod
    def edit_task(task_uuid, data):
        schema = EditSchema()

        try:
            credentials = schema.load(data)

            if "deadline" in credentials.keys():
                validate_date(task_uuid, credentials["deadline"])

            TaskRepository.update(task_uuid, data)

            return {
                "status": "success",
                "message": "Task edited successfully."
            }

        except ValidationError as err:
            return {
                "status": "error",
                "errors": err.messages
            }
        except ValueError as err:
            return {
                "status": "error",
                "errors": {
                    "deadline": [str(err)]
                }
            }
        except SQLAlchemyError as err:
            return {
                "status": "DB Error",
                "errors": str(err)
            }

    @staticmethod
    def delete_task(data):
        try:
            TaskRepository.delete(data)

            return {
                "status": "success",
                "message": "The task deleted successfully."
            }
        except SQLAlchemyError as err:
            return {
                "status": "error",
                "errors": str(err)
            }
