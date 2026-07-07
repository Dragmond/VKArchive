from __future__ import annotations

from datetime import datetime
from html import escape

from media.attachment_renderer import AttachmentRenderer
from media.date_formatter import DateFormatter
from media.system_message_renderer import SystemMessageRenderer
from vk.messages import Message
from vk.user import User


class HtmlRenderer:

    def __init__(self) -> None:

        self._attachment_renderer = AttachmentRenderer()
        self._system_renderer = SystemMessageRenderer()

    def render(
        self,
        conversation_name: str,
        messages: list[Message],
        users: dict[int, User],
    ) -> str:

        html: list[str] = [
            "<!DOCTYPE html>",
            "<html lang='ru'>",
            "<head>",
            "<meta charset='utf-8'>",
            "<meta name='viewport' content='width=device-width,initial-scale=1'>",
            f"<title>{escape(conversation_name)}</title>",
            "<style>",
            "body{font-family:Segoe UI,Arial,sans-serif;background:#202124;color:#eee;margin:0;padding:24px;}",
            "h1{margin-top:0;}",
            ".day-divider{margin:28px 0 18px;padding:8px 14px;background:#303134;border-radius:8px;text-align:center;font-weight:bold;color:#ddd;}",
            ".message{padding:12px;border-bottom:1px solid #444;}",
            ".meta{color:#9aa0a6;font-size:12px;margin-bottom:6px;}",
            ".system-message{margin:8px 0;padding:8px 12px;background:#39424e;border-left:4px solid #8ab4f8;border-radius:6px;color:#d7e3ff;font-size:13px;}",
            ".text{white-space:pre-wrap;word-break:break-word;}",
            ".attachments{margin-top:10px;display:flex;flex-wrap:wrap;gap:10px;}",
            ".attachments img{max-width:260px;border-radius:8px;}",
            ".sticker{max-width:192px;max-height:192px;}",
            ".attachment{background:#303134;padding:6px 10px;border-radius:6px;}",
            ".forwarded{margin-top:12px;margin-left:20px;padding-left:12px;border-left:3px solid #5f6368;}",
            ".forwarded-title{color:#9aa0a6;font-size:12px;margin-bottom:8px;}",
            ".reply{margin-top:10px;margin-bottom:10px;padding:8px 12px;border-left:3px solid #8ab4f8;background:#2d3136;border-radius:6px;}",
            ".reply-title{color:#8ab4f8;font-size:12px;margin-bottom:6px;}",
            "a{color:#8ab4f8;text-decoration:none;}",
            "</style>",
            "</head>",
            "<body>",
            f"<h1>{escape(conversation_name)}</h1>",
        ]

        current_day: str | None = None

        for message in messages:

            day = DateFormatter.key(message.date)

            if day != current_day:

                current_day = day

                html.append(
                    (
                        "<div class='day-divider'>"
                        f"{DateFormatter.title(message.date)}"
                        "</div>"
                    )
                )

            html.append(
                self._render_message(
                    message,
                    users,
                )
            )

        html.extend(
            [
                "</body>",
                "</html>",
            ]
        )

        return "\n".join(html)

    def _render_message(
        self,
        message: Message,
        users: dict[int, User],
    ) -> str:

        timestamp = datetime.fromtimestamp(
            message.date,
        ).strftime("%H:%M:%S")

        direction = (
            "Исходящее"
            if getattr(message, "out", False)
            else "Входящее"
        )

        user = users.get(message.from_id)

        author = (
            user.full_name
            if user is not None
            else f"ID {message.from_id}"
        )

        parts = [
            "<div class='message'>",
            (
                "<div class='meta'>"
                f"{timestamp} • {direction} • "
                f"{escape(author)}"
                "</div>"
            ),
        ]

        system_html = self._system_renderer.render(
            getattr(message, "action", None),
        )

        if system_html:
            parts.append(system_html)

        if message.text:

            parts.append(
                (
                    "<div class='text'>"
                    f"{escape(message.text)}"
                    "</div>"
                )
            )

        parts.append(
            self._render_reply_message(
                message,
                users,
            )
        )

        parts.append(
            self._render_forwarded_messages(
                message,
                users,
            )
        )

        attachments = getattr(
            message,
            "attachments",
            [],
        )

        if attachments:

            parts.append("<div class='attachments'>")

            for attachment in attachments:

                parts.append(
                    self._attachment_renderer.render(
                        attachment,
                    )
                )

            parts.append("</div>")

        parts.append("</div>")
