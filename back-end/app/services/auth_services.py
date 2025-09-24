from marshmallow import ValidationError

from app.schemas import RegisterSchema
from app.databases import SessionLocal
from app.repositories import UserRepository
from app.utils import encode, check_unique_email


class AuthService:
    @staticmethod
    def validate_user(data):
        schema = RegisterSchema()

        try:
            user = schema.load(data, session=SessionLocal)
            unique_email = check_unique_email(user.email)

            if not unique_email:
                return {
                    "status": "error",
                    "errors": {
                        "email": ["The email already exists."]
                    }
                }
            elif isinstance(unique_email, dict):
                return unique_email

            user.password = encode(user.password)
            user_repo = UserRepository()

            return user_repo.create(user)
        except ValidationError as err:
            return {
                "status": "error",
                "errors": err.messages
            }
