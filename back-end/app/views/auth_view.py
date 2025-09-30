from flask.views import View
from flask import jsonify, request
from flask_jwt_extended import jwt_required

from app.services import AuthService


class AuthView(View):
    methods = ["POST"]

    def dispatch_request(self, *args, **kwargs):
        action = request.view_args.get("action")

        if action == "register":
            return self.register()

        if action == "login":
            return self.login()

        if action == "refresh":
            return self.refresh()

        return jsonify({
            "status": "error",
            "message": "Page not found",
        }), 404

    # ____________________________________________________ Register ____________________________________________________
    @staticmethod
    def register():
        data = request.get_json()
        response = AuthService.register_user(data)
        return response

        # ____________________________________________________ Login ____________________________________________________

    @staticmethod
    def login():
        data = request.get_json()
        response = AuthService.login_user(data)
        return response

    @staticmethod
    @jwt_required(refresh=True)
    def refresh():
        return AuthService.create_new_access_token()
