from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

db: SQLAlchemy = SQLAlchemy()
migrate = Migrate()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    from en_cavale import models

    from en_cavale.spending import bp as spending_bp

    app.register_blueprint(spending_bp, url_prefix="/api/spending")

    return app
