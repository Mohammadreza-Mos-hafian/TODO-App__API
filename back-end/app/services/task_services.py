from flask_jwt_extended import get_jwt_identity

from marshmallow import ValidationError

from sqlalchemy.exc import SQLAlchemyError

from pathlib import Path

from app.databases import SessionLocal
from app.repositories import TaskRepository
from app.services.file_services import FileServices
from app.schemas import CreateSchema, TaskSchema, EditSchema, UploadFileSchema
from app.utils import validate_date, pagination_info

import os, shutil


class UserTaskService:
    @staticmethod
    def create_task(data, files=None):
        task_schema = CreateSchema()

        try:
            task_data = task_schema.load(data, session=SessionLocal)
        except ValidationError as err:
            raise

        try:
            if files and len(files) > 0:
                file_schema = UploadFileSchema()
                file_data = {
                    "files": files,
                    "task_uuid": "temp_uuid"
                }
                file_schema.load(file_data)
        except ValidationError as err:
            raise

        with SessionLocal() as session:
            try:
                task_uuid, task_id = TaskRepository.create(task_data, session)

                if files and len(files) > 0:
                    FileServices.create_files({
                        "files": files,
                        "task_uuid": str(task_uuid),
                        "task_id": str(task_id),
                        "session": session
                    })

                session.commit()

                return {
                    "status": "success",
                    "message": {
                        "task": "Task created successfully.",
                        "file": "Files created successfully." if files else None
                    }
                }

            except SQLAlchemyError as err:
                session.rollback()
                raise

    @staticmethod
    def get_task(data: str):
        schema = TaskSchema()
        try:
            task = TaskRepository.get_task(task_uuid=data)

            if not task:
                return {
                    "status": "error",
                    "errors": "Task not found."
                }

            return schema.dump(task)
        except SQLAlchemyError as err:
            raise

    @staticmethod
    def show_all_tasks(data):
        schema = TaskSchema(many=True)
        page, per_page = data["page"], data["per_page"]

        try:
            tasks, total = TaskRepository.read(get_jwt_identity(), page, per_page, True)

            resp = pagination_info(page, per_page, total)

            resp["tasks"] = schema.dump(tasks)

            return resp

        except SQLAlchemyError as err:
            raise

    @staticmethod
    def edit_task(task_uuid, data):
        schema = EditSchema()

        try:
            credentials = schema.load(data)

            if credentials.get("deadline"):
                validate_date(task_uuid, credentials["deadline"])

            TaskRepository.update(task_uuid, data)

            return {
                "status": "success",
                "message": "Task edited successfully."
            }

        except ValueError as err:
            raise ValidationError({"deadline": [str(err)]})

        except SQLAlchemyError as err:
            raise

    @staticmethod
    def delete_task(data):
        try:
            files_path = TaskRepository.delete(data)
            path = Path(files_path).parent

            if os.path.exists(path):
                shutil.rmtree(path)

            return {
                "status": "success",
                "message": "The task deleted successfully."
            }

        except ValueError as err:
            raise

        except SQLAlchemyError as err:
            raise
