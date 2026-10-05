import pandas as pd
from sqlalchemy import create_engine

DATABASE_URL = "sqlite:///emergency_resources.db"

engine = create_engine(DATABASE_URL)


def create_database():
    """Create the emergency resources database."""

    df = pd.read_csv("data/resources.csv")

    df.to_sql(
        "resources",
        engine,
        if_exists="replace",
        index=False
    )


def get_resources():
    """Read all resources from the database."""

    return pd.read_sql(
        "SELECT * FROM resources",
        engine
    )