from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFileDialog,
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QMessageBox,
)

from gui.dialog_controller import DialogController
from gui.dialog_panel import DialogPanel
from gui.download_event_bridge import DownloadEventBridge
from gui.download_progress import DownloadProgressWidget
from gui.download_queue import DownloadQueueWidget
from gui.main_window_export import MainWindowExportMixin
from gui.status_bar_widget import StatusBarWidget
from gui.toolbar_widget import ToolbarWidget
from media.export_session import ExportSession
from vk.api import VKApi
from vk.auth import VKAuthService
from vk.dialog_loader import DialogLoader
from vk.dialogs import DialogService


class MainWindow(
    QMainWindow,
    MainWindowExportMixin,
):

    def __init__(self):

        super().__init__()

        self.setWindowTitle("VK Archive")
        self.resize(900, 700)

        self.exportSession: ExportSession | None = None

        self.authService = VKAuthService(
            Path("config.json"),
        )

        self.dialogController: DialogController | None = None

        session = self.authService.load_session()

        if session is not None:

            api = VKApi(session.access_token)

            loader = DialogLoader(
                DialogService(api),
            )

            self.dialogController = DialogController(
                loader,
                self,
            )

        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout(central)

        self.toolbarWidget = ToolbarWidget()
        layout.addWidget(self.toolbarWidget)

        self.dialogPanel = DialogPanel()
        layout.addWidget(self.dialogPanel)

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

        self.dialogPanel.exportRequested.connect(
            self._export_selected_dialog,
        )

        self.dialogPanel.refreshRequested.connect(
            self._load_dialogs,
        )

        if self.dialogController is not None:

            self.dialogController.dialogsLoaded.connect(
                self.dialogPanel.set_dialogs,
            )

            self.dialogController.loadFailed.connect(
                self._dialog_load_failed,
            )

        self._setup_export_controller()

    def _load_dialogs(self) -> None:

        if self.dialogController is None:

            QMessageBox.warning(
                self,
                "VK Archive",
                "Сначала выполните вход.",
            )

            return

        self.statusWidget.set_operation(
            "Загрузка диалогов..."
        )

        self.dialogController.load()

    def _dialog_load_failed(
        self,
        error: str,
    ) -> None:

        QMessageBox.critical(
            self,
            "VK Archive",
            error,
        )

        self.statusWidget.set_operation(
            "Ошибка загрузки"
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

    def _export_selected_dialog(self) -> None:

        dialog = self.dialogPanel.selected_dialog()

        if dialog is None:

            self.statusWidget.set_operation(
                "Диалог не выбран"
            )

            return

        self.statusWidget.set_operation(
            f"Экспорт: {dialog.title}"
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

    def _update_export_statistics(
        self,
        event: str,
        value: int,
    ) -> None:

        if event == "dialog":

            self.statusWidget.increment_dialogs(value)

        elif event == "message":

            self.statusWidget.increment_messages(value)

        elif event == "file":

            self.statusWidget.increment_files(value)

    def reset_download_progress(self) -> None:

        self.progressWidget.reset()
        self.queueWidget.clear_queue()
        self.statusWidget.reset()

    def closeEvent(
        self,
        event,
    ):

        if hasattr(self, "exportController"):

            self.exportController.stop()

        self.eventBridge.disconnect_manager()

        super().closeEvent(event)
