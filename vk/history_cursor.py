from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class HistoryCursor:

    offset: int = 0

    total: int = 0

    loaded: int = 0

    @property
    def finished(self) -> bool:

        return self.loaded >= self.total
