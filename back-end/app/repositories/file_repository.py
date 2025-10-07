from typing import List

from sqlalchemy import select, desc, func
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import SQLAlchemyError

from app.databases import SessionLocal
from app.models import Task, File
from app.utils import now_datatime


class FileRepository:
    @staticmethod
    def create(files: List[File], session: SessionLocal):
        session.add_all(files)

    @staticmethod
    def read(task_uuid, page: int = 1, per_page: int = 5, return_total=False):
        offset_value = (page - 1) * per_page

        with SessionLocal() as session:
            try:
                subq = (
                    select(Task.id)
                    .where(
                        Task.uuid == task_uuid,
                        Task.is_deleted == False
                    )
                )

                total = session.execute(
                    select(func.count(File.id))
                    .where(
                        File.is_deleted == False,
                        File.task_id.in_(subq)
                    )
                ).scalar() if return_total else None

                stmt = (
                    select(File)
                    .where(
                        File.task_id.in_(subq),
                        File.is_deleted == False
                    )
                    .offset(offset_value)
                    .limit(per_page)
                    .order_by(desc("created_at"))
                )

                files = session.execute(stmt).scalars().all()

                if return_total:
                    return files, total

                return files
            except SQLAlchemyError as err:
                session.rollback()
                raise

    @staticmethod
    def delete(file_uuid):
        with SessionLocal() as session:
            try:
                stmt = (
                    select(File)
                    .where(File.uuid == file_uuid)
                )

                file: File = session.execute(stmt).scalars().first()

                if file:
                    file.is_deleted = True
                    file.deleted_at = now_datatime()

                    session.commit()

                    return file.file_path
                else:
                    raise ValueError("File not found.")
            except SQLAlchemyError as err:
                session.rollback()
                raise

    @staticmethod
    def get_file(file_uuid):
        with SessionLocal() as session:
            try:
                stmt = (
                    select(File)
                    .options(joinedload(File.task))
                    .where(
                        File.uuid == file_uuid,
                        File.is_deleted == False
                    )
                )

                return session.execute(stmt).scalars().first()

            except SQLAlchemyError as err:
                raise
