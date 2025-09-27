from marshmallow import validate, pre_load, fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from flask_jwt_extended import get_jwt_identity

from app.models import Task
from app.utils import clean_data, create_uuid4
from app.repositories import UserRepository


class CreateSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Task
        load_instance = True
        include_fk = True
        exclude = ("id", "created_at", "updated_at", "deleted_at")

    title = fields.Str(required=True,
                       validate=validate.Length(min=1, max=32, error="The title must be between 1 and 32 characters."))
    deadline = fields.Date(required=True, allow_none=False)
    description = fields.Str(validate=validate.Length(max=500))

    @pre_load
    def pre_load_data(self, data, **kwargs):
        data["uuid"] = create_uuid4()
        data["user_id"] = UserRepository.get_user(get_jwt_identity()).id
        return clean_data(data)
