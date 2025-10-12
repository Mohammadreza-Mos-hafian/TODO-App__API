from flask import request, jsonify
from flask.views import MethodView
from flask_jwt_extended import jwt_required

from app.services import TaskService
from app.utils import error_handler


class TaskView(MethodView):
    decorators = [error_handler, jwt_required()]

    def get(self, task_uuid=None):
        if task_uuid:
            response = TaskService.get_task(task_uuid)
            return jsonify(response)

        data = {
            "page": int(request.args.get("page", 1)),
            "per_page": int(request.args.get("per_page", 5))
        }

        response = TaskService.show_all_tasks(data)
        return jsonify(response), 200

    def post(self):
        data = {
            "title": request.form.get("title"),
            "deadline": request.form.get("deadline"),
            "description": request.form.get("description"),
        }
        files = request.files.getlist("files[]")

        response = TaskService.create_task(data, files)
        return jsonify(response), 201

    def patch(self, task_uuid):
        data = request.get_json()
        response = TaskService.edit_task(task_uuid, data)
        return jsonify(response), 200

    def delete(self, task_uuid):
        response = TaskService.delete_task(task_uuid)
        return jsonify(response), 200
