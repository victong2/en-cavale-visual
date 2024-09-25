from flask import Flask


def create_app():
    app = Flask(__name__)
    from en_cavale.spending import bp as spending_bp

    app.register_blueprint(spending_bp, url_prefix="/api/spending")

    return app
