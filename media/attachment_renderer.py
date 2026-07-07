from __future__ import annotations

from html import escape


class AttachmentRenderer:

    def render(
        self,
        attachment: dict,
    ) -> str:

        attachment_type = attachment.get("type", "")

        url = (
            attachment.get("url")
            or attachment.get("vk_url")
            or ""
        )

        title = (
            attachment.get("title")
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

                preview = attachment.get("preview")

                if preview:

                    preview = escape(preview)

                    return (
                        f"<a href='{safe_url}'>"
                        f"<img src='{preview}' "
                        f"loading='lazy'>"
                        "</a>"
                    )

                return (
                    "<div class='attachment'>"
                    "🎬 "
                    f"<a href='{safe_url}'>"
                    f"{filename}"
                    "</a>"
                    "</div>"
                )

            case "voice":

                if url:

                    return (
                        "<div class='attachment'>"
                        f"<audio controls src='{safe_url}'></audio>"
                        "</div>"
                    )

                return (
                    "<div class='attachment'>"
                    "🎤 Голосовое сообщение"
                    "</div>"
                )

            case "audio":

                artist = attachment.get("artist")

                if artist:

                    filename = escape(
                        f"{artist} — {title}"
                    )

                return (
                    "<div class='attachment'>"
                    "🎵 "
                    f"<a href='{safe_url}'>"
                    f"{filename}"
                    "</a>"
                    "</div>"
                )

            case "doc":

                ext = attachment.get("ext")

                if ext:

                    filename = escape(
                        f"{title}.{ext}"
                    )

                return (
                    "<div class='attachment'>"
                    "📄 "
                    f"<a href='{safe_url}'>"
                    f"{filename}"
                    "</a>"
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
                    "🔗 "
                    f"<a href='{safe_url}'>"
                    f"{safe_url}"
                    "</a>"
                    "</div>"
                )

            case _:

                return (
                    "<div class='attachment'>"
                    "📎 "
                    f"<a href='{safe_url}'>"
                    f"{filename}"
                    "</a>"
                    "</div>"
                )
