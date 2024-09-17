from flask import Blueprint

bp = Blueprint("spending", __name__)

from en_cavale.spending import routes
