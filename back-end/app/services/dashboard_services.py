from sqlalchemy.exc import SQLAlchemyError

from flask_jwt_extended import get_jwt_identity

from app.repositories import UserRepository


class DashboardService:
    @staticmethod
    def get_user_name():
        try:
            data = UserRepository.get_user(get_jwt_identity())
            return {
                "status": "success",
                "full_name": f"{data.first_name} {data.last_name}"
            }
        except SQLAlchemyError as err:
            raise
