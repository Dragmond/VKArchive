from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

from media import MediaFile
from media.download_manager import download_manager
from media.html_renderer import HtmlRenderer
from media.media_mapper import media_mapper
from vk.groups import groups
from vk.messages import Message
from vk.users import users


ExportEventCallback = Callable[[str, int], None]


class ArchiveExporter:

    def __init__(
        self,
        root: Path,
    ) -> None:

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
            self._event_callback(event, value)

    @staticmethod
    def _safe_name(
        name: str,
    ) -> str:

        invalid = '<>:"/\\|?*'

        for char in invalid:
            name = name.replace(char, "_")

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

        media: list[MediaFile] = []

        user_ids: set[int] = set()

        group_ids: set[int] = set()

        for message in messages:

            if message.from_id > 0:
                user_ids.add(message.from_id)
            elif message.from_id < 0:
                group_ids.add(message.from_id)

        user_map = users.get(
            list(user_ids),
        )

        group_map = groups.get(
            list(group_ids),
        )
