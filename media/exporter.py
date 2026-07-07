from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

from media import MediaFile
from media.download_manager import download_manager
from media.html_renderer import HtmlRenderer
from vk.messages import Message


ExportEventCallback = Callable[[str, int], None]


class ArchiveExporter:

    def __init__(self, root: Path) -> None:

        self._root = root

        self._renderer = HtmlRenderer()

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
    def _safe_name(
        name: str,
    ) -> str:

        invalid = '<>:"/\\|?*'

        for char in invalid:

            name = name.replace(
                char,
                "_",
            )

        return name.strip() or "Conversation"

    def export_messages(
        self,
        conversation_name: str,
        messages: list[Message],
    ) -> Path:

        folder = self._root / self._safe_name(
            conversation_name,
        )

        folder.mkdir(
            parents=True,
            exist_ok=True,
        )

        self._emit("dialog")

        for _ in messages:

            self._emit("message")

        for message in messages:

            for _ in getattr(
                message,
                "attachments",
                [],
            ):

                self._emit("file")

        output = folder / "messages.html"

        html = self._renderer.render(
            conversation_name,
            messages,
        )

        output.write_text(
            html,
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
            / self._safe_name(
                conversation_name,
            )
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
