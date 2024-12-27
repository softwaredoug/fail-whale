from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine

import logging


logger = logging.getLogger(__name__)


def connect(database_url: str) -> Engine:
    """Connect to the database and return the engine."""
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql+psycopg://", 1)
    else:
        raise ValueError(f"Unsupported database URL: {database_url}. Please only pass standard postgres:// URLs.")
    logger.info(f"Connecting to database: {database_url}")
    engine = create_engine(database_url)
    engine.connect()
    return engine
