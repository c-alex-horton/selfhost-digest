import yaml
import sys
from pathlib import Path
import platform
from app.__version__ import __version__

config_path = Path("config.yml")

try:
    with config_path.open("r") as f:
        config = yaml.safe_load(f)
except FileNotFoundError:
    print(
        f"Config file not found at {config_path.resolve()}. You can create one by copying the config_example.yml and renaming it to 'config.yml'"
    )
    sys.exit(1)
except yaml.YAMLError as e:
    print(f"Error parsing config file: {e}")
    sys.exit(1)


if config["user_agent_name"] == "default":
    ua = f"Selfhost-Digest/{__version__} ({platform.node()}) https://github.com/c-alex-horton/selfhost-digest"
else:
    ua = config["user_agent_name"]
