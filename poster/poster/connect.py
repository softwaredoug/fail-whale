from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine


def connect(database_url: str) -> Engine:
    """Connect to the database and return the engine."""
    if database_url.startswith("postgresql://"):
        database_url = database_url.replace("postgresql://", "postgresql+psycopg://", 1)
    else:
        raise ValueError(f"Unsupported database URL: {database_url}. Please only pass standard postgresql:// URLs.")
    engine = create_engine(database_url)
    return engine
