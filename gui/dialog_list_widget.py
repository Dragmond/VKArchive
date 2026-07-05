from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QListWidget, QListWidgetItem

from vk.dialogs import DialogInfo


class DialogListWidget(QListWidget):

    dialogSelected = Signal(DialogInfo)

    def __init__(self, parent=None):

        super().__init__(parent)

        self._dialogs: list[DialogInfo] = []

        self.itemClicked.connect(
            self._on_item_clicked,
        )

    def set_dialogs(
        self,
        dialogs: list[DialogInfo],
    ) -> None:

        self.clear()

        self._dialogs = dialogs

        for dialog in dialogs:

            text = dialog.title

            if dialog.unread_count:

                text += f" ({dialog.unread_count})"

            item = QListWidgetItem(text)

            item.setData(
                Qt.ItemDataRole.UserRole,
                dialog,
            )

            self.addItem(item)

    def clear_dialogs(self) -> None:

        self._dialogs.clear()
        self.clear()

    def selected_dialog(self) -> DialogInfo | None:

        item = self.currentItem()

        if item is None:
            return None

        return item.data(
            Qt.ItemDataRole.UserRole,
        )

    def _on_item_clicked(
        self,
        item: QListWidgetItem,
    ) -> None:

        dialog = item.data(
            Qt.ItemDataRole.UserRole,
        )

        if dialog is not None:

            self.dialogSelected.emit(dialog)
