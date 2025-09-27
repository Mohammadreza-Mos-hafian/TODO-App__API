from flask import Blueprint

from app.views import TaskView

task_bp = Blueprint("tasks", __name__, url_prefix="/api/tasks")

task_view = TaskView.as_view("task_view")

task_bp.add_url_rule("/", view_func=task_view, methods=["POST"])
task_bp.add_url_rule("/<string:uuid>", view_func=task_view, methods=["GET", "PUT", "DELETE"])
