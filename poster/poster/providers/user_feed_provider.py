from typing import Protocol
from poster.models.post import Post


class UserFeedProvider(Protocol):
    def most_recent(self, n: int) -> list[Post]:
        """Return the n most recent posts."""
        ...

    def user_posts(self, username: str, n: int) -> list[Post]:
        """Return all posts by the user."""
        ...

    def share_post(self, post: Post):
        """Share a post."""
        ...
