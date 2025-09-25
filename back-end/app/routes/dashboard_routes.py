from flask import Blueprint

from app.views import DashboardView

dash_bp = Blueprint("dashboard", __name__, url_prefix="/api/dashboard")
dash_bp.add_url_rule("/home", view_func=DashboardView.as_view("dash_view"))
