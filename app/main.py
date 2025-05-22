import shutil
import threading
import time
from datetime import datetime
from pathlib import Path

import markdown
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from app.lemmy.lemmy_news import gen_lemmy_news
from app.utils.server import serve_content
from app.weather.weather import gen_weather

from .config import config

all_posts = []
output_dir = Path(config["output_path"])


def make_header():
    lines = []

    lines.append("# Selfhost Digest\n")
    now = datetime.now()
    display_time = now.strftime("%Y-%m-%d %H:%M:%S")
    lines.append(f"#### {display_time}\n")
    return "\n".join(lines)


def generate_digest():
    
    if not output_dir.exists():
        output_dir.mkdir(parents=True)

    temp_dir = Path("temp")
    if temp_dir.exists():
        shutil.rmtree(temp_dir)

    shutil.copytree("template", temp_dir, dirs_exist_ok=True)

    full_md = build_markdown()

    output_path = temp_dir / "selfhost_digest.md"
    output_path.write_text(full_md, encoding="utf-8")
    
    gen_html_site(full_md, temp_dir)

    for item in output_dir.iterdir():
        if item.is_dir():
            shutil.rmtree(item)
        else:
            item.unlink()

    shutil.copytree(temp_dir, output_dir, dirs_exist_ok=True)


def build_markdown():
        all_sections = []

        all_sections.append(make_header())

        if "weather" in config["modules"]:
            all_sections.append(gen_weather(config["modules"]["weather"]))

        if "lemmy" in config["modules"]:
            all_sections.append(gen_lemmy_news(config["modules"]["lemmy"]))

        return  "\n\n---\n\n".join(all_sections)


def gen_html_site(full_md, temp_dir):
    with open(temp_dir / "template.html") as f:
        template = f.read()
    tempHTML = markdown.markdown(full_md)
    final_html = template.replace("contenthere", tempHTML)
    html_path = temp_dir / "index.html"
    html_path.write_text(final_html, encoding='utf=8')


def main():
        
    scheduler = BackgroundScheduler(daemon=False)

    generate_digest()

    for entry in config.get('schedule', []):
        hour, minute = map(int, entry["time"].split(":"))
        trigger = CronTrigger(hour=hour, minute=minute)

        scheduler.add_job(generate_digest, trigger)
    
    scheduler.start()
   
    server_thread = threading.Thread(target=serve_content, daemon=True)

    server_thread.start()

    try:
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        print("\nShutting down...")
        scheduler.shutdown(wait=False)


if __name__ == "__main__":
    main()
