import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS


db = SQLAlchemy()
migrate = Migrate()


def create_app():
    # instantiate the app
    app = Flask(__name__)

    # set config
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)
    CORS(app)

    # set up extensions
    db.init_app(app)
    migrate.init_app(app, db)


    # register blueprints
    from project.api.views import users_blueprint
    app.register_blueprint(users_blueprint)

    return app

