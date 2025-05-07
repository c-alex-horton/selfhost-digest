import requests
from pathlib import Path
from urllib.parse import urlparse
import uuid
import os
from opengraph_parse import parse_page


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
            filename = str(uuid.uuid4()) + "-image.jpg"  # fallback if no name

        # Build full path
        filepath = images_dir / filename

        # Skip download if file already exists
        if filepath.exists():
            print(f"Image already exists: {filepath}")
            return filepath.relative_to("output")

        # Download the image
        response = requests.get(url, stream=True, timeout=10)
        response.raise_for_status()

        with open(filepath, "wb") as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)

        print(f"Downloaded: {filepath}")
        return filepath.relative_to("output")

    except Exception as e:
        print(f"Failed to download {url}: {e}")
        return None
