from __future__ import annotations

from vk.history import HistoryMessage, HistoryService


class HistoryLoader:

    def __init__(
        self,
        service: HistoryService,
    ) -> None:

        self._service = service

    def load(
        self,
        peer_id: int,
    ) -> list[HistoryMessage]:

        messages = self._service.load_history(
            peer_id,
        )

        messages.sort(
            key=lambda message: (
                message.date,
                message.id,
            ),
        )

        return messages
