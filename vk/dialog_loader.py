from __future__ import annotations

from vk.dialogs import DialogInfo, DialogService


class DialogLoader:

    def __init__(
        self,
        service: DialogService,
    ) -> None:

        self._service = service

    def load(self) -> list[DialogInfo]:

        dialogs = self._service.load_dialogs()

        dialogs.sort(
            key=lambda dialog: (
                dialog.unread_count > 0,
                dialog.last_message_id,
            ),
            reverse=True,
        )

        return dialogs
