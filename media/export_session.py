from __future__ import annotations

from pathlib import Path

from media.exporter import ArchiveExporter
from vk.messages import Message


class ExportSession:

    def __init__(
        self,
        output_directory: Path,
    ) -> None:

        self._exporter = ArchiveExporter(
            output_directory,
        )

        self._running = False

    @property
    def exporter(
        self,
    ) -> ArchiveExporter:

        return self._exporter

    @property
    def is_running(
        self,
    ) -> bool:

        return self._running

    def run(
        self,
        conversation_name: str,
        messages: list[Message],
    ) -> Path:

        self._running = True

        try:

            html = self._exporter.export_messages(
                conversation_name,
                messages,
            )

            attachments = []

            for message in messages:

                attachments.extend(
                    getattr(
                        message,
                        "attachments",
                        [],
                    )
                )

            if attachments:

                self._exporter.export_media(
                    conversation_name,
                    attachments,
                )

            return html

        finally:

            self._running = False

    def set_event_callback(
        self,
        callback,
    ) -> None:

        self._exporter.set_event_callback(
            callback,
        )
