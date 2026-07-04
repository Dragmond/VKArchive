from __future__ import annotations

from dataclasses import dataclass

from vk.client import client


@dataclass(slots=True)
class Message:

    id: int

    date: int

    peer_id: int

    from_id: int

    text: str

    out: bool

    attachments: list[dict]


class MessagesService:

    def get_page(
        self,
        peer_id: int,
        *,
        offset: int = 0,
        count: int = 200,
    ) -> list[Message]:

        response = client.request(
            "messages.getHistory",
            peer_id=peer_id,
            offset=offset,
            count=count,
        )

        messages: list[Message] = []

        for item in response["items"]:

            messages.append(
                Message(
                    id=item["id"],
                    date=item["date"],
                    peer_id=peer_id,
                    from_id=item["from_id"],
                    text=item.get("text", ""),
                    out=bool(item.get("out", 0)),
                    attachments=item.get("attachments", []),
                )
            )

        return messages

    def get_all(
        self,
        peer_id: int,
    ) -> list[Message]:

        result: list[Message] = []

        offset = 0

        page_size = 200

        while True:

            page = self.get_page(
                peer_id,
                offset=offset,
                count=page_size,
            )

            if not page:
                break

            result.extend(page)

            if len(page) < page_size:
                break

            offset += page_size

        return result


messages = MessagesService()
