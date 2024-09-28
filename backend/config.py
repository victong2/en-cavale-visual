import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))

from configparser import ConfigParser

DB_FOLDER = os.path.join(basedir, "../db/")


class Config:
    DATABASE_URL = os.environ.get("DATABASE_URL")

    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL environment variable is not set")

    SQLALCHEMY_DATABASE_URI = DATABASE_URL.replace("postgres://", "postgresql://")


def load_config(filename="database.ini", section="postgresql"):
    parser = ConfigParser()
    parser.read(DB_FOLDER + filename)

    # get section, default to postgresql
    config = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            config[param[0]] = param[1]
    else:
        raise Exception(
            "Section {0} not found in the {1} file".format(section, filename)
        )

    return config
