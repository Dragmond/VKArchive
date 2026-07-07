from __future__ import annotations

from dataclasses import dataclass, field

from database.database import db
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

    reply_message: "Message | None" = None

    fwd_messages: list["Message"] = field(
        default_factory=list,
    )


class MessagesService:

    def _parse_message(
        self,
        item: dict,
        peer_id: int,
    ) -> Message:

        reply = item.get(
            "reply_message",
        )

        forwarded = item.get(
            "fwd_messages",
            [],
        )

        return Message(
            id=item["id"],
            date=item["date"],
            peer_id=peer_id,
            from_id=item["from_id"],
            text=item.get(
                "text",
                "",
            ),
            out=bool(
                item.get(
                    "out",
                    0,
                )
            ),
            attachments=item.get(
                "attachments",
                [],
            ),
            reply_message=(
                self._parse_message(
                    reply,
                    peer_id,
                )
                if reply
                else None
            ),
            fwd_messages=[
                self._parse_message(
                    message,
                    peer_id,
                )
                for message in forwarded
            ],
        )

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

        return [
            self._parse_message(
                item,
                peer_id,
            )
            for item in response["items"]
        ]

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

    def sync(
        self,
        peer_id: int,
    ) -> list[Message]:
        """
        Загружает историю и сохраняет только новые сообщения.
        """

        last_message_id = db.get_last_message_id(
            peer_id,
        )

        new_messages: list[Message] = []

        for message in reversed(
            self.get_all(
                peer_id,
            )
        ):

            if (
                last_message_id is not None
                and message.id <= last_message_id
            ):
                continue

            db.save_message(
                message_id=message.id,
                peer_id=message.peer_id,
                sender_id=message.from_id,
                date=message.date,
                text=message.text,
                outgoing=message.out,
            )

            new_messages.append(
                message,
            )

        return new_messages


messages = MessagesService()
