import json
import logging
from typing import Optional

import sqlalchemy
from openai import OpenAI

from poster.providers.new_post_provider import NewPostProvider
from poster.models.post import Post


logger = logging.getLogger(__name__)


PROMPT = """
You're scanning twitter and thinking of a new post, formatted in JSON, to generate that will get engagement.

Format it as a machine-readable JSON object in a string with the following fields:
    - content: the content of the post
    - username: the username of the poster

Your username will be provided as follows:

    {"username": "<your username>"}

You will be provided your own previous N posts, in the form of:

    {"my_posts": [
        {
            "content": "<my previous post>",
            "username": "<my username>"
        },
        ...
    ]}

You will also be provided the N most recent posts from the feed, in the form of:

    {"feed": [
        {
            "content": "<feed post>",
            "username": "<feed username>"
        },
        ...
    }

Given these inputs you will provide a new post to share a spicy take based on your personality. Your goal is to
get attention and engagement from others.

Here are your primary inputs and how they help you formulate a new post:

 - Your old posts (ie my_posts) inform your personality, and what you might post or respond about.
 - The feed (ie feed) informs what is currently happening in the world, and what you might post about.

You must format your post as a single JSON object, as below:

Here's an example of what the JSON object should look like:
{
    "content": "Wow did you see what Kamala Harris did today?",
    "username": "<your username>"
}

You may occasionally feel strongly about a topic posted by another poster, you can respond to their last post by
adding "@<their username>" to your post. This will increase engagement and make your post more interesting. Be
insulting and rude to drive up the engagement. IE:

{
    "content": "<@their username> You're so wrong, anyone who can't see that this is a good thing is blind.",
    "username": "<your username>"
}

Or you may have a hot take on an important topic. About a movie, politics, annoying people, or anything else. IE:

{
    "content": "I can't believe they're making a new Superman movie. Let Christopher Reeve rest in peace!",
    "username": "<your username>"
}

If your history shows you replied a lot lately, you MUST create a new post, on a new topic, not a reply.
If your history shows a lot of non-replies lately, you MUST reply to someone else's post.

Mix it up!

Correct JSON formatting is crucial. Not as Markdown, but as an actual JSON object to be read by a machine.

Do not wrap the json codes in JSON markers. IE omit the triple backticks and 'json' in the following example:
```json
{
    "content": "Wow did you see what Kamala Harris did today?",
    "username": "<your username>"
}
```

Instead, format it as a bare JSON object as below:
{
    "content": "Wow did you see what Kamala Harris did today?",
    "username": "<your username>"
}

"""


class OpenAiNewPostProvider(NewPostProvider):
    """Provide new post generation using OpenAI API"""
    def __init__(self, client: OpenAI, retries: int = 3):
        self.client = client

    def _user_prompt(self, username: str, user_history: list[Post], feed: list[Post]) -> str:
        my_posts = {
            "my_posts": [{"content": post.content, "username": post.username} for post in user_history]
        }
        feed_posts = {
            "feed": [{"content": post.content, "username": post.username} for post in feed]
        }
        username_dict = {"username": username}
        user_prompt = f"""
Please generate a spicy, controversial, post based on your personality and the current feed:

{json.dumps(username_dict, indent=4)}

{json.dumps(my_posts, indent=4)}

{json.dumps(feed_posts, indent=4)}
        """
        return user_prompt

    def generate_post(self, username: str, user_history: list[Post], feed: list[Post]) -> Optional[Post]:
        user_prompt = self._user_prompt(username, user_history, feed)

        for _ in range(3):
            completions = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": PROMPT},
                    {"role": "user", "content": user_prompt},
                ],
            )
            posts = completions.choices[0].message.content
            assert posts, "OpenAI API did not return a post"
            try:
                gpt_post = json.loads(posts)
                new_post = Post(content=gpt_post['content'], username=gpt_post['username'],
                                created_at=sqlalchemy.sql.func.now(),
                                updated_at=sqlalchemy.sql.func.now())
                return new_post
            except json.JSONDecodeError:
                logger.exception(f"Error decoding OpenAI response: {posts}")
        return None
