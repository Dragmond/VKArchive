from __future__ import annotations

from datetime import datetime


class DateFormatter:

    @staticmethod
    def key(timestamp: int) -> str:
        return datetime.fromtimestamp(
            timestamp,
        ).strftime("%Y-%m-%d")

    @staticmethod
    def title(timestamp: int) -> str:
        return datetime.fromtimestamp(
            timestamp,
        ).strftime("%d.%m.%Y")
