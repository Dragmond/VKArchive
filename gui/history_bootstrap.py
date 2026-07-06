from __future__ import annotations

from pathlib import Path

from vk.api import VKApi
from vk.auth import VKAuthService
from vk.history import HistoryService
from vk.history_loader import HistoryLoader


def create_history_loader() -> HistoryLoader | None:

    auth = VKAuthService(
        Path("config.json"),
    )

    session = auth.load_session()

    if session is None:
        return None

    api = VKApi(
        session.access_token,
    )

    return HistoryLoader(
        HistoryService(api),
    )
