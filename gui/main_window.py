from pathlib import Path

from PySide6.QtCore import QMetaObject, Qt
from PySide6.QtWidgets import (
    QAbstractItemView,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QProgressBar,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from media import MediaFile
from media.download_manager import download_manager


class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()

        self.setWindowTitle("VK Archive")
        self.resize(900, 700)

        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout(central)

        title = QLabel("VK Archive")
        title.setStyleSheet("""
            font-size:26px;
            font-weight:bold;
        """)
        layout.addWidget(title)

        self.loginButton = QPushButton("Войти в VK")
        layout.addWidget(self.loginButton)

        progressLayout = QHBoxLayout()

        self.progressLabel = QLabel("Готов")
        progressLayout.addWidget(self.progressLabel)

        progressLayout.addStretch()

        self.progressPercent = QLabel("0%")
        progressLayout.addWidget(self.progressPercent)

        layout.addLayout(progressLayout)

        self.progressBar = QProgressBar()
        self.progressBar.setRange(0, 100)
        layout.addWidget(self.progressBar)

        self.currentFileLabel = QLabel()
        self.currentFileLabel.setWordWrap(True)
        layout.addWidget(self.currentFileLabel)

        self.queueTable = QTableWidget(0, 3)
        self.queueTable.setHorizontalHeaderLabels(
            [
                "Файл",
                "Статус",
                "Тип",
            ]
        )
        self.queueTable.horizontalHeader().setStretchLastSection(True)
        self.queueTable.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers
        )
        self.queueTable.setSelectionMode(
            QAbstractItemView.SelectionMode.NoSelection
        )

        layout.addWidget(self.queueTable)

        download_manager.set_progress_callback(
            self._download_progress_callback
        )

    def _download_progress_callback(
        self,
        current: int,
        total: int,
        media: MediaFile,
    ) -> None:

        filename = media.filename or Path(media.url).name

        QMetaObject.invokeMethod(
            self,
            lambda: self._update_progress(
                current,
                total,
                filename,
                media.type,
            ),
            Qt.ConnectionType.QueuedConnection,
        )

    def _update_progress(
        self,
        current: int,
        total: int,
        filename: str,
        media_type: str,
    ) -> None:

        self.set_download_progress(
            current,
            total,
            filename,
        )

        row = self.queueTable.rowCount()

        self.queueTable.insertRow(row)

        self.queueTable.setItem(
            row,
            0,
            QTableWidgetItem(filename),
        )

        self.queueTable.setItem(
            row,
            1,
            QTableWidgetItem("✓ Завершено"),
        )

        self.queueTable.setItem(
            row,
            2,
            QTableWidgetItem(media_type),
        )

        self.queueTable.scrollToBottom()

    def set_download_progress(
        self,
        current: int,
        total: int,
        filename: str,
    ) -> None:

        if total <= 0:

            self.progressBar.setValue(0)

            self.progressPercent.setText("0%")

            self.progressLabel.setText("Готов")

            self.currentFileLabel.clear()

            return

        percent = int(current * 100 / total)

        self.progressBar.setValue(percent)

        self.progressPercent.setText(f"{percent}%")

        self.progressLabel.setText(
            f"Загружено {current} из {total}"
        )

        self.currentFileLabel.setText(filename)

    def reset_download_progress(self) -> None:

        self.progressBar.setValue(0)

        self.progressPercent.setText("0%")

        self.progressLabel.setText("Готов")

        self.currentFileLabel.clear()

        self.queueTable.setRowCount(0)

    def closeEvent(self, event):

        download_manager.set_progress_callback(None)

        super().closeEvent(event)
