from __future__ import annotations

from datetime import datetime
from html import escape

from vk.messages import Message


class HtmlRenderer:

    def render(
        self,
        conversation_name: str,
        messages: list[Message],
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
            ".message{padding:12px;border-bottom:1px solid #444;}",
            ".meta{color:#9aa0a6;font-size:12px;margin-bottom:6px;}",
            ".text{white-space:pre-wrap;word-break:break-word;}",
            ".attachments{margin-top:10px;display:flex;flex-wrap:wrap;gap:10px;}",
            ".attachments img{max-width:260px;border-radius:8px;}",
            ".sticker{max-width:192px;max-height:192px;}",
            ".attachment{background:#303134;padding:6px 10px;border-radius:6px;}",
            ".forwarded{margin-top:12px;margin-left:20px;padding-left:12px;border-left:3px solid #5f6368;}",
            ".forwarded-title{color:#9aa0a6;font-size:12px;margin-bottom:8px;}",
            "a{color:#8ab4f8;text-decoration:none;}",
            "</style>",
            "</head>",
            "<body>",
            f"<h1>{escape(conversation_name)}</h1>",
        ]

        for message in messages:
            html.append(self._render_message(message))

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
    ) -> str:

        timestamp = datetime.fromtimestamp(
            message.date
        ).strftime("%Y-%m-%d %H:%M:%S")

        direction = (
            "Исходящее"
            if message.out
            else "Входящее"
        )

       parts.append(
    self._render_forwarded_messages(
        message,
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
                    self._render_attachment(
                        attachment,
                    )
                )

            parts.append("</div>")

        parts.append("</div>")

        return "\n".join(parts)

def _render_attachment(
    self,
    attachment,
) -> str:

    filename = escape(
        attachment.filename
        or attachment.url.split("/")[-1]
    )

    match attachment.type:

        case "photo":

            return (
                f"<a href='media/{filename}'>"
                f"<img src='media/{filename}' "
                f'loading="lazy"></a>'
            )

        case "video":

            return (
                "<div class='attachment'>"
                f"<video controls width='420' "
                f"src='media/{filename}'></video>"
                "</div>"
            )

        case "voice":

            return (
                "<div class='attachment'>"
                f"<audio controls src='media/{filename}'></audio>"
                "</div>"
            )

        case "audio":

            return (
                "<div class='attachment'>"
                f"🎵 <a href='media/{filename}'>{filename}</a>"
                "</div>"
            )

        case "document":

            return (
                "<div class='attachment'>"
                f"📄 <a href='media/{filename}'>{filename}</a>"
                "</div>"
            )

        case "sticker":

            return (
                f"<img src='media/{filename}' "
                "class='sticker'>"
            )

        case "link":

            return (
                "<div class='attachment'>"
                f"🔗 <a href='{escape(attachment.url)}'>"
                f"{escape(attachment.url)}</a>"
                "</div>"
            )

        case _:

            return (
                "<div class='attachment'>"
                f"📎 <a href='media/{filename}'>{filename}</a>"
                "</div>"
            )
def _render_forwarded_messages(
    self,
    message,
) -> str:

    forwarded = getattr(
        message,
        "fwd_messages",
        [],
    )

    if not forwarded:
        return ""

    parts = [
        "<div class='forwarded'>",
        "<div class='forwarded-title'>Пересланные сообщения</div>",
    ]

    for forwarded_message in forwarded:

        parts.append(
            self._render_message(
                forwarded_message,
            )
        )

    parts.append("</div>")

    return "\n".join(parts)
