from __future__ import annotations

from html import escape

from vk.attachment import Attachment


class AttachmentRenderer:

    def render(
        self,
        attachment: Attachment,
    ) -> str:

        attachment_type = attachment.type

        url = (
            attachment.url
            or attachment.vk_url
            or ""
        )

        title = (
            attachment.title
            or url.split("/")[-1]
            or attachment_type
        )

        filename = escape(title)

        safe_url = escape(url)

        match attachment_type:

            case "photo":

                if not url:
                    return ""

                return (
                    f"<a href='{safe_url}'>"
                    f"<img src='{safe_url}' loading='lazy'>"
                    "</a>"
                )

            case "video":

                preview = attachment.extra.get(
                    "preview",
                )

                if preview:

                    return (
                        f"<a href='{safe_url}'>"
                        f"<img src='{escape(preview)}' "
                        "loading='lazy'>"
                        "</a>"
                    )

                return (
                    "<div class='attachment'>"
                    f"🎬 <a href='{safe_url}'>{filename}</a>"
                    "</div>"
                )

            case "voice":

                if url:

                    return (
                        "<div class='attachment'>"
                        f"<audio controls "
                        f"src='{safe_url}'></audio>"
                        "</div>"
                    )

                return (
                    "<div class='attachment'>"
                    "🎤 Голосовое сообщение"
                    "</div>"
                )

            case "audio":

                artist = attachment.extra.get(
                    "artist",
                )

                if artist:

                    filename = escape(
                        f"{artist} — {title}"
                    )

                return (
                    "<div class='attachment'>"
                    f"🎵 <a href='{safe_url}'>{filename}</a>"
                    "</div>"
                )

            case "doc":

                ext = attachment.extra.get(
                    "ext",
                )

                if ext:

                    filename = escape(
                        f"{title}.{ext}"
                    )

                return (
                    "<div class='attachment'>"
                    f"📄 <a href='{safe_url}'>{filename}</a>"
                    "</div>"
                )

            case "sticker":

                if not url:
                    return ""

                return (
                    f"<img src='{safe_url}' "
                    "class='sticker'>"
                )

            case "link":

                return (
                    "<div class='attachment'>"
                    f"🔗 <a href='{safe_url}'>{filename}</a>"
                    "</div>"
                )

            case "poll":

                votes = attachment.extra.get(
                    "votes",
                    0,
                )

                answers = attachment.extra.get(
                    "answers",
                    0,
                )

                return (
                    "<div class='attachment'>"
                    f"📊 <strong>{filename}</strong><br>"
                    f"Вариантов: {answers}<br>"
                    f"Голосов: {votes}"
                    "</div>"
                )
