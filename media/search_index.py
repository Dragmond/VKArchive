from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from vk.messages import Message


@dataclass(slots=True)
class SearchDocument:

    conversation: str

    message_id: int

    sender_id: int

    date: int

    text: str

    html_file: str


class SearchIndexBuilder:

    def __init__(self, root: Path):

        self._root = root

    def build(
        self,
        conversation_name: str,
        html_file: str,
        messages: list[Message],
    ) -> Path:

        output = self._root / "search-index.json"

        documents: list[dict] = []

        if output.exists():

            documents = json.loads(
                output.read_text(
                    encoding="utf-8",
                )
            )

        for message in messages:

            text = message.text.strip()

            if not text:
                continue

            documents.append(
                SearchDocument(
                    conversation=conversation_name,
                    message_id=message.id,
                    sender_id=message.from_id,
                    date=message.date,
                    text=text,
                    html_file=html_file,
                ).__dict__
            )

        output.write_text(
            json.dumps(
                documents,
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        return output
