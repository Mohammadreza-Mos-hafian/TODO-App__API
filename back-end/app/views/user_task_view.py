from flask import request, jsonify
from flask.views import MethodView
from flask_jwt_extended import jwt_required

from app.services import UserTaskService


class UserTaskView(MethodView):
    decorators = [jwt_required()]

    @staticmethod
    def get():
        data = {
            "page": int(request.args.get("page", 1)),
            "per_page": int(request.args.get("per_page", 5))
        }
        response = UserTaskService.show_all_tasks(data)
        return jsonify(response)

    @staticmethod
    def post():
        data = request.get_json()
        response = UserTaskService.create_task(data)
        return jsonify(response)

    @staticmethod
    def put():
        pass

    @staticmethod
    def delete():
        pass
