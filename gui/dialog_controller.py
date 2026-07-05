from __future__ import annotations

from PySide6.QtCore import QObject, Signal

from vk.dialog_loader import DialogLoader
from vk.dialogs import DialogInfo


class DialogController(QObject):

    dialogsLoaded = Signal(list)
    loadFailed = Signal(str)

    def __init__(
        self,
        loader: DialogLoader,
        parent=None,
    ) -> None:

        super().__init__(parent)

        self._loader = loader

    def load(self) -> None:

        try:

            dialogs = self._loader.load()

        except Exception as exc:

            self.loadFailed.emit(str(exc))
            return

        self.dialogsLoaded.emit(dialogs)

    @staticmethod
    def selected_peer(
        dialog: DialogInfo | None,
    ) -> int | None:

        if dialog is None:
            return None

        return dialog.peer_id
