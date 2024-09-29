from pathlib import Path
import re
import click
import pandas as pd
import decimal
import time
from functools import wraps

from flask import current_app

from en_cavale import db
from en_cavale.models import Category, Spending

# Get the base directory (the directory of the current file)
basedir = Path(__file__).resolve().parent

# Construct the data directory path
datadir = basedir / "../../data"


def timing_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} took {end_time - start_time:.4f} seconds to execute.")
        return result

    return wrapper


@click.argument("csv_file")
@click.command("import-csv")
@timing_decorator
def import_csv(csv_file):
    """Import data from a CSV file into the database."""
    file = datadir / csv_file
    print(f"Importing data from {file} in data folder...")
    # Load the CSV file using pandas
    df = pd.read_csv(file)

    # Strip whitespace from column names and data
    df.columns = df.columns.str.strip()
    df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

    # Preload all category_name to category_id mappings into a dictionary
    category_mapping = {cat.name: cat.id for cat in Category.query.all()}

    # Pre-process the DataFrame
    df["category_id"] = df["Categorie"].map(category_mapping)
    df["amount"] = df["Montant"].str.replace(r"[^0-9|.]", "", regex=True).astype(float)

    # Filter out rows with invalid categories
    valid_df = df[df["category_id"].notna()]
    invalid_categories = df[df["category_id"].isna()]["Categorie"].unique()

    if len(invalid_categories) > 0:
        print(f"Invalid categories found: {invalid_categories}")

    spendings = []
    # Iterate through the CSV rows
    for index, row in valid_df.iterrows():
        spending = Spending(
            date=row["Date"],
            amount=row["amount"],
            category_id=row["category_id"],
        )
        if not pd.isna(row["Description"]):
            spending.description = row["Description"]
        spendings.append(spending)
        db.session.add(spending)

    # Bulk insert not faster that inserting one by one and then committing.
    # db.session.bulk_save_objects(spendings)
    db.session.commit()
    print(
        f"Data from {csv_file} successfully imported. {len(spendings)} spendings inserted."
    )
