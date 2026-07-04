from __future__ import annotations

from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QAbstractItemView,
    QHeaderView,
    QTableWidget,
    QTableWidgetItem,
)


class DownloadQueueWidget(QTableWidget):

    STATUS_WAITING = "Ожидание"
    STATUS_DOWNLOADING = "Загрузка"
    STATUS_COMPLETED = "✓ Завершено"
    STATUS_FAILED = "Ошибка"

    STATUS_COLORS = {
        STATUS_WAITING: QColor("#9e9e9e"),
        STATUS_DOWNLOADING: QColor("#4ea3ff"),
        STATUS_COMPLETED: QColor("#39c16c"),
        STATUS_FAILED: QColor("#ff5555"),
    }

    def __init__(self, parent=None):

        super().__init__(0, 3, parent)

        self._rows: dict[str, int] = {}

        self.setHorizontalHeaderLabels(
            [
                "Файл",
                "Статус",
                "Тип",
            ]
        )

        header = self.horizontalHeader()

        header.setStretchLastSection(True)

        header.setSectionResizeMode(
            0,
            QHeaderView.ResizeMode.Stretch,
        )

        header.setSectionResizeMode(
            1,
            QHeaderView.ResizeMode.ResizeToContents,
        )

        header.setSectionResizeMode(
            2,
            QHeaderView.ResizeMode.ResizeToContents,
        )

        self.verticalHeader().setVisible(False)

        self.setSelectionMode(
            QAbstractItemView.SelectionMode.NoSelection,
        )

        self.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers,
        )

    def clear_queue(self) -> None:

        self.setRowCount(0)

        self._rows.clear()

    def ensure_item(
        self,
        filename: str,
        media_type: str,
    ) -> int:

        row = self._rows.get(filename)

        if row is not None:
            return row

        row = self.rowCount()

        self.insertRow(row)

        self._rows[filename] = row

        self.setItem(
            row,
            0,
            QTableWidgetItem(filename),
        )

        self.setItem(
            row,
            2,
            QTableWidgetItem(media_type),
        )

        self._set_status(
            row,
            self.STATUS_WAITING,
        )

        return row

    def _set_status(
        self,
        row: int,
        status: str,
    ) -> None:

        item = QTableWidgetItem(status)

        item.setForeground(
            self.STATUS_COLORS.get(
                status,
                QColor("#ffffff"),
            )
        )

        self.setItem(
            row,
            1,
            item,
        )

        self.scrollToBottom()

    def update_status(
        self,
        filename: str,
        media_type: str,
        status: str,
    ) -> None:

        row = self.ensure_item(
            filename,
            media_type,
        )

        self._set_status(
            row,
            status,
        )

    def mark_waiting(
        self,
        filename: str,
        media_type: str,
    ) -> None:

        self.update_status(
            filename,
            media_type,
            self.STATUS_WAITING,
        )

    def mark_downloading(
        self,
        filename: str,
        media_type: str,
    ) -> None:

        self.update_status(
            filename,
            media_type,
            self.STATUS_DOWNLOADING,
        )

    def mark_completed(
        self,
        filename: str,
        media_type: str,
    ) -> None:

        self.update_status(
            filename,
            media_type,
            self.STATUS_COMPLETED,
        )

    def mark_failed(
        self,
        filename: str,
        media_type: str,
    ) -> None:

        self.update_status(
            filename,
            media_type,
            self.STATUS_FAILED,
        )
