from flask import jsonify, request
from flask.views import MethodView
from flask_jwt_extended import jwt_required

from app.services import DashboardService


class DashboardView(MethodView):
    @jwt_required()
    def get(self):
        response = DashboardService.get_user_name()
        return jsonify(response)
