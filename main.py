import yaml
import requests
from datetime import datetime
from pathlib import Path
import json
from opengraph_parse import parse_page
from urllib.parse import urlparse
import os

with open("config.yml", "r") as f:
    config = yaml.safe_load(f)

all_posts = []


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
    with open("./output/output.md", "w", encoding="utf-8") as f:
        f.write("# Selfhost Digest\n")
        for instance_posts in all_posts:
            f.write(f"## {instance_posts['community']}\n")
            for post in instance_posts["posts"]:
                f.write(f"### {post['post']['name']}\n")
                if "url" in post["post"]:
                    image = handle_opengraph(post["post"]["url"])
                    if image:
                        f.write(f"![link image]({image})")
                if "body" in post["post"]:
                    f.write(post["post"]["body"] + "\n")
                if "url" in post["post"]:
                    f.write(f"#### [Link to Article]({post['post']['url']})\n")

                # Add some extra padding between articles for readability
                f.write("\n\n\n")


def handle_opengraph(link_url):
    data = parse_page(link_url)
    if isinstance(data, dict) and "og:image" in data:
        return download_image(data["og:image"])
    else:
        return False


def download_image(url):
    try:
        # Create "images" directory if it doesn't exist
        images_dir = Path("./output/images")
        images_dir.mkdir(exist_ok=True)

        # Extract filename from URL
        parsed = urlparse(url)
        filename = os.path.basename(parsed.path)
        if not filename:
            filename = "image.jpg"  # fallback if no name

        # Build full path
        filepath = images_dir / filename

        # Download the image
        response = requests.get(url, stream=True, timeout=10)
        response.raise_for_status()

        with open(filepath, "wb") as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)

        print(f"Downloaded: {filepath}")
        return filepath

    except Exception as e:
        print(f"Failed to download {url}: {e}")
        return None


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
