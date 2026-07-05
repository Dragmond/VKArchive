from pathlib import Path

from PySide6.QtCore import QMetaObject, Qt
from PySide6.QtWidgets import (
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from gui.download_progress import DownloadProgressWidget
from gui.download_queue import DownloadQueueWidget
from media import MediaFile
from media.download_manager import download_manager


class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()

        self.setWindowTitle("VK Archive")
        self.resize(900, 700)

        central = QWidget()

        self.setCentralWidget(central)

        layout = QVBoxLayout(central)

        title = QLabel("VK Archive")

        title.setStyleSheet("""
            font-size:26px;
            font-weight:bold;
        """)

        layout.addWidget(title)

        self.loginButton = QPushButton("Войти в VK")

        layout.addWidget(self.loginButton)

        self.progressWidget = DownloadProgressWidget()

        layout.addWidget(self.progressWidget)

        self.queueWidget = DownloadQueueWidget()

        layout.addWidget(self.queueWidget)

        layout.addStretch()

        download_manager.set_progress_callback(
            self._download_progress_callback
        )

        download_manager.set_state_callback(
            self._download_state_callback
        )

    def _download_state_callback(
        self,
        state: str,
        media: MediaFile,
    ) -> None:

        filename = media.filename or Path(media.url).name

        QMetaObject.invokeMethod(
            self,
            lambda: self._update_state(
                state,
                filename,
                media.type,
            ),
            Qt.ConnectionType.QueuedConnection,
        )

    def _update_state(
        self,
        state: str,
        filename: str,
        media_type: str,
    ) -> None:

        if state == "queued":

            self.queueWidget.mark_waiting(
                filename,
                media_type,
            )

        elif state == "started":

            self.queueWidget.mark_downloading(
                filename,
                media_type,
            )

        elif state == "completed":

            self.queueWidget.mark_completed(
                filename,
                media_type,
            )

        elif state == "failed":

            self.queueWidget.mark_failed(
                filename,
                media_type,
            )

    def _download_progress_callback(
        self,
        current: int,
        total: int,
        media: MediaFile,
    ) -> None:

        filename = media.filename or Path(media.url).name

        QMetaObject.invokeMethod(
            self,
            lambda: self.progressWidget.set_progress(
                current,
                total,
                filename,
            ),
            Qt.ConnectionType.QueuedConnection,
        )

    def reset_download_progress(self) -> None:

        self.progressWidget.reset()

        self.queueWidget.clear_queue()

    def closeEvent(
        self,
        event,
    ):

        download_manager.set_progress_callback(None)
        download_manager.set_state_callback(None)

        super().closeEvent(event)
