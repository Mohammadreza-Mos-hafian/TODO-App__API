from flask import request, jsonify
from flask.views import MethodView
from flask_jwt_extended import jwt_required

from app.services import TaskService


class TaskView(MethodView):
    decorators = [jwt_required()]

    @staticmethod
    def get(user_uuid: str):
        pass

    @staticmethod
    def post():
        data = request.get_json()
        response = TaskService.create_task(data)
        return jsonify(response)

    @staticmethod
    def put(user_uuid: str):
        pass

    @staticmethod
    def delete(user_uuid: str):
        pass
