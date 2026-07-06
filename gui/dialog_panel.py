from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QHBoxLayout,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from gui.dialog_list_widget import DialogListWidget
from vk.dialogs import DialogInfo


class DialogPanel(QWidget):

    dialogSelected = Signal(DialogInfo)
    exportRequested = Signal()
    refreshRequested = Signal()

    def __init__(self, parent=None):

        super().__init__(parent)

        layout = QVBoxLayout(self)

        self.dialogList = DialogListWidget()

        layout.addWidget(self.dialogList)

        buttons = QHBoxLayout()

        self.refreshButton = QPushButton(
            "Обновить"
        )

        self.exportButton = QPushButton(
            "Экспорт"
        )

        self.exportButton.setEnabled(False)

        buttons.addWidget(self.refreshButton)
        buttons.addStretch()
        buttons.addWidget(self.exportButton)

        layout.addLayout(buttons)

        self.dialogList.dialogSelected.connect(
            self._dialog_selected,
        )

        self.refreshButton.clicked.connect(
            self.refreshRequested.emit,
        )

        self.exportButton.clicked.connect(
            self.exportRequested.emit,
        )

    def set_dialogs(
        self,
        dialogs: list[DialogInfo],
    ) -> None:

        self.dialogList.set_dialogs(dialogs)

        self.exportButton.setEnabled(False)

    def selected_dialog(
        self,
    ) -> DialogInfo | None:

        return self.dialogList.selected_dialog()

    def clear(
        self,
    ) -> None:

        self.dialogList.clear_dialogs()

        self.exportButton.setEnabled(False)

    def _dialog_selected(
        self,
        dialog: DialogInfo,
    ) -> None:

        self.exportButton.setEnabled(True)

        self.dialogSelected.emit(dialog)
