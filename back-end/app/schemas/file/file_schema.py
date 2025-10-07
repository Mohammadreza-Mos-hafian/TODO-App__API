from marshmallow import post_dump
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from app.models import File


class FileSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = File
        load_instance = True
        exclude = ("id", "file_path", "is_deleted", "created_at", "updated_at", "deleted_at")
