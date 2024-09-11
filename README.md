Web application to visualize spendings during a year of travels.

# Setup

[pyenv](https://github.com/pyenv/pyenv) is _recommended_ to handle the Python version. We use Python 3.11.

[Poetry](https://python-poetry.org/) is used for dependency management and virtual environment handling.

```
poetry add psycopg
poetry shell
```

# Running the app

## Database

Start database container.

```
docker-compose up -d
```

## Backend

Start the Flask application as a backend process.

```
poetry run start
```

# IDE

Select appropriate Python interpreter. It is in the virtual environment provided by `poetry env info --path`.

# Database

We use the default username `postgres`.
To connect to the DB, We use the CLI tool `psql` and the web interface of adminer. **DBeaver** is also a recommended client.

Data are imported from a Google sheet.

# TODO

Apply migrations/versioning with Alembic or liquibase.
