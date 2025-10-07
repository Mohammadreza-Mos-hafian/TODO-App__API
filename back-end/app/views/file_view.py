from flask import request, jsonify
from flask.views import MethodView
from flask_jwt_extended import jwt_required

from sqlalchemy.exc import SQLAlchemyError

from marshmallow import ValidationError

from app.services import FileServices


class FileView(MethodView):
    decorators = [jwt_required()]

    @staticmethod
    def get():
        try:
            data = {
                "task_uuid": request.args.get("uuid"),
                "page": int(request.args.get("page", 1)),
                "per_page": int(request.args.get("per_page", 5)),
            }
            response = FileServices.show_all_files(data)
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
                "task_uuid": request.form.get("uuid"),
                "files": request.files.getlist("files[]")
            }
            response = FileServices.create_files(data)
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
    def delete(file_uuid):
        try:
            response = FileServices.delete_file(file_uuid)
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

    @staticmethod
    @jwt_required()
    def download(file_uuid):
        try:
            return FileServices.download_file(file_uuid)

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
