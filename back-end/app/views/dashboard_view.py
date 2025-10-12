from flask import jsonify, request
from flask.views import MethodView
from flask_jwt_extended import jwt_required

from app.services import DashboardService
from app.utils import error_handler


class DashboardView(MethodView):
    decorators = [error_handler, jwt_required()]

    def get(self):
        response = DashboardService.get_user_name()
        return jsonify(response), 200
