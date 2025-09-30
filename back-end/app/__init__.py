from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from app.routes import auth_bp, dash_bp, task_bp
from dotenv import load_dotenv

from datetime import timedelta

import os

load_dotenv()


def create_app():
    app = Flask(__name__)

    CORS(app, supports_credentials=True, origins=["http://127.0.0.1:3000"])

    app.register_blueprint(auth_bp)
    app.register_blueprint(dash_bp)
    app.register_blueprint(task_bp)

    app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY").strip()
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_ACCESS_TOKEN_SECRET_KEY").strip()
    app.config["JWT_REFRESH_SECRET_KEY"] = os.getenv("JWT_REFRESH_TOKEN_SECRET_KEY").strip()
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=5)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)

    app.config["DEBUG"] = os.getenv("DEBUG").strip() == "True"

    JWTManager(app)

    return app
