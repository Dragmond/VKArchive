from pathlib import Path

from PySide6.QtCore import Qt, QThread
from PySide6.QtWidgets import (
    QFileDialog,
    QMainWindow,
    QMessageBox,
    QVBoxLayout,
    QWidget,
)

from gui.download_event_bridge import DownloadEventBridge
from gui.download_progress import DownloadProgressWidget
from gui.download_queue import DownloadQueueWidget
from gui.export_worker import ExportWorker
from gui.status_bar_widget import StatusBarWidget
from gui.toolbar_widget import ToolbarWidget
from media.export_session import ExportSession


class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()

        self.setWindowTitle("VK Archive")
        self.resize(900, 700)

        self.exportSession: ExportSession | None = None
        self.exportThread: QThread | None = None
        self.exportWorker: ExportWorker | None = None

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

        self.eventBridge.exportEventChanged.connect(
            self._update_export_statistics,
            Qt.ConnectionType.QueuedConnection,
        )

        self.toolbarWidget.loginButton.clicked.connect(
            self._create_export_session,
        )

    def _create_export_session(self) -> None:

        directory = QFileDialog.getExistingDirectory(
            self,
            "Выберите папку для архива",
        )

        if not directory:
            return

        self.exportSession = ExportSession(
            Path(directory),
        )

        self.eventBridge.connect_session(
            self.exportSession,
        )

        self.statusWidget.set_operation(
            "Сессия экспорта создана"
        )

    def start_export(
        self,
        conversation_name: str,
        messages: list,
    ) -> None:

        if self.exportSession is None:

            QMessageBox.warning(
                self,
                "VK Archive",
                "Сначала создайте сессию экспорта.",
            )

            return

        self.toolbarWidget.set_export_running(True)

        self.exportThread = QThread(self)

        self.exportWorker = ExportWorker(
            self.exportSession,
            conversation_name,
            messages,
        )

        self.exportWorker.moveToThread(
            self.exportThread,
        )

        self.exportThread.started.connect(
            self.exportWorker.run,
        )

        self.exportWorker.finished.connect(
            self._export_finished,
        )

        self.exportWorker.failed.connect(
            self._export_failed,
        )

        self.exportWorker.finished.connect(
            self.exportThread.quit,
        )

        self.exportWorker.failed.connect(
            self.exportThread.quit,
        )

        self.exportThread.finished.connect(
            self.exportThread.deleteLater,
        )

        self.exportThread.start()

    def _export_finished(
        self,
        result,
    ) -> None:

        self.toolbarWidget.set_export_running(False)

        self.statusWidget.set_operation(
            "Экспорт завершён"
        )

        QMessageBox.information(
            self,
            "VK Archive",
            f"Экспорт завершён.\n\n{result}",
        )

        self.exportWorker = None
        self.exportThread = None

    def _export_failed(
        self,
        error: str,
    ) -> None:

        self.toolbarWidget.set_export_running(False)

        self.statusWidget.set_operation(
            "Ошибка экспорта"
        )

        QMessageBox.critical(
            self,
            "VK Archive",
            error,
        )

        self.exportWorker = None
        self.exportThread = None

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

    def _update_export_statistics(
        self,
        event: str,
        value: int,
    ) -> None:

        if event == "dialog":

            self.statusWidget.increment_dialogs(
                value,
            )

        elif event == "message":

            self.statusWidget.increment_messages(
                value,
            )

        elif event == "file":

            self.statusWidget.increment_files(
                value,
            )

    def reset_download_progress(self) -> None:

        self.progressWidget.reset()

        self.queueWidget.clear_queue()

        self.statusWidget.reset()

    def closeEvent(
        self,
        event,
    ):

        if self.exportThread is not None:

            self.exportThread.quit()
            self.exportThread.wait()

        self.eventBridge.disconnect_manager()

        super().closeEvent(event)
