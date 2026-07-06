from __future__ import annotations

from pathlib import Path

from gui.dialog_controller import DialogController
from vk.api import VKApi
from vk.auth import VKAuthService
from vk.dialog_loader import DialogLoader
from vk.dialogs import DialogService


def create_dialog_controller(
    parent=None,
) -> DialogController | None:

    auth = VKAuthService(
        Path("config.json"),
    )

    session = auth.load_session()

    if session is None:
        return None

    api = VKApi(
        session.access_token,
    )

    loader = DialogLoader(
        DialogService(api),
    )

    return DialogController(
        loader,
        parent,
    )
