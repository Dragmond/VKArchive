import json
from pathlib import Path

from models.settings import Settings


CONFIG_FILE = Path("config.json")


class Config:

    def __init__(self):

        self.settings = Settings()

        self.load()

    def load(self):

        if not CONFIG_FILE.exists():
            raise FileNotFoundError("config.json not found")

        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.settings = Settings.from_dict(data)

    def save(self):

        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(
                self.settings.to_dict(),
                f,
                indent=4,
                ensure_ascii=False,
            )


config = Config()
