from __future__ import annotations

from datetime import datetime
from pathlib import Path

from media import MediaFile
from media.download_manager import download_manager
from vk.messages import Message


class ArchiveExporter:

    def __init__(self, root: Path) -> None:

        self._root = root

    @staticmethod
    def _safe_name(name: str) -> str:

        invalid = '<>:"/\\|?*'

        for char in invalid:
            name = name.replace(char, "_")

        return name.strip() or "Conversation"

    def export_messages(
        self,
        conversation_name: str,
        messages: list[Message],
    ) -> Path:

        folder = self._root / self._safe_name(conversation_name)

        folder.mkdir(
            parents=True,
            exist_ok=True,
        )

        output = folder / "messages.txt"

        with output.open(
            "w",
            encoding="utf-8",
        ) as file:

            for message in messages:

                timestamp = datetime.fromtimestamp(
                    message.date
                ).strftime("%Y-%m-%d %H:%M:%S")

                direction = "→" if message.out else "←"

                file.write(
                    f"[{timestamp}] {direction} "
                    f"{message.from_id}: "
                    f"{message.text}\n"
                )

        return output

    def export_media(
        self,
        conversation_name: str,
        media: list[MediaFile],
    ) -> Path:

        folder = (
            self._root
            / self._safe_name(conversation_name)
            / "media"
        )

        download_manager.download_many(
            media,
            folder,
        )

        return folder


__all__ = [
    "ArchiveExporter",
]
