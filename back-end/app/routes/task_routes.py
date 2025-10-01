from flask import Blueprint

from app.views import UserTaskView, AdminTaskView

task_bp = Blueprint("tasks", __name__, url_prefix="/api")

user_task_view = UserTaskView.as_view("user_task_view")
admin_task_view = AdminTaskView.as_view("admin_task_view")

task_bp.add_url_rule("/tasks", view_func=user_task_view, methods=["POST", "GET"])
task_bp.add_url_rule("/tasks/<task_uuid>", view_func=user_task_view, methods=["PUT", "DELETE"])

task_bp.add_url_rule("/users/<user_uuid>/tasks", view_func=admin_task_view, methods=["GET"])
task_bp.add_url_rule("/users/<user_uuid>/tasks/<task_uuid>", view_func=admin_task_view, methods=["PUT", "DELETE"])
