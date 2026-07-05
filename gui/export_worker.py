from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QObject, Signal, Slot

from media.export_session import ExportSession
from vk.messages import Message


class ExportWorker(QObject):

    finished = Signal(Path)
    failed = Signal(str)

    def __init__(
        self,
        session: ExportSession,
        conversation_name: str,
        messages: list[Message],
    ) -> None:

        super().__init__()

        self._session = session
        self._conversation_name = conversation_name
        self._messages = messages

    @Slot()
    def run(self) -> None:

        try:

            result = self._session.run(
                self._conversation_name,
                self._messages,
            )

            self.finished.emit(result)

        except Exception as error:

            self.failed.emit(str(error))
