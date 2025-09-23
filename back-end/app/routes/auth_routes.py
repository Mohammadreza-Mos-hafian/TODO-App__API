from flask import Blueprint

from app.views import AuthView

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")
auth_bp.add_url_rule("/<action>", view_func=AuthView.as_view("auth_view"))
