from sqlalchemy import create_engine
import pandas as pd


DATABASE_URL = "sqlite:///emergency_resources.db"

engine = create_engine(DATABASE_URL)


def load_resources():
    """
    Load emergency resources from CSV into a pandas DataFrame.
    """

    file_path = "data/resources.csv"

    df = pd.read_csv(file_path)

    return df


def save_resources_to_database():

    df = load_resources()

    df.to_sql(
        "resources",
        engine,
        if_exists="replace",
        index=False
    )


def get_resources_from_database():

    try:

        df = pd.read_sql(
            "SELECT * FROM resources",
            engine
        )

        return df

    except Exception:

        save_resources_to_database()

        df = pd.read_sql(
            "SELECT * FROM resources",
            engine
        )

        return df