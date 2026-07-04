from __future__ import annotations

from datetime import datetime
from html import escape
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

        output = folder / "messages.html"

        html: list[str] = [
            "<!DOCTYPE html>",
            "<html lang='ru'>",
            "<head>",
            "<meta charset='utf-8'>",
            f"<title>{escape(conversation_name)}</title>",
            "<style>",
            "body{font-family:Segoe UI,Arial,sans-serif;background:#202124;color:#eee;margin:0;padding:24px;}",
            "h1{margin-top:0;}",
            ".message{padding:10px;border-bottom:1px solid #444;}",
            ".meta{color:#9aa0a6;font-size:12px;margin-bottom:4px;}",
            ".text{white-space:pre-wrap;word-break:break-word;}",
            "</style>",
            "</head>",
            "<body>",
            f"<h1>{escape(conversation_name)}</h1>",
        ]

        for message in messages:

            timestamp = datetime.fromtimestamp(
                message.date
            ).strftime("%Y-%m-%d %H:%M:%S")

            direction = "Исходящее" if message.out else "Входящее"

            html.extend(
                [
                    "<div class='message'>",
                    (
                        "<div class='meta'>"
                        f"{timestamp} • "
                        f"{direction} • "
                        f"ID {message.from_id}"
                        "</div>"
                    ),
                    (
                        "<div class='text'>"
                        f"{escape(message.text)}"
                        "</div>"
                    ),
                    "</div>",
                ]
            )

        html.extend(
            [
                "</body>",
                "</html>",
            ]
        )

        output.write_text(
            "\n".join(html),
            encoding="utf-8",
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
