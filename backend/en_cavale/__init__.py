from flask import Flask

app = Flask(__name__)

from en_cavale.spending import bp as spending_bp

app.register_blueprint(spending_bp, url_prefix="/spending")
