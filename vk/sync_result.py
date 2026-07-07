from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class SyncResult:

    loaded_messages: int = 0

    saved_messages: int = 0

    api_requests: int = 0

    interrupted: bool = False

    def register_request(self) -> None:

        self.api_requests += 1

    def register_loaded(
        self,
        count: int,
    ) -> None:

        self.loaded_messages += count

    def register_saved(self) -> None:

        self.saved_messages += 1
