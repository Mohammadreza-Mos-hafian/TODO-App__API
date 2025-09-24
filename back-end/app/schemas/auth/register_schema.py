from typing import Dict

from marshmallow import fields, validate, validates_schema, ValidationError, pre_load
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from markupsafe import escape

from app.models import User

import re


class RegisterSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        exclude = ("id", "created_at", "updated_at", "deleted_at")

    first_name = fields.Str(validate=validate.Length(min=3, max=32))
    last_name = fields.Str(validate=validate.Length(min=3, max=32))
    email = fields.Email(validate=validate.Length(max=64))
    password = fields.Str(required=True, load_only=True, validate=validate.Regexp(
        r"^(?=(?:.*[a-zA-Z]){8,})(?=.*\d)[a-zA-Z0-9@_\-$]+$",
        error="Use at least 8 letters with a number. Allowed symbols: (@, _, -, $)"
    ))
    confirmation_password = fields.Str(required=True, load_only=True)

    @validates_schema
    def validate_password_confirmation(self, data: Dict[str, str], **kwargs):
        if data["password"] != data["confirmation_password"]:
            raise ValidationError("Password confirmation does not match", field_name="confirmation_password")

    @pre_load
    def clean_data(self, data: Dict[str, str], **kwargs) -> Dict[str, str]:
        for key, value in data.items():
            if isinstance(data[key], str):
                data[key] = escape(re.sub(r"<.*?>", "", value))
                data[key] = re.sub(r"\s+", " ", data[key]).strip()

        data["email"] = re.sub(r"[^\w@.\-]", "", data["email"]).lower()

        return data