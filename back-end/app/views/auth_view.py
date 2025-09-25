from flask.views import View
from flask import jsonify, request

from app.services import AuthService


class AuthView(View):
    methods = ["GET", "POST"]

    def dispatch_request(self, *args, **kwargs):
        action = request.view_args.get("action")

        if action == "register" and request.method == "POST":
            return self.register()

        if action == "login" and request.method == "POST":
            return self.login()

        if action == "logout": return self.logout()

        return None

    # ____________________________________________________ Register ____________________________________________________
    @staticmethod
    def register():
        data = request.get_json()
        response = AuthService.register_user(data)
        return jsonify(response)

        # ____________________________________________________ Login ____________________________________________________

    @staticmethod
    def login():
        data = request.get_json()
        response = AuthService.login_user(data)
        return jsonify(response)

    # ____________________________________________________ Logout ____________________________________________________
    @staticmethod
    def logout():
        pass
