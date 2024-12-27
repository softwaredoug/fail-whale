import argparse
import logging
import sys

from openai import OpenAI

import sqlalchemy
from sqlalchemy import MetaData, delete
from sqlalchemy.orm import sessionmaker

from poster.env_default import EnvDefault
from poster.connect import connect
from poster.post import Post
from poster.post_generator import post_generator


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
stdout_handler.setFormatter(formatter)

logger.addHandler(stdout_handler)

# Ensure no duplicate handlers
logger.propagate = False


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
    parser.add_argument(
        "--drop",
        action="store_true",
        help="Drop all posts before inserting new ones",
    )
    parser.add_argument(
        "--topic",
        type=str,
        help="Topic to generate posts about",
    )
    return parser.parse_args()


def drop_all_posts(engine):
    metadata = MetaData()
    metadata.reflect(bind=engine)
    with sessionmaker(bind=engine)() as session:
        session.execute(delete(Post))
        session.commit()
        logger.info("All posts deleted.")


def main():
    args = parse_args()
    engine = connect(args.database_url)
    client = OpenAI(api_key=args.openai_api_key)
    if args.drop:
        drop_all_posts(engine)
    # Dump users
    metadata = MetaData()
    metadata.reflect(bind=engine)
    with sessionmaker(bind=engine)() as session:
        for gpt_post in post_generator(openai=client, topic=args.topic):
            new_post = Post(content=gpt_post['content'], username=gpt_post['username'],
                            created_at=sqlalchemy.sql.func.now(), updated_at=sqlalchemy.sql.func.now())
            session.add(new_post)
            session.commit()
            # Insert seed posts


if __name__ == "__main__":
    main()
