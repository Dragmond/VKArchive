from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class User:

    id: int

    first_name: str

    last_name: str

    photo: str | None = None

    @property
    def full_name(self) -> str:

        return f"{self.first_name} {self.last_name}".strip()
