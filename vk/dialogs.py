from __future__ import annotations

from dataclasses import dataclass

from vk.api import VKApi


@dataclass(slots=True)
class DialogInfo:

    peer_id: int
    title: str
    unread_count: int
    last_message_id: int


class DialogService:

    def __init__(
        self,
        api: VKApi,
    ) -> None:

        self._api = api

    def load_dialogs(self) -> list[DialogInfo]:

        result = self._api.get_dialogs()

        dialogs: list[DialogInfo] = []

        for item in result["items"]:

            conversation = item["conversation"]
            peer = conversation["peer"]

            chat_settings = conversation.get(
                "chat_settings",
                {},
            )

            title = chat_settings.get(
                "title",
                f"Диалог {peer['id']}",
            )

            dialogs.append(
                DialogInfo(
                    peer_id=peer["id"],
                    title=title,
                    unread_count=conversation.get(
                        "unread_count",
                        0,
                    ),
                    last_message_id=item["last_message"]["id"],
                )
            )

        dialogs.sort(
            key=lambda d: d.last_message_id,
            reverse=True,
        )

        return dialogs
