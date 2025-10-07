from flask import jsonify, request
from flask.views import MethodView
from flask_jwt_extended import jwt_required

from sqlalchemy.exc import SQLAlchemyError

from app.services import DashboardService


class DashboardView(MethodView):
    @jwt_required()
    def get(self):
        try:
            response = DashboardService.get_user_name()
            return jsonify(response), 200

        except SQLAlchemyError as err:
            return jsonify({
                "status": "DB Error",
                "errors": str(err)
            }), 500
