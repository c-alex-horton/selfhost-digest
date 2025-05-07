import yaml
import sys
import requests
from datetime import datetime
from pathlib import Path
import json
import shutil
from .utils import download_image, handle_opengraph
from .config import config


all_posts = []


def setup():
    output_dir = Path("output")

    if output_dir.exists():
        for item in output_dir.iterdir():
            if item.is_dir():
                shutil.rmtree(item)
            else:
                item.unlink()
    else:
        output_dir.mkdir()

    image_dir = output_dir / "images"
    image_dir.mkdir(exist_ok=True)

    shutil.copy("placeholder.jpg", image_dir / "placeholder.jpg")


# Fetch posts from all instances and communities defined in the Yaml config
def get_posts(instances):
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


def posts_to_markdown():
    print("Writing posts to markdown...")
    output_dir = Path("./output")
    output_dir.mkdir(exist_ok=True)

    with open("./output/output.md", "w", encoding="utf-8") as f:
        f.write("# Selfhost Digest\n")
        now = datetime.now()
        display_time = now.strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"#### {display_time}\n")
        for instance_posts in all_posts:
            f.write(f"## {instance_posts['community']}\n")
            for post in instance_posts["posts"]:
                # Make the post name a link to the Lemmy article
                f.write(f"### [{post['post']['name']}]({post['post']['ap_id']})\n")

                # Get the Opengraph image of the article link. Might change this to the thumbnail image
                if "thumbnail_url" in post["post"]:
                    image = download_image(post["post"]["thumbnail_url"])
                    if image:
                        f.write(f"![link image]({image})\n")
                elif "image_details" in post:
                    image = download_image(post["image_details"]["link"])
                    if image:
                        f.write(f"![link image]({image})\n")
                elif "url" in post["post"]:
                    image = handle_opengraph(post["post"]["url"])
                    if image:
                        f.write(f"![link image]({image})\n")
                elif config["image_for_all_posts"]:
                    f.write(f"![link image](images/placeholder.jpg)\n")

                if "body" in post["post"]:
                    f.write(post["post"]["body"] + "\n")
                if "url" in post["post"]:
                    f.write(f"#### [Link to Article]({post['post']['url']})\n")

                # Add some extra padding between articles for readability
                f.write("\n\n\n")


def move_output(path):
    try:
        shutil.rmtree(path + "output")
    except Exception as e:
        print(e)

    try:
        shutil.move("./output", path)
    except Exception as e:
        print(e)


setup()

if not config["testing"]:
    get_posts(config["instances"])
else:
    print("Testing Enabled")
    if Path("posts_output.json").exists():
        with open("posts_output.json", "r", encoding="utf-8") as f:
            all_posts = json.load(f)
    else:
        print("No 'posts_output.json' file found. Pulling posts.")
        get_posts(config["instances"])

posts_to_markdown()

if not config["testing"]:
    move_output(config["output_path"])
