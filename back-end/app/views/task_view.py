from flask import request, jsonify
from flask.views import MethodView
from flask_jwt_extended import jwt_required

from sqlalchemy.exc import SQLAlchemyError

from marshmallow import ValidationError

from app.services import UserTaskService


class TaskView(MethodView):
    decorators = [jwt_required()]

    @staticmethod
    def get(task_uuid=None):
        try:
            if task_uuid:
                response = UserTaskService.get_task(task_uuid)
                return jsonify(response)

            data = {
                "page": int(request.args.get("page", 1)),
                "per_page": int(request.args.get("per_page", 5))
            }

            response = UserTaskService.show_all_tasks(data)
            return jsonify(response), 200

        except SQLAlchemyError as err:
            return jsonify({
                "status": "DB Error",
                "errors": str(err)
            }), 500

    @staticmethod
    def post():
        try:
            data = {
                "title": request.form.get("title"),
                "deadline": request.form.get("deadline"),
                "description": request.form.get("description"),
            }
            files = request.files.getlist("files[]")

            response = UserTaskService.create_task(data, files)
            return jsonify(response), 201

        except ValidationError as err:
            return jsonify({
                "status": "error",
                "errors": err.messages
            }), 400

        except SQLAlchemyError as err:
            return jsonify({
                "status": "DB Error",
                "errors": str(err)
            }), 500

    @staticmethod
    def patch(task_uuid):
        try:
            data = request.get_json()
            response = UserTaskService.edit_task(task_uuid, data)
            return jsonify(response), 200

        except ValidationError as err:
            return jsonify({
                "status": "error",
                "errors": err.messages
            }), 400

        except SQLAlchemyError as err:
            return jsonify({
                "status": "DB Error",
                "errors": str(err)
            }), 500

    @staticmethod
    def delete(task_uuid):
        try:
            response = UserTaskService.delete_task(task_uuid)
            return jsonify(response), 200

        except ValueError as err:
            return jsonify({
                "status": "error",
                "errors": str(err)
            }), 404

        except SQLAlchemyError as err:
            return jsonify({
                "status": "DB Error",
                "errors": str(err)
            }), 500
