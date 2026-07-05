from __future__ import annotations

from collections.abc import Callable
from datetime import datetime
from html import escape
from pathlib import Path

from media import MediaFile
from media.download_manager import download_manager
from vk.messages import Message


ExportEventCallback = Callable[[str, int], None]


class ArchiveExporter:

    def __init__(self, root: Path) -> None:

        self._root = root

        self._event_callback: ExportEventCallback | None = None

    def set_event_callback(
        self,
        callback: ExportEventCallback | None,
    ) -> None:

        self._event_callback = callback

    def _emit(
        self,
        event: str,
        value: int = 1,
    ) -> None:

        if self._event_callback is not None:

            self._event_callback(
                event,
                value,
            )

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

        self._emit("dialog")

        output = folder / "messages.html"

        html: list[str] = [
            "<!DOCTYPE html>",
            "<html lang='ru'>",
            "<head>",
            "<meta charset='utf-8'>",
            "<meta name='viewport' content='width=device-width,initial-scale=1'>",
            f"<title>{escape(conversation_name)}</title>",
            "<style>",
            "body{font-family:Segoe UI,Arial,sans-serif;background:#202124;color:#eee;margin:0;padding:24px;}",
            "h1{margin-top:0;}",
            ".message{padding:12px;border-bottom:1px solid #444;}",
            ".meta{color:#9aa0a6;font-size:12px;margin-bottom:6px;}",
            ".text{white-space:pre-wrap;word-break:break-word;}",
            ".attachments{margin-top:10px;display:flex;flex-wrap:wrap;gap:10px;}",
            ".attachments img{max-width:260px;border-radius:8px;}",
            ".attachment{background:#303134;padding:6px 10px;border-radius:6px;}",
            "a{color:#8ab4f8;text-decoration:none;}",
            "</style>",
            "</head>",
            "<body>",
            f"<h1>{escape(conversation_name)}</h1>",
        ]

        for message in messages:

            self._emit("message")

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
                ]
            )

            attachments = getattr(
                message,
                "attachments",
                [],
            )

            if attachments:

                html.append("<div class='attachments'>")

                for media in attachments:

                    filename = escape(
                        media.filename or media.url.split("/")[-1]
                    )

                    self._emit("file")

                    if media.type == "photo":

                        html.append(
                            f"<a href='media/{filename}'>"
                            f"<img src='media/{filename}' "
                            f"loading='lazy'></a>"
                        )

                    elif media.type == "voice":

                        html.append(
                            "<div class='attachment'>"
                            f"<audio controls src='media/{filename}'></audio>"
                            "</div>"
                        )

                    elif media.type == "video":

                        html.append(
                            "<div class='attachment'>"
                            f"<video controls width='420' "
                            f"src='media/{filename}'></video>"
                            "</div>"
                        )

                    else:

                        html.append(
                            "<div class='attachment'>"
                            f"<a href='media/{filename}'>{filename}</a>"
                            "</div>"
                        )

                html.append("</div>")

            html.append("</div>")

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
