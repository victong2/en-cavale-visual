from datetime import timedelta
import re
import psycopg
from config import load_config
import plotly.express as px
import pandas as pd


def connect(config):
    """Connect to the PostgreSQL database server

    Warning: Unlike file objects or other resources, exiting the connection’s with block doesn’t close the connection, but only the transaction associated to it. If you want to make sure the connection is closed after a certain point, you should still use a try-catch block:
    """
    try:
        # connecting to the PostgreSQL server
        return psycopg.connect(**config)
    except (psycopg.DatabaseError, Exception) as error:
        print(f"The error '{error}' occurred")
        raise ConnectionError("Failed to connect to the database") from error


def get_spending_by_country():
    config = load_config()
    conn = connect(config)
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM country")
            print("The number of results: ", cur.rowcount)
            rows_countries = cur.fetchall()

            cur.execute("SELECT * FROM spending")
            print("The number of results: ", cur.rowcount)
            rows = cur.fetchall()

            spendingPerDay = {}
            spendingPerCountry = {}
            for row in rows:
                date, amount = row[1], float(row[2])
                if date in spendingPerDay:
                    spendingPerDay[date] += amount
                else:
                    spendingPerDay[date] = amount
            # print(spendingPerDay)

            # Spending per day
            # Spending per country. How do you handle days in common? Half half
            overlapping = {}
            for row in rows_countries:
                country, start, end = row[1], row[2], row[3]
                if start in overlapping:
                    overlapping[start] = True
                else:
                    overlapping[start] = False
                if end in overlapping:
                    overlapping[end] = True
                else:
                    overlapping[end] = False

            spendingPerCountryPerDays = {}
            for row in rows_countries:
                country, start, end, region = row[1], row[2], row[3], row[4]
                # Edge case for countries reapparing multiple times.
                country_name = country
                if region:
                    country_name += f": {region}"
                spendingPerCountry[country_name] = 0
                # Sum amount between date
                # list days betwen dates
                delta = end - start
                for i in range(delta.days + 1):
                    day = start + timedelta(days=i)
                    # Avoid counting a day twice.
                    if day in overlapping and overlapping[day]:
                        spendingPerCountry[country_name] += spendingPerDay[day] / 2
                    else:
                        spendingPerCountry[country_name] += spendingPerDay[day]
                # Spending per day and per country
                spendingPerCountryPerDays[country_name] = (
                    spendingPerCountry[country_name] / delta.days
                )

            print(spendingPerCountry)
            print(spendingPerCountryPerDays)
            return spendingPerCountryPerDays
            # Spending per day and per country

            # x days of the year. y spending per day.
            # colors/layers for category
            # handle countries appearing multiple times (China)

    except (Exception, psycopg.DatabaseError) as error:
        print(error)


def draw_graph(spendingPerCountryPerDay):
    print("draw graph")
    df = pd.DataFrame(data=spendingPerCountryPerDay)
    fig = px.bar(df, x="country", y="spending")
    fig.show()


def start():
    spending = get_spending_by_country()

    # This representation does not indicate how much time we spent in each country.
    d = {"country": spending.keys(), "spending": spending.values()}
    draw_graph(d)
