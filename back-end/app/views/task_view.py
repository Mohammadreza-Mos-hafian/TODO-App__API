from flask import request
from flask.views import MethodView
from flask_jwt_extended import jwt_required

from app.services import TaskService


class TaskView(MethodView):
    decorators = [jwt_required()]

    @staticmethod
    def get(uuid: str):
        pass

    @staticmethod
    def post():
        data = request.get_json()
        response = TaskService.create_task(data)
        return response

    @staticmethod
    def put(uuid: str):
        pass

    @staticmethod
    def delete(uuid: str):
        pass
