from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QObject, Signal

from media import MediaFile
from media.download_manager import download_manager
from media.export_session import ExportSession


class DownloadEventBridge(QObject):

    progressChanged = Signal(int, int, str)
    stateChanged = Signal(str, str, str)

    # event, value
    exportEventChanged = Signal(str, int)

    def __init__(self, parent=None):

        super().__init__(parent)

        self._session: ExportSession | None = None

        download_manager.set_progress_callback(
            self._progress_callback
        )

        download_manager.set_state_callback(
            self._state_callback
        )

    @staticmethod
    def _filename(
        media: MediaFile,
    ) -> str:

        return media.filename or Path(
            media.url
        ).name

    def connect_session(
        self,
        session: ExportSession,
    ) -> None:

        if self._session is session:
            return

        if self._session is not None:
            self.disconnect_session()

        self._session = session

        self._session.set_event_callback(
            self._export_callback
        )

    def disconnect_session(
        self,
    ) -> None:

        if self._session is None:
            return

        self._session.set_event_callback(
            None,
        )

        self._session = None

    def _progress_callback(
        self,
        current: int,
        total: int,
        media: MediaFile,
    ) -> None:

        self.progressChanged.emit(
            current,
            total,
            self._filename(media),
        )

    def _state_callback(
        self,
        state: str,
        media: MediaFile,
    ) -> None:

        self.stateChanged.emit(
            state,
            self._filename(media),
            media.type,
        )

    def _export_callback(
        self,
        event: str,
        value: int,
    ) -> None:

        self.exportEventChanged.emit(
            event,
            value,
        )

    def disconnect_manager(
        self,
    ) -> None:

        self.disconnect_session()

        download_manager.set_progress_callback(
            None
        )

        download_manager.set_state_callback(
            None
        )
