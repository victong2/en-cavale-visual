from datetime import timedelta
import re
import psycopg
from config import load_config
import plotly.express as px
import plotly.graph_objects as go
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
    res = {}
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

        res[country_name] = {
            "spending": spendingPerCountry[country_name] / delta_day,
            "arrival": country.arrival,
            "departure": country.departure,
        }

    return res


def draw_graph(spendingPerCountryPerDay):
    df = pd.DataFrame(data=spendingPerCountryPerDay)

    # Convert arrival and departure columns to datetime
    df["arrival"] = pd.to_datetime(df["arrival"])
    df["departure"] = pd.to_datetime(df["departure"])

    # Calculate the number of days spent in each country
    # df["days_spent"] = (df["departure"] - df["arrival"]).dt.days - 1

    fig = go.Figure()

    # Create a bar for each day in each country
    for _, row in df.iterrows():
        date_range = pd.date_range(start=row["arrival"], end=row["departure"])
        daily_spending = row["spending"]
        fig.add_trace(
            go.Bar(
                x=date_range,
                y=[daily_spending] * len(date_range),
                name=row["country"],
                text=[row["country"]] * len(date_range),
                hovertemplate="%{text}<br>Date: %{x}<br>Daily Spending: %{y:.2f} $CAD",
            )
        )

    # Update layout to improve visualization
    fig.update_layout(
        title="Daily Spending per Country Over Time",
        xaxis_title="Date",
        yaxis_title="Daily Spending in $CAD",
        barmode="overlay",
        legend_title="Countries",
        # hovermode="x unified",
        hovermode="closest",
    )

    fig.show()


# Quickly visualize the graph.
# Run this function inside `flask shell`:
# >>> from en_cavale.spending.spending import start
# >>> start()
def start():
    spending = get_spending_by_country()

    spending_list = [data["spending"] for data in spending.values()]
    arrival = [data["arrival"] for data in spending.values()]
    departure = [data["departure"] for data in spending.values()]

    d = {
        "country": spending.keys(),
        "spending": spending_list,
        "arrival": arrival,
        "departure": departure,
    }
    draw_graph(d)
