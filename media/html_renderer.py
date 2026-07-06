from __future__ import annotations

from pathlib import Path

from vk.messages import Message


class HtmlRenderer:

    def render(
        self,
        conversation_name: str,
        messages: list[Message],
    ) -> str:

        ...

    def _render_message(
        self,
        message: Message,
    ) -> str:

        ...

    def _render_attachment(
        self,
        attachment,
    ) -> str:

        ...

    def _render_photo(
        self,
        attachment,
    ) -> str:

        ...

    def _render_video(
        self,
        attachment,
    ) -> str:

        ...

    def _render_voice(
        self,
        attachment,
    ) -> str:

        ...

    def _render_document(
        self,
        attachment,
    ) -> str:

        ...

    def _render_audio(
        self,
        attachment,
    ) -> str:

        ...

    def _render_sticker(
        self,
        attachment,
    ) -> str:

        ...

    def _render_link(
        self,
        attachment,
    ) -> str:

        ...
