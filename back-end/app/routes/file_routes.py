from flask import Blueprint

from app.views import FileView

file_bp = Blueprint("files", __name__, url_prefix="/api")

file_view = FileView.as_view("file_view")

file_bp.add_url_rule("/files", view_func=file_view, methods=["GET", "POST"])
file_bp.add_url_rule("/files/<file_uuid>", view_func=file_view, methods=["DELETE"])
file_bp.add_url_rule("/files/<file_uuid>/download", view_func=FileView().download, methods=["GET"])
