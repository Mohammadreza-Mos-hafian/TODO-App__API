from marshmallow import Schema, fields, validate, pre_load, validates, ValidationError

from app.utils import clean_data


class EditSchema(Schema):
    title = fields.Str(validate=validate.Length(min=1, max=32, error="The title must be between 1 and 32 characters."))
    deadline = fields.Date(allow_none=False)
    status = fields.Str(required=True)
    description = fields.Str(validate=validate.Length(max=500))

    @validates("status")
    def validate_status(self, value, **kwargs):
        if value in (None, ""):
            raise ValidationError("Status is required.", field_name="status")
        try:
            int_value = int(value)
        except ValueError:
            raise ValidationError("Status must be a number.", field_name="status")

        if int(value) not in range(0, 4):
            raise ValidationError("Invalid status.", field_name="status")

    @pre_load
    def pre_load_data(self, data, **kwargs):
        return clean_data(data)
