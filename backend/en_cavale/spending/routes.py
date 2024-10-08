import json
from en_cavale.spending import bp
from en_cavale.spending.spending import get_spending_by_country


@bp.route("/")
def hello_world():
    return "Hello, World!"


@bp.route("/countries/")
def spending_data():
    spending = get_spending_by_country()
    spending_list = [data["spending"] for data in spending.values()]

    # This representation does not indicate how much time we spent in each country.
    d = {"country": list(spending.keys()), "spending": spending_list}
    print(d)
    return json.dumps(d, indent=4)
