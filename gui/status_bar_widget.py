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

        self.operationLabel = QLabel("Готов")

        layout.addWidget(self.operationLabel)

        layout.addStretch()

        self.statisticsLabel = QLabel(
            "Диалогов: 0 | Сообщений: 0 | Файлов: 0"
        )

        layout.addWidget(self.statisticsLabel)

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

        self.statisticsLabel.setText(
            f"Диалогов: {dialogs} | "
            f"Сообщений: {messages} | "
            f"Файлов: {files}"
        )

    def reset(self) -> None:

        self.set_operation("Готов")

        self.set_statistics(
            0,
            0,
            0,
        )
