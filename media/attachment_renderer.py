from __future__ import annotations

from html import escape


class AttachmentRenderer:

    def render(
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
                    f"loading='lazy'></a>"
                )

            case "video":

                return (
                    "<div class='attachment'>"
                    f"<video controls "
                    f"width='420' "
                    f"src='media/{filename}'>"
                    "</video>"
                    "</div>"
                )

            case "voice":

                return (
                    "<div class='attachment'>"
                    f"<audio controls "
                    f"src='media/{filename}'>"
                    "</audio>"
                    "</div>"
                )

            case "audio":

                return (
                    "<div class='attachment'>"
                    f"🎵 "
                    f"<a href='media/{filename}'>"
                    f"{filename}"
                    "</a>"
                    "</div>"
                )

            case "document":

                return (
                    "<div class='attachment'>"
                    f"📄 "
                    f"<a href='media/{filename}'>"
                    f"{filename}"
                    "</a>"
                    "</div>"
                )

            case "sticker":

                return (
                    f"<img "
                    f"src='media/{filename}' "
                    f"class='sticker'>"
                )

            case "link":

                return (
                    "<div class='attachment'>"
                    "🔗 "
                    f"<a href='{escape(attachment.url)}'>"
                    f"{escape(attachment.url)}"
                    "</a>"
                    "</div>"
                )

            case _:

                return (
                    "<div class='attachment'>"
                    "📎 "
                    f"<a href='media/{filename}'>"
                    f"{filename}"
                    "</a>"
                    "</div>"
                )
