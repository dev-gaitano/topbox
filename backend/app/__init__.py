from flask import Flask

from app.api import register_blueprints

from .config import Config
from .errors import register_error_handlers
from .extensions import init_extensions


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    init_extensions(app)

    register_blueprints(app)

    register_error_handlers(app)

    return app
