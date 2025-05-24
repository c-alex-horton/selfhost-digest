import requests
from pathlib import Path
import uuid
import time
from opengraph_parse import parse_page
from app.config import config, ua


def handle_opengraph(link_url):
    if config["testing"]:
        return "images/placeholder.jpg"

    try:
        data = parse_page(link_url)
        if isinstance(data, dict) and "og:image" in data:
            return download_image(data["og:image"])
    except Exception as e:
        print(f"Failed to parse OpenGraph for {link_url}: {e}")

    return "images/placeholder.jpg" if config["image_for_all_posts"] else None


def download_image(url, retries=3, delay=3):
    if config["testing"]:
        return "images/placeholder.jpg"

    images_dir = Path("temp/images")
    images_dir.mkdir(parents=True, exist_ok=True)
    filename = f"{uuid.uuid4()}-image.jpg"
    filepath = images_dir / filename

    HEADERS = {
        "User-Agent": ua
    }

    for attempt in range(retries):
        try:
            response = requests.get(url, headers=HEADERS, stream=True, timeout=10)
            response.raise_for_status()

            with open(filepath, "wb") as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)

            print(f"Downloaded: {filepath}")
            return Path("images") / filename

        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1} failed to download {url}: {e}")
            time.sleep(delay)

    print(f"Giving up on {url}")
    return "images/placeholder.jpg" if config["image_for_all_posts"] else None

