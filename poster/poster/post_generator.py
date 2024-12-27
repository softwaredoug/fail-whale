import json

PROMPT = """
Generate spicy or controversial twitter posts about the requested topic.

Return a JSON array of objects with the following fields:
    - content: the content of the post
    - username: the username of the poster

Here's an example of what the JSON object should look like if the topic is
Kamala Harris and we request 2 posts:

[
    {
        "content": "Wow did you see what Kamala Harris did today?",
        "username": "american_democrat123"
    },
    {
        "content": "I'm tired of this woke nonsense from Kamala Harris",
        "username": "conservative_4_life"
    }
]

Here's an example of what the JSON object should look like if the topic is
kubernetes and we request 3 posts:

[
    {
        "content": "If you don't like k8s, you're a bad developer",
        "username": "devops_guru"
    },
    {
        "content": "Kubernetes is so hard to use",
        "username": "sysadmin_123"
    },
    {
        "content": "In this blog post, I discuss why you should not use kubernetes",
        "username": "cloud_ninja"
    }

"""


def post_generator(openai, topic, N=10) -> list[dict[str, str]]:
    completions = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": PROMPT},
            {"role": "user", "content": f"Generate {N} spicy or controversial twitter posts about {topic}"},
        ],
    )
    posts = completions.choices[0].message.content
    return json.loads(posts)
