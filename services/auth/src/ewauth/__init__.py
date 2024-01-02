import os
from flask import Flask
from flask_cors import CORS
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from ewauth import config


CONFIG = config.get_app_config(os.environ.get("CONFIG", "dev"))


db = SQLAlchemy()
mail = Mail()


def create_app(app_config: config.Configuration):
    app = Flask(__name__)
    app.config.from_object(app_config)
    app_config.init_app(app)

    db.init_app(app)
    mail.init_app(app)

    from ewauth.api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix="/api/v1")

    if not isinstance(app_config, config.ProdConfig):
        CORS(app)
    Migrate(app, db)
    return app
