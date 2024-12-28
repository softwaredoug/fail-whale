from typing import Optional
import logging

from poster.providers import NewPostProvider, UserFeedProvider
from poster.models.post import Post


logger = logging.getLogger(__name__)


def user_tick(username: str,
              feed_provider: UserFeedProvider,
              post_provider: NewPostProvider,
              scan_N: int = 10,
              user_N: int = 10) -> Optional[Post]:
    """Generate a new post for the user and add it to the feed."""
    my_posts = feed_provider.user_posts(username, user_N)
    feed = feed_provider.most_recent(scan_N)
    return post_provider.generate_post(username, user_history=my_posts, feed=feed)


def loop(feed_provider: UserFeedProvider,
         post_provider: NewPostProvider,
         usernames: list[str],
         scan_N: int = 10,
         user_N: int = 10) -> None:
    """Run the user tick loop."""
    while True:
        for username in usernames:
            new_post = user_tick(username, feed_provider, post_provider, scan_N, user_N)
            if new_post:
                feed_provider.share_post(new_post)
                logger.info(f"User {username} posted: {new_post.content}")
            else:
                logger.info(f"User {username} did not post")
