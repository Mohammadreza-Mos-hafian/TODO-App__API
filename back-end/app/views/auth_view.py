from flask.views import View
from flask import jsonify, request
from flask_jwt_extended import jwt_required

from app.services import AuthService
from app.utils import error_handler


class AuthView(View):
    methods = ["POST"]
    decorators = [error_handler]

    def dispatch_request(self, *args, **kwargs):
        actions = {
            "register": self.register,
            "login": self.login,
            "refresh": self.refresh,
        }

        action = request.view_args.get("action")
        func = actions.get(action)

        if not func:
            return jsonify({
                "status": "error",
                "message": "Page not found",
            }), 404

        return func()

    # ____________________________________________________ Register ____________________________________________________

    def register(self):
        data = request.get_json()
        response = AuthService.register_user(data)
        return jsonify(response), 201

    # ____________________________________________________ Login ____________________________________________________

    def login(self):
        data = request.get_json()
        response = AuthService.login_user(data)
        return jsonify(response), 200

    @jwt_required(refresh=True)
    def refresh(self):
        return AuthService.create_new_access_token()
