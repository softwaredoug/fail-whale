from typing import Protocol, Optional
from poster.models.post import Post


class NewPostProvider(Protocol):
    def generate_post(self, username: str, user_history: list[Post], feed: list[Post]) -> Optional[Post]:
        """Create a new post."""
        ...
