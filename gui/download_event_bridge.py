from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QObject, Signal

from media import MediaFile
from media.download_manager import download_manager


class DownloadEventBridge(QObject):

    progressChanged = Signal(int, int, str)
    stateChanged = Signal(str, str, str)

    # event, value
    exportEventChanged = Signal(str, int)

    def __init__(self, parent=None):

        super().__init__(parent)

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

    def connect_exporter(
        self,
        exporter,
    ) -> None:

        exporter.set_event_callback(
            self._export_callback
        )

    def disconnect_exporter(
        self,
        exporter,
    ) -> None:

        exporter.set_event_callback(None)

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

    def disconnect_manager(self) -> None:

        download_manager.set_progress_callback(None)
        download_manager.set_state_callback(None)
