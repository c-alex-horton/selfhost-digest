import requests

instance = "https://lemmy.world"
community = "news"
url = f"{instance}/api/v3/post/list"

params = {"community_name": community, "limit": 1, "sort": "Hot"}

resp = requests.get(url, params=params)
posts = resp.json()["posts"]

for post in posts:
    print(post)
