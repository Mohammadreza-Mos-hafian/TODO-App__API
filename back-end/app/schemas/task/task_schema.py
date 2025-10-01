from marshmallow import post_dump, pre_dump
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from app.models import Task
from app.utils import show_task_status, task_status_color


class TaskSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Task
        load_instance = True
        exclude = ("id", "is_deleted", "uuid", "created_at", "updated_at", "deleted_at")

    @post_dump
    def post_dump_data(self, task, **kwargs):
        task["color"] = task_status_color(task["status"])
        task["status"] = show_task_status(task["status"])

        return task
