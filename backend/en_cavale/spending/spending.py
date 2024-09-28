from datetime import timedelta
import re
import psycopg
from config import load_config
import plotly.express as px
import pandas as pd
from en_cavale import db
from en_cavale.models import Country, Spending

from sqlalchemy import func
from datetime import timedelta
from collections import defaultdict


def with_session(func):
    def wrapper(*args, **kwargs):
        with db.session() as session:
            try:
                return func(session, *args, **kwargs)
            except Exception as error:
                session.rollback()
                print(f"Error occurred: {error}")
                raise

    return wrapper


def get_spendings(session):
    """Yield Spending records in batches to manage memory efficiently."""
    return (spending for spending in session.query(Spending).yield_per(100))


@with_session
def get_spending_by_country(session):
    """
    Calculate average daily spending per country
    """
    countries = session.query(Country).all()

    spendingPerDay = defaultdict(float)
    spendingPerCountry = defaultdict(float)

    # Calculate spending per day
    for spending in get_spendings(session):
        spendingPerDay[spending.date] += float(spending.amount)

    # Determine overlapping days. The date has been seen twice (or more).
    # During overlapping days, money is spent in both countries.
    overlapping = {}
    for c in countries:
        overlapping[c.arrival] = c.arrival in overlapping
        overlapping[c.departure] = c.departure in overlapping

    # Handle country spending per day and per country
    for country in countries:
        country_name = country.name
        if country.region:
            country_name += f": {country.region}"

        delta_day = (country.departure - country.arrival).days
        days = (country.arrival + timedelta(days=i) for i in range(delta_day + 1))
        for day in days:
            spendingPerCountry[country_name] += spendingPerDay.get(day, 0) / (
                2 if overlapping.get(day) else 1
            )

        spendingPerCountry[country_name] /= delta_day

    return spendingPerCountry


def draw_graph(spendingPerCountryPerDay):
    print("draw graph")
    df = pd.DataFrame(data=spendingPerCountryPerDay)
    fig = px.bar(df, x="country", y="spending")
    fig.show()


# Quickly visualize the graph.
# Run this function inside `flask shell`:
# >>> from en_cavale.spending.spending import start
# >>> start()
def start():
    spending = get_spending_by_country()

    # This representation does not indicate how much time we spent in each country.
    d = {"country": spending.keys(), "spending": spending.values()}
    draw_graph(d)
