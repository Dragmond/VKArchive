from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class MessageBatch:

    rows: list[tuple] = field(
        default_factory=list,
    )

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

    def extend(
        self,
        other: "MessageBatch",
    ) -> None:

        self.rows.extend(
            other.rows,
        )

    def clear(self) -> None:

        self.rows.clear()

    @property
    def size(self) -> int:

        return len(
            self.rows,
        )

    @property
    def empty(self) -> bool:

        return not self.rows
