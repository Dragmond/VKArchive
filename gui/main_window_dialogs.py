from __future__ import annotations

from PySide6.QtWidgets import QMessageBox


class MainWindowDialogsMixin:

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

    def _export_selected_dialog(
        self,
    ) -> None:

        dialog = self.dialogPanel.selected_dialog()

        if dialog is None:

            self.statusWidget.set_operation(
                "Диалог не выбран"
            )

            return

        self.statusWidget.set_operation(
            f"Экспорт: {dialog.title}"
        )

        # На следующем коммите здесь появится:
        # HistoryController
        # ExportController.start(...)
