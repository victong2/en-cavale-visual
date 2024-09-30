from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

# import logging

# # Configure logging
# logging.basicConfig()
# logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)  # Log SQL statements

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

    # Register the CLI command
    from en_cavale.commands import import_csv

    app.cli.add_command(import_csv)

    return app
