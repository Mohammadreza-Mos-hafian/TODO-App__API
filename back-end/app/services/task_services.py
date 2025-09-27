from marshmallow import ValidationError

from sqlalchemy.exc import SQLAlchemyError

from app.databases import SessionLocal
from app.repositories import TaskRepository
from app.schemas import CreateSchema


class TaskService:
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
    def show_all_task():
        pass

    @staticmethod
    def edit_task():
        pass

    @staticmethod
    def delete_task():
        pass
