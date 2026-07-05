from __future__ import annotations

from PySide6.QtCore import QObject, QThread, Signal

from gui.export_worker import ExportWorker
from media.export_session import ExportSession


class ExportController(QObject):

    finished = Signal(object)
    failed = Signal(str)

    def __init__(
        self,
        parent=None,
    ) -> None:

        super().__init__(parent)

        self._thread: QThread | None = None
        self._worker: ExportWorker | None = None

    @property
    def is_running(self) -> bool:

        return self._thread is not None

    def start(
        self,
        session: ExportSession,
        conversation_name: str,
        messages: list,
    ) -> None:

        if self.is_running:
            return

        self._thread = QThread()

        self._worker = ExportWorker(
            session,
            conversation_name,
            messages,
        )

        self._worker.moveToThread(
            self._thread,
        )

        self._thread.started.connect(
            self._worker.run,
        )

        self._worker.finished.connect(
            self.finished,
        )

        self._worker.failed.connect(
            self.failed,
        )

        self._worker.finished.connect(
            self._thread.quit,
        )

        self._worker.failed.connect(
            self._thread.quit,
        )

        self._thread.finished.connect(
            self._cleanup,
        )

        self._thread.start()

    def stop(self) -> None:

        if self._thread is None:
            return

        self._thread.quit()
        self._thread.wait()

    def _cleanup(self) -> None:

        if self._thread is not None:

            self._thread.deleteLater()

        if self._worker is not None:

            self._worker.deleteLater()

        self._thread = None
        self._worker = None
