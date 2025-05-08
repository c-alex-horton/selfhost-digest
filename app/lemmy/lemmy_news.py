import requests
from datetime import datetime
import json
from app.utils import download_image, handle_opengraph
from app.config import config
from pathlib import Path


# Fetch posts from all instances and communities defined in the Yaml config
def get_posts(instances):
    all_posts = []
    print("Fetching Posts...")
    for instance in instances:
        url = f"{instance["url"]}/api/v3/post/list"

        for community in instance["communities"]:
            params = {
                "community_name": community["name"],
                "limit": community["posts"],
                "sort": "Hot",
            }
            print(f"Getting posts from {instance['url']}/c/{community['name']}...")
            resp = requests.get(url, params=params)

            fetched_posts = resp.json()["posts"]

            instance_posts = {
                "community": f"{instance['url']}/c/{community['name']}",
                "fetched_at": datetime.now(),
                "posts": fetched_posts,
            }

            all_posts.append(instance_posts)
            print("Done")

    with open("posts_output.json", "w", encoding="utf-8") as f:
        json.dump(all_posts, f, ensure_ascii=False, indent=2, default=str)

    print("All posts received")
    return all_posts


def posts_to_markdown(posts):
    print("Generating markdown from posts...")
    lines = []

    for instance_posts in posts:
        lines.append(f"## {instance_posts['community']}\n")
        for post in instance_posts["posts"]:
            lines.append(f"### [{post['post']['name']}]({post['post']['ap_id']})\n")

            image = None
            if "thumbnail_url" in post["post"]:
                image = download_image(post["post"]["thumbnail_url"])
            elif "image_details" in post:
                image = download_image(post["image_details"]["link"])
            elif "url" in post["post"]:
                image = handle_opengraph(post["post"]["url"])
            elif config["image_for_all_posts"]:
                image = "images/placeholder.jpg"

            if image:
                lines.append(f"![link image]({image})\n")

            if "body" in post["post"]:
                lines.append(post["post"]["body"] + "\n")
            if "url" in post["post"]:
                lines.append(f"#### [Link to Article]({post['post']['url']})\n")

            lines.append("\n\n\n")

    return "\n".join(lines)


def gen_lemmy_news():

    if not config["testing"]:
        posts = get_posts(config["instances"])
    else:
        print("Testing Enabled")
        if Path("posts_output.json").exists():
            with open("posts_output.json", "r", encoding="utf-8") as f:
                posts = json.load(f)
        else:
            print("No 'posts_output.json' file found. Pulling posts.")
            posts = get_posts(config["instances"])

    return posts_to_markdown(posts)
