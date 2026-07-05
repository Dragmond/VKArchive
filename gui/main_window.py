from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QMainWindow,
    QVBoxLayout,
    QWidget,
)

from gui.download_event_bridge import DownloadEventBridge
from gui.download_progress import DownloadProgressWidget
from gui.download_queue import DownloadQueueWidget
from gui.status_bar_widget import StatusBarWidget
from gui.toolbar_widget import ToolbarWidget


class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()

        self.setWindowTitle("VK Archive")
        self.resize(900, 700)

        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout(central)

        self.toolbarWidget = ToolbarWidget()
        layout.addWidget(self.toolbarWidget)

        self.progressWidget = DownloadProgressWidget()
        layout.addWidget(self.progressWidget)

        self.queueWidget = DownloadQueueWidget()
        layout.addWidget(self.queueWidget)

        self.statusWidget = StatusBarWidget()
        layout.addWidget(self.statusWidget)

        self.eventBridge = DownloadEventBridge(self)

        self.eventBridge.progressChanged.connect(
            self.progressWidget.set_progress,
            Qt.ConnectionType.QueuedConnection,
        )

        self.eventBridge.stateChanged.connect(
            self._update_state,
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

            self.statusWidget.set_operation(
                "Файл добавлен в очередь"
            )

        elif state == "started":

            self.queueWidget.mark_downloading(
                filename,
                media_type,
            )

            self.statusWidget.set_operation(
                f"Загрузка: {filename}"
            )

        elif state == "completed":

            self.queueWidget.mark_completed(
                filename,
                media_type,
            )

            self.statusWidget.set_operation(
                "Загрузка завершена"
            )

        elif state == "failed":

            self.queueWidget.mark_failed(
                filename,
                media_type,
            )

            self.statusWidget.set_operation(
                f"Ошибка загрузки: {filename}"
            )

    def reset_download_progress(self) -> None:

        self.progressWidget.reset()

        self.queueWidget.clear_queue()

        self.statusWidget.reset()

    def closeEvent(
        self,
        event,
    ):

        self.eventBridge.disconnect_manager()

        super().closeEvent(event)
