from pathlib import Path
import re
import click
import pandas as pd
import decimal

from flask import current_app

from en_cavale import db
from en_cavale.models import Category, Spending

# Get the base directory (the directory of the current file)
basedir = Path(__file__).resolve().parent

# Construct the data directory path
datadir = basedir / "../../data"


@click.argument("csv_file")
@click.command("import-csv")
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

    # Iterate through the CSV rows
    for index, row in df.iterrows():
        category_name = row["Categorie"]
        category_id = category_mapping.get(category_name)

        if category_id:
            spending = Spending(
                date=row["Date"],
                amount=float(re.sub("[^0-9|.]", "", row["Montant"])),
                category_id=category_id,
            )
            if not pd.isna(row["Description"]):
                spending.description = row["Description"]
            db.session.add(spending)
        else:
            print(f"Category '{category_name}' not found at index {index}!")

    db.session.commit()
    print(f"Data from {csv_file} successfully imported.")
