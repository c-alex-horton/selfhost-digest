from pathlib import Path
import shutil
from .config import config
from app.lemmy.lemmy_news import gen_lemmy_news
from datetime import datetime
from app.weather.weather import gen_weather

all_posts = []
output_dir = Path(config["output_path"])


def setup():

    if output_dir.exists():
        for item in output_dir.iterdir():
            if item.is_dir():
                shutil.rmtree(item)
            else:
                item.unlink()
    else:
        output_dir.mkdir(parents=True)

    image_dir = output_dir / "images"
    image_dir.mkdir(exist_ok=True)

    shutil.copy("placeholder.jpg", image_dir / "placeholder.jpg")


def make_header():
    lines = []

    lines.append("# Selfhost Digest\n")
    now = datetime.now()
    display_time = now.strftime("%Y-%m-%d %H:%M:%S")
    lines.append(f"#### {display_time}\n")
    return "\n".join(lines)


def main():
    setup()

    all_sections = []

    all_sections.append(make_header())

    if "weather" in config["modules"]:
        all_sections.append(gen_weather(config["modules"]["weather"]))

    if "lemmy" in config["modules"]:
        all_sections.append(gen_lemmy_news(config["modules"]["lemmy"]))

    full_md = "\n\n---\n\n".join(all_sections)

    output_path = output_dir / "selfhost_digest.md"
    output_path.write_text(full_md, encoding="utf-8")


if __name__ == "__main__":
    main()
