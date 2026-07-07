from __future__ import annotations

from enum import StrEnum


class AttachmentType(StrEnum):

    PHOTO = "photo"

    VIDEO = "video"

    AUDIO = "audio"

    AUDIO_MESSAGE = "audio_message"

    DOC = "doc"

    LINK = "link"

    POLL = "poll"

    GEO = "geo"

    WALL = "wall"

    GIFT = "gift"

    GRAFFITI = "graffiti"

    STORY = "story"

    MARKET = "market"

    MARKET_ALBUM = "market_album"

    CALL = "call"

    STICKER = "sticker"
