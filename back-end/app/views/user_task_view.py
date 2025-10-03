from flask import request, jsonify
from flask.views import MethodView
from flask_jwt_extended import jwt_required

from app.services import UserTaskService


class UserTaskView(MethodView):
    decorators = [jwt_required()]

    @staticmethod
    def get(task_uuid=None):
        if task_uuid:
            response = UserTaskService.get_task(task_uuid)
            return jsonify(response)

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
    def patch(task_uuid):
        data = request.get_json()
        response = UserTaskService.edit_task(task_uuid, data)
        return jsonify(response)

    @staticmethod
    def delete(task_uuid):
        response = UserTaskService.delete_task(task_uuid)
        return jsonify(response)
