from poster.providers.user_feed_provider import UserFeedProvider
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import Session
from poster.models.post import Post


class SqlUserFeedProvider(UserFeedProvider):
    """Provide users feed from SQL database"""
    def __init__(self, engine: Engine):
        self.engine = engine

    def most_recent(self, n: int) -> list[Post]:
        with Session(bind=self.engine) as sess:
            return sess.query(Post).order_by(Post.created_at.desc()).limit(n).all()

    def user_posts(self, username: str, n: int) -> list[Post]:
        with Session(bind=self.engine) as sess:
            return sess.query(Post).filter(Post.username == username).limit(n).all()

    def share_post(self, post: Post):
        with Session(bind=self.engine, expire_on_commit=False) as sess:
            sess.add(post)
            sess.commit()
