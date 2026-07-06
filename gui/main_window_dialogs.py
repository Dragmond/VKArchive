from __future__ import annotations

from PySide6.QtWidgets import QMessageBox

from gui.history_bootstrap import create_history_loader


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

        if self.exportSession is None:

            QMessageBox.warning(
                self,
                "VK Archive",
                "Сначала создайте сессию экспорта.",
            )

            return

        loader = create_history_loader()

        if loader is None:

            QMessageBox.warning(
                self,
                "VK Archive",
                "Не выполнен вход.",
            )

            return

        self.statusWidget.set_operation(
            f"Загрузка сообщений: {dialog.title}"
        )

        messages = loader.load(
            dialog.peer_id,
        )

        self.start_export(
            dialog.title,
            messages,
        )
