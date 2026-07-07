from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class HistoryState:

    last_message_id: int = 0

    loaded_messages: int = 0

    api_requests: int = 0

    @property
    def has_history(self) -> bool:

        return self.last_message_id > 0

    def register_request(self) -> None:

        self.api_requests += 1

    def register_messages(
        self,
        count: int,
    ) -> None:

        self.loaded_messages += count
