import argparse
import logging
import sys

from openai import OpenAI

from sqlalchemy import MetaData, delete
from sqlalchemy.orm import sessionmaker

from poster.env_default import EnvDefault
from poster.connect import connect
from poster.models.post import Post
from poster.loop.loop import loop
from poster.providers import OpenAiNewPostProvider, SqlUserFeedProvider


logger = logging.getLogger("poster")
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
    parser.add_argument(
        "--times",
        type=int,
        default=1,
        help="Number of times to run the loop per user",
    )
    parser.add_argument(
        "--username",
        nargs="+",
        required=True,
        type=str,
        help="Usernames to generate posts for",
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

    feed_provider = SqlUserFeedProvider(engine)
    post_provider = OpenAiNewPostProvider(client)

    loop(feed_provider, post_provider, usernames=args.username,
         times=args.times * len(args.username))


if __name__ == "__main__":
    main()
