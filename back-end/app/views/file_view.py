from flask import request, jsonify
from flask.views import MethodView
from flask_jwt_extended import jwt_required

from app.services import FileServices
from app.utils import error_handler


class FileView(MethodView):
    decorators = [error_handler, jwt_required()]

    def get(self, ):
        data = {
            "task_uuid": request.args.get("uuid"),
            "page": int(request.args.get("page", 1)),
            "per_page": int(request.args.get("per_page", 5)),
        }
        response = FileServices.show_all_files(data)
        return jsonify(response), 200

    def post(self):
        data = {
            "task_uuid": request.form.get("uuid"),
            "files": request.files.getlist("files[]")
        }
        response = FileServices.create_files(data)
        return jsonify(response), 201

    def delete(self, file_uuid):
        response = FileServices.delete_file(file_uuid)
        return jsonify(response), 200

    @error_handler
    @jwt_required()
    def download(self, file_uuid):
        return FileServices.download_file(file_uuid)
