from flask import Flask
from flask_cors import CORS

from app.databases import ma
from app.routes import auth_bp


def create_app():
    app = Flask(__name__)

    CORS(app)

    ma.init_app(app)

    app.register_blueprint(auth_bp)

    return app
