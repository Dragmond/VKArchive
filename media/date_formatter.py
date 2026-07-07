from __future__ import annotations

from datetime import datetime


class DateFormatter:

    @staticmethod
    def day_key(timestamp: int) -> str:

        return datetime.fromtimestamp(
            timestamp,
        ).strftime("%Y-%m-%d")

    @staticmethod
    def day_title(timestamp: int) -> str:

        return datetime.fromtimestamp(
            timestamp,
        ).strftime("%d.%m.%Y")
