from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class Attachment:

    type: str

    title: str | None = None

    url: str | None = None

    vk_url: str | None = None

    owner_id: int | None = None

    id: int | None = None

    data: dict = field(default_factory=dict)

    extra: dict = field(default_factory=dict)
