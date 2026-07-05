from __future__ import annotations

from PySide6.QtCore import QObject, QThread, Signal

from gui.export_worker import ExportWorker
from media.export_session import ExportSession


class ExportController(QObject):

    finished = Signal(object)
    failed = Signal(str)
    cancelled = Signal()

    def __init__(self, parent=None):

        super().__init__(parent)

        self._thread: QThread | None = None
        self._worker: ExportWorker | None = None
        self._session: ExportSession | None = None

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

        self._session = session

        self._thread = QThread(self)

        self._worker = ExportWorker(
            session,
            conversation_name,
            messages,
        )

        self._worker.moveToThread(self._thread)

        self._thread.started.connect(
            self._worker.run,
        )

        self._worker.finished.connect(
            self.finished.emit,
        )

        self._worker.failed.connect(
            self.failed.emit,
        )

        self._worker.finished.connect(
            self.stop,
        )

        self._worker.failed.connect(
            self.stop,
        )

        self._thread.finished.connect(
            self._cleanup,
        )

        self._thread.start()

    def cancel(self) -> None:

        if not self.is_running:
            return

        if self._session is not None:

            self._session.cancel()

        self.stop()

        self.cancelled.emit()

    def stop(self) -> None:

        if self._thread is None:
            return

        self._thread.quit()
        self._thread.wait()

    def _cleanup(self) -> None:

        if self._worker is not None:
            self._worker.deleteLater()

        if self._thread is not None:
            self._thread.deleteLater()

        self._worker = None
        self._thread = None
        self._session = None
