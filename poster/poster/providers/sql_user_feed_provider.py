from poster.providers.user_feed_provider import UserFeedProvider
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import Session
from poster.models.post import Post


class SqlUserFeedProvider(UserFeedProvider):
    """Provide users feed from SQL database"""
    def __init__(self, engine: Engine):
        self.engine = engine

    def most_recent(self, username: str, n: int) -> list[Post]:
        with Session(bind=self.engine) as sess:
            return (
                sess.query(Post)
                    .filter(Post.username != username)
                    .order_by(Post.created_at.desc())
                    .limit(n)
                    .all()
            )

    def user_posts(self, username: str, n: int) -> list[Post]:
        with Session(bind=self.engine) as sess:
            my_posts = (sess
                        .query(Post)
                        .filter(Post.username == username)
                        .filter(~Post.content.like("@%"))
                        .filter(Post.likes >= 0)
                        .order_by(Post.likes.desc(), Post.created_at.desc())
                        .limit(n).all()
                        )
            return my_posts

    def share_post(self, post: Post):
        with Session(bind=self.engine, expire_on_commit=False) as sess:
            sess.add(post)
            sess.commit()
