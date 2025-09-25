from marshmallow import fields, pre_load, validate, Schema

from app.utils import clean_data


class LoginSchema(Schema):
    email = fields.Str(required=True, validate=[
        validate.Length(
            min=1,
            error="Email is required"
        ),
        validate.Regexp(
            r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$",
            error="Invalid email format."
        )
    ])
    password = fields.Str(required=True, load_only=True, validate=validate.Length(min=1, error="Password is required"))

    @pre_load
    def pre_load_data(self, data, **kwargs):
        return clean_data(data)
