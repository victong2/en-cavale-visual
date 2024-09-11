import json
from en_cavale.spending import get_spending_by_country
from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello, World!"


@app.route("/spending/")
def spending_data():
    spending = get_spending_by_country()

    # This representation does not indicate how much time we spent in each country.
    d = {"country": list(spending.keys()), "spending": list(spending.values())}
    print(d)
    return json.dumps(d, indent=4)


def start():
    app.run(host="0.0.0.0", port=5000, debug=True)
