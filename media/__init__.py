from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class MediaFile:

    type: str

    url: str

    filename: str | None = None

    size: int | None = None
