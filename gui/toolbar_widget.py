from __future__ import annotations

from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QPushButton,
    QWidget,
)


class ToolbarWidget(QWidget):

    def __init__(self, parent=None):

        super().__init__(parent)

        layout = QHBoxLayout(self)

        layout.setContentsMargins(0, 0, 0, 0)

        self.titleLabel = QLabel("VK Archive")

        self.titleLabel.setStyleSheet("""
            font-size:26px;
            font-weight:bold;
        """)

        layout.addWidget(self.titleLabel)

        layout.addStretch()

        self.loginButton = QPushButton("Войти в VK")

        layout.addWidget(self.loginButton)

        self.cancelButton = QPushButton(
            "Отменить экспорт"
        )

        self.cancelButton.setEnabled(False)

        layout.addWidget(self.cancelButton)

    def set_export_running(
        self,
        running: bool,
    ) -> None:

        self.loginButton.setEnabled(
            not running
        )

        self.cancelButton.setEnabled(
            running
        )
