from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class HistoryState:

    last_message_id: int | None = None

    requests: int = 0

    loaded_messages: int = 0

    stopped: bool = False

    def register_request(self) -> None:

        self.requests += 1

    def register_page(
        self,
        count: int,
    ) -> None:

        self.loaded_messages += count

    def stop(self) -> None:

        self.stopped = True
