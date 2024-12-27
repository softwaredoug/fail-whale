import os
import argparse

import sqlalchemy
from sqlalchemy import create_engine, MetaData, Table, inspect
from sqlalchemy.orm import sessionmaker

from poster.env_default import EnvDefault
from poster.connect import connect


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Connect to a database and query the 'users' table.")
    parser.add_argument(
        "--database-url",
        type=str,
        action=EnvDefault,
        envvar="DATABASE_URL",
        required=True,
        help="Database URL to connect to (overrides DATABASE_URL environment variable)",
    )
    parser.add_argument(
        "--openai-api-key",
        type=str,
        action=EnvDefault,
        envvar="OPENAI_API_KEY",
        required=True,
        help="OpenAI API key (overrides OPENAI_API_KEY environment variable)",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    engine = connect(args.database_url)
    # Dump users
    metadata = MetaData()
    metadata.reflect(bind=engine)
    session = sessionmaker(bind=engine)()
    user_table = metadata.tables["users"]
    users = session.query(user_table).all()
    for user in users:
        print(user)
    session.close()



if __name__ == "__main__":
    main()
