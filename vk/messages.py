from __future__ import annotations

from dataclasses import dataclass, field

from database.database import db
from database.message_batch import MessageBatch
from vk.attachment_parser import attachment_parser
from vk.client import client


BATCH_SIZE = 1000


@dataclass(slots=True)
class Message:

    id: int
    date: int
    peer_id: int
    from_id: int
    text: str
    out: bool

    attachments: list[dict]

    action: dict | None = None

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

        reply = item.get("reply_message")

        return Message(
            id=item.get("id", 0),
            date=item.get("date", 0),
            peer_id=peer_id,
            from_id=item.get("from_id", 0),
            text=item.get("text", ""),
            out=bool(item.get("out", 0)),
            attachments=attachment_parser.parse(
                item.get("attachments", [])
            ),
            action=item.get("action"),
            reply_message=(
                self._parse_message(reply, peer_id)
                if reply
                else None
            ),
            fwd_messages=[
                self._parse_message(message, peer_id)
                for message in item.get(
                    "fwd_messages",
                    [],
                )
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
            self._parse_message(item, peer_id)
            for item in response["items"]
        ]

    def sync(
        self,
        peer_id: int,
    ) -> list[Message]:

        last_message_id = db.get_last_message_id(peer_id)

        page_size = 200
        offset = 0

        new_messages: list[Message] = []

        batch = MessageBatch()

        stop = False

        db.begin()

        try:

            while not stop:

                page = self.get_page(
                    peer_id,
                    offset=offset,
                    count=page_size,
                )

                if not page:
                    break

                for message in reversed(page):

                    if (
                        last_message_id is not None
                        and message.id <= last_message_id
                    ):
                        stop = True
                        break

                    batch.add(
                        message_id=message.id,
                        peer_id=message.peer_id,
                        sender_id=message.from_id,
                        date=message.date,
                        text=message.text,
                        outgoing=message.out,
                    )

                    new_messages.append(message)

                    if batch.size >= BATCH_SIZE:

                        db.save_messages(batch)

                        batch.clear()

                if stop:
                    break

                if len(page) < page_size:
                    break

                offset += page_size

            if not batch.empty:

                db.save_messages(batch)

            db.commit()

        except Exception:

            db.rollback()
            raise

        new_messages.reverse()

        return new_messages


messages = MessagesService()
