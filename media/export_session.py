from __future__ import annotations

from pathlib import Path

from media.exporter import ArchiveExporter
from vk.messages import Message


class ExportCancelledError(Exception):
    """Raised when the export process is cancelled by the user."""


class ExportSession:

    def __init__(
        self,
        output_directory: Path,
    ) -> None:

        self._exporter = ArchiveExporter(
            output_directory,
        )

        self._running = False
        self._cancel_requested = False

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

    @property
    def is_cancelled(
        self,
    ) -> bool:

        return self._cancel_requested

    def cancel(
        self,
    ) -> None:

        self._cancel_requested = True

    def reset_cancel(
        self,
    ) -> None:

        self._cancel_requested = False

    def _check_cancelled(
        self,
    ) -> None:

        if self._cancel_requested:

            raise ExportCancelledError(
                "Экспорт отменён пользователем."
            )

    def run(
        self,
        conversation_name: str,
        messages: list[Message],
    ) -> Path:

        self.reset_cancel()

        self._running = True

        try:

            self._check_cancelled()

            html = self._exporter.export_messages(
                conversation_name,
                messages,
            )

            attachments = []

            for message in messages:

                self._check_cancelled()

                attachments.extend(
                    getattr(
                        message,
                        "attachments",
                        [],
                    )
                )

            if attachments:

                self._check_cancelled()

                self._exporter.export_media(
                    conversation_name,
                    attachments,
                )

            self._check_cancelled()

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
