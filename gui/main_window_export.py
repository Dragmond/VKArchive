from __future__ import annotations

from PySide6.QtWidgets import QMessageBox

from gui.export_controller import ExportController


class MainWindowExportMixin:

    def _setup_export_controller(self) -> None:

        self.exportController = ExportController(self)

        self.exportController.finished.connect(
            self._export_finished,
        )

        self.exportController.failed.connect(
            self._export_failed,
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

        self.exportController.start(
            self.exportSession,
            conversation_name,
            messages,
        )

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
