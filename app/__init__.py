from flask import Flask
import os
from app.auth import auth, log_required
from app.bookmarks import bookmarks
from app.database import db
from app.services.microservice import micro
from flask_jwt_extended import JWTManager
from app.main import main


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY=os.environ.get("SECRET_KEY"),
            SQLALCHEMY_DATABASE_URI=os.environ.get("SQLALCHEMY_DB_URI"),
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            JWT_SECRET_KEY=os.environ.get("JWT_SECRET_KEY"),
            JWT_TOKEN_LOCATION=['cookies'],
            JWT_COOKIE_SECURE=True,
            JWT_COOKIE_CSRF_PROTECT=False,
            JWT_ACCESS_COOKIE_PATH='/api/v1/'
        )
    else:
        app.config.from_mapping(test_config)

    db.app = app
    db.init_app(app)

    jwt = JWTManager(app)

    @jwt.unauthorized_loader
    def unauthorized_callback(callback):
        return log_required()

    @jwt.invalid_token_loader
    def invalid_token_loader(callback):
        return log_required()

    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(bookmarks)
    app.register_blueprint(micro)

    return app
