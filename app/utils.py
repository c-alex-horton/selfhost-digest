import requests
from pathlib import Path
from urllib.parse import urlparse
import uuid
import os
from opengraph_parse import parse_page
from app.config import config


def handle_opengraph(link_url):
    if config["testing"]:
        return "images/placeholder.jpg"

    data = parse_page(link_url)
    if isinstance(data, dict) and "og:image" in data:
        return download_image(data["og:image"])
    else:
        return False


def download_image(url):
    if config["testing"]:
        return "images/placeholder.jpg"

    try:
        images_dir = Path(config["output_path"]) / "images"
        images_dir.mkdir(exist_ok=True)

        filename = str(uuid.uuid4()) + "-image.jpg"
        filepath = images_dir / filename

        response = requests.get(url, stream=True, timeout=10)
        response.raise_for_status()

        with open(filepath, "wb") as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)

        print(f"Downloaded: {filepath}")
        return Path("images") / filename

    except Exception as e:
        print(f"Failed to download {url}: {e}")
        if config["image_for_all_posts"]:
            return "images/placeholder.jpg"
        return None
