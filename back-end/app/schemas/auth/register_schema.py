from typing import Dict

from marshmallow import fields, validate, validates_schema, ValidationError, pre_load
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from app.models import User
from app.utils import clean_data


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
    def pre_load_data(self, data, **kwargs):
        return clean_data(data)
