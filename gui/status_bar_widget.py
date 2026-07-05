from __future__ import annotations

from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QWidget,
)


class StatusBarWidget(QWidget):

    def __init__(self, parent=None):

        super().__init__(parent)

        layout = QHBoxLayout(self)

        layout.setContentsMargins(0, 0, 0, 0)

        self._dialogs = 0
        self._messages = 0
        self._files = 0

        self.operationLabel = QLabel("Готов")
        layout.addWidget(self.operationLabel)

        layout.addStretch()

        self.statisticsLabel = QLabel()

        layout.addWidget(self.statisticsLabel)

        self._update_statistics_label()

    def _update_statistics_label(self) -> None:

        self.statisticsLabel.setText(
            f"Диалогов: {self._dialogs} | "
            f"Сообщений: {self._messages} | "
            f"Файлов: {self._files}"
        )

    def set_operation(
        self,
        operation: str,
    ) -> None:

        self.operationLabel.setText(operation)

    def set_statistics(
        self,
        dialogs: int,
        messages: int,
        files: int,
    ) -> None:

        self._dialogs = dialogs
        self._messages = messages
        self._files = files

        self._update_statistics_label()

    def increment_dialogs(
        self,
        count: int = 1,
    ) -> None:

        self._dialogs += count

        self._update_statistics_label()

    def increment_messages(
        self,
        count: int = 1,
    ) -> None:

        self._messages += count

        self._update_statistics_label()

    def increment_files(
        self,
        count: int = 1,
    ) -> None:

        self._files += count

        self._update_statistics_label()

    def reset(self) -> None:

        self._dialogs = 0
        self._messages = 0
        self._files = 0

        self.set_operation("Готов")

        self._update_statistics_label()
