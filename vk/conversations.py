from __future__ import annotations

from dataclasses import dataclass

from vk.client import client


@dataclass(slots=True)
class Conversation:

    peer_id: int

    title: str

    last_message_id: int

    unread_count: int

    can_write: bool


class ConversationsService:

    def get_page(
        self,
        *,
        offset: int = 0,
        count: int = 200,
    ) -> list[Conversation]:

        response = client.request(
            "messages.getConversations",
            offset=offset,
            count=count,
            extended=1,
        )

        conversations: list[Conversation] = []

        for item in response["items"]:

            conversation = item["conversation"]

            peer = conversation["peer"]

            chat_settings = conversation.get("chat_settings", {})

            title = chat_settings.get(
                "title",
                f'Peer {peer["id"]}',
            )

            conversations.append(
                Conversation(
                    peer_id=peer["id"],
                    title=title,
                    last_message_id=conversation["last_message_id"],
                    unread_count=conversation.get(
                        "unread_count",
                        0,
                    ),
                    can_write=conversation.get(
                        "can_write",
                        {}).get(
                            "allowed",
                            False,
                        ),
                )
            )

        return conversations

    def get_all(self) -> list[Conversation]:

        result: list[Conversation] = []

        offset = 0

        page_size = 200

        while True:

            page = self.get_page(
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


conversations = ConversationsService()
