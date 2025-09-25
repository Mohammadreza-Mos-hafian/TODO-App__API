from typing import Dict

from marshmallow import fields, validate, validates_schema, ValidationError, pre_load
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from app.models import User
from app.utils import clean_data, create_uuid4


class RegisterSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        exclude = ("id", "created_at", "updated_at", "deleted_at")

    first_name = fields.Str(required=True, validate=validate.Length(min=1, max=32,
                                                                    error="The first name must be between 1 and 32 characters."))
    last_name = fields.Str(required=True, validate=validate.Length(min=1, max=32,
                                                                   error="The last name must be between 1 and 32 characters."))
    email = fields.Str(required=True, validate=[
        validate.Length(
            min=1,
            max=64,
            error="The email must be between 1 and 64 characters."
        ),
        validate.Regexp(
            r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$",
            error="Invalid email format."
        )
    ])
    password = fields.Str(required=True, load_only=True, validate=[
        validate.Length(
            min=1,
            max=255,
            error="The password must be between 1 and 255 characters."
        ),
        validate.Regexp(
            r"^(?=(?:.*[a-zA-Z]){8,})(?=.*\d)[a-zA-Z0-9@_\-$]+$",
            error="Use at least 8 letters with a number. Allowed symbols: (@, _, -, $)"
        )
    ])
    confirmation_password = fields.Str(required=True, load_only=True,
                                       validate=validate.Length(min=1, error="Field is required."))

    @validates_schema
    def validate_password_confirmation(self, data: Dict[str, str], **kwargs):
        if data["password"] != data["confirmation_password"]:
            raise ValidationError("Password confirmation does not match", field_name="confirmation_password")

    @pre_load
    def pre_load_data(self, data, **kwargs):
        data["uuid"] = create_uuid4()
        return clean_data(data)
