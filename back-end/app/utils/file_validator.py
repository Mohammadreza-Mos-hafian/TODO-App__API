from typing import List

from flask import current_app

from marshmallow import fields, ValidationError

from werkzeug.datastructures import FileStorage

from PIL import Image

from pathlib import Path

from app.models import File

import magic, uuid, os, re


def _validate_file_type(file):
    allowed_types = ["application/pdf", "image/jpeg", "image/png", "image/jpg"]

    mime_type = magic.from_buffer(file.read(2048), mime=True)
    file.seek(0)

    if mime_type not in allowed_types:
        raise ValueError("The file format is not allowed (jpg, jpeg, png, pdf).")


def _validate_file_size(file):
    max_size = current_app.config["MAX_CONTENT_LENGTH"]

    file.seek(0, 2)
    size = file.tell()
    file.seek(0)

    if size > max_size:
        raise ValueError(f"The file size exceeds the limit (max: {max_size / (1024 ** 2)}MB).")


def _validate_image(file):
    try:
        img = Image.open(file)
        img.verify()
        file.seek(0)
    except Exception:
        raise ValueError("The file is not valid (the image is not real).")


def sanitize_filename(filename):
    return re.sub(r'[\\/:"*?<>|]+', "", filename)


def _create_filename(file_name):
    return f"{uuid.uuid4().hex}_{file_name}"


def validated_file(file):
    _validate_file_type(file)
    _validate_file_size(file)

    if file.mimetype.startswith("image/"):
        _validate_image(file)


def create_file_path(user_uuid: str, task_uuid: str, filename: str) -> str:
    file_folder = str(
        Path(current_app.config["UPLOAD_FOLDER"]) / f"user_{user_uuid.strip()}" / f"task_{task_uuid.strip()}"
    )
    filename = _create_filename(sanitize_filename(filename))
    os.makedirs(file_folder, exist_ok=True)

    return os.path.join(file_folder, filename)


def create_file_model(file_path: str, original_name: str, file_uuid: uuid.UUID):
    return File(
        file_path=file_path,
        original_name=original_name,
        uuid=file_uuid
    )


def save_files(credentials: List[FileStorage], files: List[File]):
    for i in range(len(credentials)):
        credentials[i].save(files[i].file_path)


class FileField(fields.Field):
    def _deserialize(self, value, attr, data, **kwargs):
        if value is None:
            return None

        if not isinstance(value, FileStorage):
            raise ValidationError("Invalid file.")

        if value.filename == "":
            raise ValidationError("No file selected.")

        if len(value.filename) > 64:
            raise ValidationError(f"Filename is too long (max {current_app.config['MAX_ORIG']} character).")

        try:
            validated_file(value)
        except ValueError as err:
            raise ValidationError(str(err))

        return value
