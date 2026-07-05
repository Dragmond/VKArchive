from __future__ import annotations

from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QVBoxLayout,
    QWidget,
)


class DownloadProgressWidget(QWidget):

    def __init__(self, parent=None):

        super().__init__(parent)

        layout = QVBoxLayout(self)

        header = QHBoxLayout()

        self.progressLabel = QLabel("Готов")

        header.addWidget(self.progressLabel)

        header.addStretch()

        self.progressPercent = QLabel("0%")

        header.addWidget(self.progressPercent)

        layout.addLayout(header)

        self.progressBar = QProgressBar()

        self.progressBar.setRange(0, 100)

        layout.addWidget(self.progressBar)

        self.currentFileLabel = QLabel()

        self.currentFileLabel.setWordWrap(True)

        layout.addWidget(self.currentFileLabel)

    def set_progress(
        self,
        current: int,
        total: int,
        filename: str,
    ) -> None:

        if total <= 0:

            self.reset()

            return

        percent = int(current * 100 / total)

        self.progressBar.setValue(percent)

        self.progressPercent.setText(
            f"{percent}%"
        )

        self.progressLabel.setText(
            f"Загружено {current} из {total}"
        )

        self.currentFileLabel.setText(filename)

    def reset(self) -> None:

        self.progressBar.setValue(0)

        self.progressPercent.setText("0%")

        self.progressLabel.setText("Готов")

        self.currentFileLabel.clear()
