import sqlalchemy as sa
import sqlalchemy.orm as so
from en_cavale import create_app, db
from en_cavale.models import Category, Country, Spending

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {
        "sa": sa,
        "so": so,
        "db": db,
        "Category": Category,
        "Country": Country,
        "Spending": Spending,
    }
