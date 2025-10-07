from sqlalchemy.exc import SQLAlchemyError

from marshmallow import ValidationError

from flask import send_from_directory
from flask_jwt_extended import get_jwt_identity

from app.databases import SessionLocal
from app.repositories import TaskRepository, FileRepository, UserRepository
from app.schemas import FileSchema, UploadFileSchema
from app.utils import sanitize_filename, create_file_model, create_file_path, pagination_info, \
    save_files, create_uuid4

import os, mimetypes


class FileServices:
    @staticmethod
    def create_files(data):
        schema = UploadFileSchema()
        files, session = [], None

        if data.get("session"):
            session = data["session"]
            del data["session"]

        credentials = schema.load(data)

        try:
            task_id = (
                credentials["task_id"]
                if credentials.get("task_id")
                else TaskRepository.get_task(credentials["task_uuid"]).id
            )

            for f in credentials["files"]:
                original_name = os.path.splitext(sanitize_filename(f.filename))[0]
                file_path = create_file_path(get_jwt_identity(), credentials["task_uuid"], f.filename)

                file_model = create_file_model(file_path, original_name, create_uuid4())
                file_model.task_id = task_id

                files.append(file_model)

        except ValueError as err:
            raise ValidationError({"files": [str(err)]})

        except SQLAlchemyError as err:
            raise

        if session:
            FileRepository.create(files, session=session)
            save_files(credentials["files"], files)

            return {
                "status": "success",
                "message": "Files uploaded successfully."
            }

        with SessionLocal() as session:
            try:
                FileRepository.create(files, session=session)
                save_files(credentials["files"], files)
                session.commit()

                return {
                    "status": "success",
                    "message": "Files uploaded successfully."
                }
            except SQLAlchemyError as err:
                session.rollback()
                raise

    @staticmethod
    def show_all_files(data):
        schema = FileSchema(many=True)
        page, per_page = data["page"], data["per_page"]

        try:
            files, total = FileRepository.read(data["task_uuid"], page, per_page, True)

            resp = pagination_info(page, per_page, total)

            resp["files"] = schema.dump(files)
            resp["task_name"] = TaskRepository.get_task(task_uuid=data["task_uuid"]).title

            return resp

        except SQLAlchemyError as err:
            raise

    @staticmethod
    def delete_file(data):
        try:
            file_path = FileRepository.delete(data)

            if os.path.exists(file_path):
                os.remove(file_path)

            return {
                "status": "success",
                "message": "The file deleted successfully."
            }

        except ValueError as err:
            raise

        except SQLAlchemyError as err:
            raise

    @staticmethod
    def download_file(file_uuid):
        try:
            if not (file := FileRepository.get_file(file_uuid)):
                raise ValueError("File not found.")

            if not os.path.exists(file.file_path):
                raise ValueError("File not found.")

            if not (
                    current_user := UserRepository.get_user(
                        get_jwt_identity())) or file.task.user_id != current_user.id:
                raise ValueError("The file is not belong to you.")

            directory = os.path.dirname(file.file_path)
            filename = os.path.basename(file.file_path)

            file_ext = os.path.splitext(filename)[1]
            original_name = file.original_name + file_ext
            mime_type, _ = mimetypes.guess_type(file.file_path)

            return send_from_directory(
                directory=directory,
                path=filename,
                as_attachment=True,
                download_name=original_name,
                mimetype=mime_type or "application/octet-stream"
            )

        except SQLAlchemyError as err:
            raise
