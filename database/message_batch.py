from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class MessageBatch:

    rows: list[tuple] = None

    def __post_init__(self) -> None:

        if self.rows is None:
            self.rows = []

    def add(
        self,
        *,
        message_id: int,
        peer_id: int,
        sender_id: int,
        date: int,
        text: str,
        outgoing: bool,
    ) -> None:

        self.rows.append(
            (
                message_id,
                peer_id,
                sender_id,
                date,
                text,
                int(outgoing),
            )
        )

    @property
    def empty(self) -> bool:

        return not self.rows
