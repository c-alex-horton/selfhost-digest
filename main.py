import yaml
import requests


with open("config.yml", "r") as f:
    config = yaml.safe_load(f)

# print(config)

all_posts = []


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

            all_posts.append(resp.json()["posts"])
            print("Done")

    print("All posts received")
    for instance_posts in all_posts:
        for post in instance_posts:
            print(post["post"]["name"])


get_posts(config["instances"])
