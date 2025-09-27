from marshmallow import ValidationError

from sqlalchemy.exc import SQLAlchemyError

from app.schemas import RegisterSchema, LoginSchema
from app.databases import SessionLocal
from app.repositories import UserRepository
from app.utils import encode, check_unique_email, check_user
from app.services.jwt_services import JWTService


class AuthService:
    @staticmethod
    def register_user(data):
        schema = RegisterSchema()

        try:
            credentials = schema.load(data, session=SessionLocal)
            check_unique_email(credentials.email)

            credentials.password = encode(credentials.password)
            user = UserRepository.create(credentials)

            return {
                "status": "success",
                "access_token": JWTService.create_access_token(str(user.uuid)),
                "refresh_token": JWTService.create_refresh_token(str(user.uuid))
            }
        except ValidationError as err:
            return {
                "status": "error",
                "errors": err.messages
            }
        except SQLAlchemyError as err:
            return {
                "status": "DB Error",
                "errors": str(err)
            }
        except ValueError as err:
            return {
                "status": "Auth Error",
                "errors": str(err)
            }

    @staticmethod
    def login_user(data):
        schema = LoginSchema()

        try:
            credentials = schema.load(data)
            current_user = check_user(credentials["email"], credentials["password"])

            return {
                "status": "success",
                "access_token": JWTService.create_access_token(str(current_user.uuid)),
                "refresh_token": JWTService.create_refresh_token(str(current_user.uuid)),
            }

        except ValidationError as err:
            return {
                "status": "error",
                "errors": err.messages
            }
        except SQLAlchemyError as err:
            return {
                "status": "DB Error",
                "errors": str(err)
            }
        except ValueError as err:
            return {
                "status": "Auth Error",
                "errors": str(err)
            }
