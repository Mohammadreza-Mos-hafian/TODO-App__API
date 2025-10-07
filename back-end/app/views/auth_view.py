from flask.views import View
from flask import jsonify, request
from flask_jwt_extended import jwt_required

from sqlalchemy.exc import SQLAlchemyError

from marshmallow import ValidationError

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
        try:
            data = request.get_json()
            response = AuthService.register_user(data)
            return jsonify(response), 201

        except ValidationError as err:
            return jsonify({
                "status": "error",
                "errors": err.messages
            }), 400

        except ValueError as err:
            return jsonify({
                "status": "Auth Error",
                "errors": str(err)
            }), 500

        except SQLAlchemyError as err:
            return jsonify({
                "status": "DB Error",
                "errors": str(err)
            }), 500
        # ____________________________________________________ Login ____________________________________________________

    @staticmethod
    def login():
        try:
            data = request.get_json()
            response = AuthService.login_user(data)
            return jsonify(response), 200

        except ValidationError as err:
            return jsonify({
                "status": "error",
                "errors": err.messages
            }), 400

        except ValueError as err:
            return jsonify({
                "status": "Auth Error",
                "errors": str(err)
            }), 500

        except SQLAlchemyError as err:
            return jsonify({
                "status": "DB Error",
                "errors": str(err)
            }), 500

    @staticmethod
    @jwt_required(refresh=True)
    def refresh():
        return AuthService.create_new_access_token()
