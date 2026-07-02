import json
from pathlib import Path


CONFIG_FILE = Path("config.json")


class Config:

    def __init__(self):

        self.load()

    def load(self):

        if not CONFIG_FILE.exists():
            raise FileNotFoundError("config.json not found")

        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            self.data = json.load(f)

    def save(self):

        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(
                self.data,
                f,
                indent=4,
                ensure_ascii=False
            )

    def get(self, key, default=None):

        return self.data.get(key, default)

    def set(self, key, value):

        self.data[key] = value
        self.save()


config = Config()