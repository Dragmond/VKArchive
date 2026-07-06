from __future__ import annotations

from dataclasses import dataclass

from vk.api import VKApi


@dataclass(slots=True)
class HistoryMessage:

    id: int
    date: int
    from_id: int
    text: str
    attachments: list


class HistoryService:

    def __init__(
        self,
        api: VKApi,
    ) -> None:

        self._api = api

    def load_history(
        self,
        peer_id: int,
    ) -> list[HistoryMessage]:

        offset = 0

        messages: list[HistoryMessage] = []

        while True:

            response = self._api.get_history(
                peer_id=peer_id,
                count=200,
                offset=offset,
            )

            items = response["items"]

            if not items:
                break

            for item in items:

                messages.append(
                    HistoryMessage(
                        id=item["id"],
                        date=item["date"],
                        from_id=item["from_id"],
                        text=item.get("text", ""),
                        attachments=item.get(
                            "attachments",
                            [],
                        ),
                    )
                )

            offset += len(items)

            if len(items) < 200:
                break

        messages.reverse()

        return messages
