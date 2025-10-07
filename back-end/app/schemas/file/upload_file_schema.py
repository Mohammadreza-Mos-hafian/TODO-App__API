from marshmallow import Schema, fields, validates
from app.utils import FileField


class UploadFileSchema(Schema):
    task_id = fields.Str(required=False)
    task_uuid = fields.Str(required=False)
    files = fields.List(FileField(), required=True)
