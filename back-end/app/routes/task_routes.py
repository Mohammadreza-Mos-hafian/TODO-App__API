from flask import Blueprint

from app.views import TaskView

task_bp = Blueprint("tasks", __name__, url_prefix="/api")

user_task_view = TaskView.as_view("user_task_view")

task_bp.add_url_rule("/tasks", view_func=user_task_view, methods=["POST", "GET"])
task_bp.add_url_rule("/tasks/<task_uuid>", view_func=user_task_view, methods=["GET", "PATCH", "DELETE"])